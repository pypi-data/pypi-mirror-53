"""Implement AvoidNonUniqueSegments(Specification)"""

from collections import defaultdict

from ..Specification import Specification

# from .VoidSpecification import VoidSpecification
from ..SpecEvaluation import SpecEvaluation
from dnachisel.biotools import reverse_complement
from dnachisel.Location import Location

from functools import lru_cache


def get_kmer_extractor(
    sequence, include_reverse_complement=True, min_length=1
):
    """Return a function (i => standardized_kmer_string)."""
    if include_reverse_complement:
        rev_comp_sequence = reverse_complement(sequence)
        L = len(sequence)

        def extract_kmer(i):
            subsequence = sequence[i : i + min_length]
            rev_comp = rev_comp_sequence[L - i - min_length : L - i]
            return min(subsequence, rev_comp)

    else:

        def extract_kmer(i):
            return sequence[i : i + min_length]

    return extract_kmer


@lru_cache(maxsize=1)
def get_kmer_extractor_cached(
    sequence, include_reverse_complement=True, min_length=1
):
    """Kmer extractor with memoization.
    
    This globally cached method enables much faster computations when
    several AvoidNonUniqueSegments functions with equal min_length are used. 
    """
    if include_reverse_complement:
        rev_comp_sequence = reverse_complement(sequence)
        L = len(sequence)

        @lru_cache(maxsize=len(sequence))
        def extract_kmer(i):
            subsequence = sequence[i : i + min_length]
            rev_comp = rev_comp_sequence[L - i - min_length : L - i]
            return min(subsequence, rev_comp)

    else:

        @lru_cache(maxsize=len(sequence))
        def extract_kmer(i):
            return sequence[i : i + min_length]

    return extract_kmer


