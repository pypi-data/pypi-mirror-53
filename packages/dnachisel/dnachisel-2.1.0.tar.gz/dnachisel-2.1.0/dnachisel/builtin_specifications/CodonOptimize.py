import numpy as np
from python_codon_tables import get_codons_table
from .CodonSpecification import CodonSpecification
from ..SpecEvaluation import SpecEvaluation
from ..biotools import (
    CODONS_TRANSLATIONS,
    CODONS_SEQUENCES,
    group_nearby_indices,
    dict_to_pretty_string,
)
from ..Location import Location


def codons_frequencies_and_positions(sequence):
    """Return dicts indicating codons frequencies and positions.

    Parameters
    ----------
    sequence
      A sequence with length divisible by 3 (like an ORF)

    Returns
    -------
    codons_frequencies
      A dict ``{'K': {'total': 60, 'AAA': 0.5, 'AAG': 0.4}}, 'M': {...} ...}``
      providing the frequency of each version of each codon in the given
      sequence.


    codons_positions
      A dict ``{'ATA': [2, 55, 1], 'ATG': [0] ...}`` indicating the position of
      the different codons in the sequence.

    """
    codons_positions = {cod: [] for cod in CODONS_TRANSLATIONS}
    for i in range(int(len(sequence) / 3)):
        codon = sequence[3 * i : 3 * (i + 1)]
        codons_positions[codon].append(i)
    # aa: amino-acid
    codons_frequencies = {aa: {"total": 0} for aa in CODONS_SEQUENCES}
    for codon, positions in codons_positions.items():
        count = len(positions)
        aa = CODONS_TRANSLATIONS[codon]
        codons_frequencies[aa][codon] = count
        codons_frequencies[aa]["total"] += count
    for aa, data in codons_frequencies.items():
        total = max(1, data["total"])
        for codon, value in data.items():
            if codon != "total":
                data[codon] = 1.0 * value / total
    return codons_frequencies, codons_positions


class CodonOptimize(CodonSpecification):
    """Codon-optimize a coding sequence for a particular species.

    Several codon-optimization policies exist. At the moment this Specification
    implements a method in which codons are replaced by the most frequent
    codon in the species.

    (as long as this doesn't break any Specification or lowers the global
    optimization objective)

    Parameters
    ----------

    species
      Either a TaxID (this requires a web connection as the corresponding table
      will be downloaded from the internet) or the name of the species to
      codon-optimize for (the name must be supported by ``python_codon_tables``
      e.g. ``e_coli``, ``s_cerevisiae``, ``h_sapiens``, ``c_elegans``,
      ``b_subtilis``, ``d_melanogaster``).
      Note that the species can be omited if a ``codon_usage_table`` is
      provided instead

    mode
      Either 'best_codon' or 'harmonized_frequencies'. For 'best_codon', the
      optimization will always replace a codon with the most-frequent triplet
      possible. For 'harmonized_frequencies', the optimization will bring the
      relative frequencies of the different triplets as close as possible to
      the frequencies in the reference species.

    location
      Either a DnaChisel Location or a tuple of the form (start, end, strand)
      or just (start, end), with strand defaulting to +1, indicating the
      position of the gene to codon-optimize. If not provided, the whole
      sequence is considered as the gene. The location should have a length
      that is a multiple of 3. The location strand is either 1 if the gene is
      encoded on the (+) strand, or -1 for antisense.

    codon_usage_table
      A dict of the form ``{'*': {"TGA": 0.112, "TAA": 0.68}, 'K': ...}``
      giving the RSCU table (relative usage of each codon). Only provide if
      no ``species`` parameter was provided.

    Examples
    --------

    >>> objective = CodonOptimizationSpecification(
    >>>     species = "E. coli",
    >>>     location = (150, 300), # coordinates of a gene
    >>>     strand = -1
    >>> )


    """

    best_possible_score = 0
    localization_group_spread = 3

    def __init__(
        self,
        species=None,
        location=None,
        mode="best_codon",
        codon_usage_table=None,
        boost=1.0,
    ):
        self.mode = mode
        self.boost = boost
        if isinstance(location, tuple):
            location = Location.from_tuple(location, default_strand=+1)
        self.location = location
        self.species = species
        if species is not None:
            codon_usage_table = get_codons_table(self.species)
            # codon_usage_table = CODON_USAGE_TABLES[self.species]
        if codon_usage_table is None:
            raise ValueError(
                "Provide either an species name or a codon " "usage table"
            )

        # PRECOMPUTE SOME TABLES (WILL BE PASSED ON TO LOCALIZED PROBLEMS)
        self.codon_usage_table = codon_usage_table
        if "codons_frequencies" not in self.codon_usage_table:
            self.codon_usage_table["codons_frequencies"] = dict(
                [
                    item
                    for aa_data in self.codon_usage_table.values()
                    for item in aa_data.items()
                ]
            )
        if "best_frequencies" not in self.codon_usage_table:
            self.codon_usage_table["best_frequencies"] = {
                aa: max(aa_data.values())
                for aa, aa_data in self.codon_usage_table.items()
                if aa != "codons_frequencies"
            }

    def initialized_on_problem(self, problem, role):
        """Get location from sequence if no location provided."""
        return self._copy_with_full_span_if_no_location(problem)

    def evaluate(self, problem):
        """ Return the sum of all codons frequencies.

        Note: no smart localization currently, the sequence is improved via

        """
        return {
            "best_codon": self.evaluate_best_codon,
            "harmonized_frequencies": self.evaluate_harmonized_frequencies,
        }[self.mode](problem)

    def codon_harmonization_stats(self, sequence):
        """Return a codon harmonisation score and a suboptimal locations list.

        Parameters
        ----------

        sequence
          An ATGC string

        species
          Any species name from the DnaChisel codon tables, such as ``e_coli``.

        Returns
        -------
        score, list_of_over_represented_codons_positions
          ``score`` is a negative number equals to sum(fi - ei) where for the
          i-th codon in the sequence fi is the relative frequency of this
          triplet in the sequence and ei is the relative frequency in the
          reference species. The ``list_of_suboptimal_codons_positions`` is
          of the form [1, 4, 5, 6...] a number k in that list indicates that
          the k-th codon is over-represented, and that a synonymous mutation
          of this codon can improve the harmonization score.

        """
        length = len(sequence)
        if length % 3:
            raise ValueError(
                "Coding sequence with size %d not multiple of 3)" % length
            )
        # codons_frequencies, codons_positions = \
        #     codons_frequencies_and_positions(sequence)
        score = 0
        nonoptimal_aa_indices = []
        codons_positions, aa_comparisons = self.compare_frequencies(sequence)
        for aa, data in aa_comparisons.items():
            total = data.pop("total")
            for codon, codon_freq in data.items():
                frequency_diff = codon_freq["sequence"] - codon_freq["table"]
                score -= total * abs(frequency_diff)
                if codon_freq["sequence"] > codon_freq["table"]:
                    nonoptimal_aa_indices += codons_positions[codon]
        return score, [3 * i for i in nonoptimal_aa_indices]

    def codons_indices_to_locations(self, indices):
        """Convert a list of codon positions to a list of Locations"""
        indices = np.array(indices)
        if self.location.strand == -1:
            indices = sorted(self.location.end - indices)
            return [
                Location(group[0] - 3, group[-1], strand=-1)
                for group in group_nearby_indices(
                    indices, max_group_spread=self.localization_group_spread
                )
            ]
        else:
            indices += self.location.start
            return [
                Location(group[0], group[-1] + 3)
                for group in group_nearby_indices(
                    indices, max_group_spread=self.localization_group_spread
                )
            ]

    def evaluate_best_codon(self, problem):
        """Return the evaluation for mode==best_codon."""
        subsequence = self.location.extract_sequence(problem.sequence)
        length = len(subsequence)
        if length % 3:
            raise ValueError(
                "CodonOptimizationSpecification on a window/sequence"
                "with size %d not multiple of 3)" % length
            )
        codons = [
            subsequence[3 * i : 3 * (i + 1)] for i in range(int(length / 3))
        ]
        CT = CODONS_TRANSLATIONS
        current_usage, optimal_usage = [
            np.array(e)
            for e in zip(
                *[
                    (
                        self.codon_usage_table["codons_frequencies"][codon],
                        self.codon_usage_table["best_frequencies"][CT[codon]],
                    )
                    for codon in codons
                ]
            )
        ]
        non_optimality = optimal_usage - current_usage
        nonoptimal_indices = 3 * np.nonzero(non_optimality)[0]
        locations = self.codons_indices_to_locations(nonoptimal_indices)
        score = -non_optimality.sum()
        return SpecEvaluation(
            self,
            problem,
            score=score,
            locations=locations,
            message="Codon opt. on window %s scored %.02E"
            % (self.location, score),
        )

    def evaluate_harmonized_frequencies(self, problem):
        """Return the evaluation for mode == harmonized_frequencies."""
        subsequence = self.location.extract_sequence(problem.sequence)
        score, nonoptimal_indices = self.codon_harmonization_stats(subsequence)
        locations = self.codons_indices_to_locations(nonoptimal_indices)
        np.random.shuffle(locations)
        return SpecEvaluation(
            self,
            problem,
            score=score,
            locations=locations,
            message="Codon opt. on window %s scored %.02E"
            % (self.location, score),
        )

    def localized_on_window(self, new_location, start_codon, end_codon):
        """Relocate without changing much."""
        if self.mode == "harmonized_frequencies":
            return self
        else:
            return self.__class__(
                species=self.species,
                location=new_location,
                codon_usage_table=self.codon_usage_table,
                boost=self.boost,
            )

    def label_parameters(self):
        return ["(custom table)" if self.species is None else self.species]

    def compare_frequencies(self, sequence, text_mode=False):
        """Return a dict indicating differences between codons frequencies in
        the sequence and in this specifications's codons usage table.

        Returns
        -------

        positions, comparisons
          (if text_mode = False)

        a formatted print-ready string
          (if text_mode = True)

        >>> {
        >>>   "K": {
        >>>     "total": 6,
        >>>     "AAA": {
        >>>         "sequence": 1.0,
        >>>         "table": 0.7
        >>>     },
        >>>     ...
        >>>   },
        >>>   "D": ...
        >>> }

        """
        frequencies, positions = codons_frequencies_and_positions(sequence)
        frequencies = {
            aa: data for aa, data in frequencies.items() if data["total"]
        }
        comparisons = {
            aa: {
                "total": seq_data["total"],
                **{
                    codon: {"sequence": seq_data[codon], "table": table_data}
                    for codon, table_data in self.codon_usage_table[aa].items()
                },
            }
            for aa, seq_data in frequencies.items()
        }
        if text_mode:
            return dict_to_pretty_string(comparisons)
        else:
            return positions, comparisons