class AvoidNonUniqueSegments(Specification):
    """Avoid sub-sequence which have repeats elsewhere in the sequence.

    NOTE: For sequences with subsequences appearing more than 2 times, the
    specification may not work as a problem constraint, but will work as a
    problem optimization objective.

    You can define a location L and an reference L* (by default they
    are both the full sequence)

    >>>          [=== L ===]
    >>>
    >>>       [=========== L* ==========]
    >>>
    >>> --------- Sequence --------------------------

    This Specification class specifies that "No sub-sequence in L of length
    above min_length has more than 1 occurence in L*".

    Some specific cases

    - L = L* = Sequence. In this case the full sequence will have only unique
      kmers above a certain size (no self-homology).
    - L < L*, L* = Sequence. The segment L will have no self-homology and no
      homology to the rest of the sequence above a certain size. But there
      can be self-homologies elsewhere in the sequence.
    - L = L*. segment L will have no self-homology.

    Parameters
    ----------
    min_length
      Minimal length of sequences to be considered repeats

    location
      Segment of the sequence in which to look for repeats. If None, repeats
      are searched in the full sequence.

    include_reverse_complement
      If True, the sequence repeats are also searched for in the reverse
      complement of the sequence (or sub sequence if `location` is not None).

    Examples
    --------

    >>> from dnachisel import *
    >>> sequence = random_dna_sequence(50000)
    >>> constraint= AvoidNonUniqueSegments(10, include_reverse_complement=True)
    >>> problem = DnaOptimizationProblem(sequence, constraints= [contraint])
    >>> print (problem.constraints_summary())
    """

    best_possible_score = 0
    use_cache = True
    # priority = -1

    def __init__(
        self,
        min_length,
        reference=None,
        location=None,
        include_reverse_complement=True,
        boost=1.0,
        localization_data=None,
    ):
        """Initialize."""
        self.min_length = min_length
        if isinstance(location, tuple):
            location = Location.from_tuple(location)
        self.location = location
        if reference in ['here', 'same']:
            reference = location
        if isinstance(reference, tuple):
            reference = Location.from_tuple(reference)
        self.reference = reference
        self.include_reverse_complement = include_reverse_complement
        self.boost = 1.0
        self.localization_data = localization_data

    def initialized_on_problem(self, problem, role="constraint"):
        """Location is the full sequence by default."""

        def location_or_default(location):
            default = Location(0, len(problem.sequence), 1)
            return default if location is None else location

        location = location_or_default(self.location)
        reference = location_or_default(self.reference)
        return self.copy_with_changes(
            location=location, reference=reference
        )

    def evaluate(self, problem):
        """Return 0 if the sequence has no repeats, else -number_of_repeats."""
        if self.localization_data is not None:
            return self.local_evaluation(problem)
        else:
            return self.global_evaluation(problem)

    def local_evaluation(self, problem):
        extract_kmer = self.get_kmer_extractor(problem.sequence)
        variable_kmers = {}
        for label in ("location", "extended"):
            variable_kmers[label] = d = {}
            for i in self.localization_data[label]["changing_indices"]:
                kmer = extract_kmer(i)
                if kmer not in d:
                    d[kmer] = [i]
                else:
                    d[kmer].append(i)

        nonunique_locations = []
        for kmer, indices in variable_kmers["location"].items():
            if len(indices) > 1:
                nonunique_locations += indices
        location_variable_kmers = set(variable_kmers["location"].keys())
        extended_variable_kmers = set(variable_kmers["extended"].keys())
        fixed_location_kmers = self.localization_data["location"][
            "fixed_kmers"
        ]
        extended_fixed_kmers = self.localization_data["extended"][
            "fixed_kmers"
        ]

        for c in [
            extended_variable_kmers,
            fixed_location_kmers,
            extended_fixed_kmers,
        ]:
            nonunique_locations += [
                i
                for kmer in location_variable_kmers.intersection(c)
                for i in variable_kmers["location"][kmer]
            ]

        for c in [location_variable_kmers, fixed_location_kmers]:
            nonunique_locations += [
                i
                for kmer in extended_variable_kmers.intersection(c)
                for i in variable_kmers["extended"][kmer]
            ]
        nonunique_locations = [
            Location(i, i + self.min_length) for i in nonunique_locations
        ]
        return SpecEvaluation(
            self,
            problem,
            score=-len(nonunique_locations),
            locations=nonunique_locations,
            message="Failed, the following positions are the first occurences"
            "of local non-unique segments %s" % nonunique_locations,
        )

    def get_kmer_extractor(self, sequence):
        if self.use_cache:
            getter = get_kmer_extractor_cached
        else:
            getter = get_kmer_extractor
        return getter(
            sequence,
            min_length=self.min_length,
            include_reverse_complement=self.include_reverse_complement,
        )

    def global_evaluation(self, problem):
        extract_kmer = self.get_kmer_extractor(problem.sequence)
        kmers_locations = defaultdict(lambda: [])
        start, end = self.reference.start, self.reference.end
        for i in range(start, end - self.min_length):
            location = (i, i + self.min_length)
            kmer_sequence = extract_kmer(i)
            kmers_locations[kmer_sequence].append(location)

        locations = sorted(
            [
                Location(start_, end_)
                for locations_list in kmers_locations.values()
                for start_, end_ in locations_list
                if len(locations_list) > 1
                and (self.location.start <= start_ < end_ < self.location.end)
            ],
            key=lambda l: l.start,
        )

        if locations == []:
            return SpecEvaluation(
                self,
                problem,
                score=0,
                locations=[],
                message="Passed: no nonunique %d-mer found." % self.min_length,
            )
        return SpecEvaluation(
            self,
            problem,
            score=-len(locations),
            locations=locations,
            message="Failed, the following positions are the first occurences "
            "of non-unique segments %s" % locations,
        )

    def localized(self, location, problem=None, with_righthand=True):
        """Localize the evaluation."""

        if location.overlap_region(self.reference) is None:
            return None
        if problem is None:
            return self
        extract_kmer = self.get_kmer_extractor(problem.sequence)
        k = self.min_length
        reference = location.extended(k - 1, right=with_righthand)
        changing_kmers_zone = reference.overlap_region(
            self.reference
        )
        changing_kmer_indices = set(changing_kmers_zone.indices[: -k + 1])
        localization_data = {}
        for loc, label in [
            (self.location, "location"),
            (self.reference, "extended"),
        ]:
            kmer_indices = set(loc.indices[: -self.min_length])
            fixed_kmer_indices = kmer_indices.difference(changing_kmer_indices)
            fixed_kmers = set([extract_kmer(i) for i in fixed_kmer_indices])
            changing_inds = kmer_indices.intersection(changing_kmer_indices)
            localization_data[label] = {
                "fixed_kmers": fixed_kmers,
                "changing_indices": changing_inds,
            }
        localization_data["extended"]["changing_indices"].difference_update(
            localization_data["location"]["changing_indices"]
        )
        return self.copy_with_changes(
            localization_data=localization_data, location=changing_kmers_zone
        )

    def shifted(self, shift):
        """Shift the location of the specification.
        This will also shift the reference.
        """
        new_location = None if self.location is None else self.location + shift
        reference = (
            None
            if self.reference is None
            else self.reference + shift
        )
        return self.copy_with_changes(
            location=new_location,
            reference=reference,
            derived_from=self,
        )

    def label_parameters(self):
        return [("min_length", str(self.min_length))]

    def short_label(self):
        return "All %dbp unique" % self.min_length
