"""Define MutationSpace"""

import itertools
import numpy as np
from .biotools import windows_overlap

# TODO: better in-code docs


class MutationChoice:
    """Represent a segment of a sequence with several possible variants.

    Parameters
    ----------

    segment
      A pair (start, end) indicating the range of nucleotides concerned. We
      are applying Python range, so

    variants
      A set of sequence variants, at the given position

    Examples
    --------

    >>> choice = MutationChoice((70, 73), {})


    """

    __slots__ = ["segment", "start", "end", "variants", "is_any_nucleotide"]

    def __init__(self, segment, variants, is_any_nucleotide=False):
        if isinstance(segment, int):
            segment = (segment, segment + 1)
        self.segment = segment
        self.start, self.end = segment
        self.variants = variants
        self.is_any_nucleotide = is_any_nucleotide
        # self.possible_subsequences = set(m.subsequence for m in mutations)

    def random_variant(self, sequence):
        """Return one of the variants, randomly."""
        subsequence = sequence[self.start : self.end]
        variants = [v for v in self.variants if v != subsequence]
        # the sorting of variants seems essential to ensure reproducibility
        # between sessions.
        # it does not slow down the global algorithm (or less than 3%)
        variants = sorted(variants)
        return variants[np.random.randint(len(variants))]

    def merge_with(self, others):
        """Merge this mutation choice with others to form a single choice

        Examples:
        ---------

        >>> ((2, 5), {'ATT', 'ATA'})

       percolated with:

        >>> [
        >>>     ((0, 3), {'GTA', 'GCT', 'GTT'}),
        >>>     ((3, 4), {'A', 'T', 'G', 'C'}),
        >>>     ((4, 7), {'ATG', 'ACC', 'CTG'})
        >>> ]

        returns the only choices on the full interval which are compatible with
        at least one choice in each of the MutationChoices
        >>> (0, 7), {'GTATACC', 'GTATATG'}

        """
        others = sorted(others, key=lambda o: o.start)
        others_start = others[0].start
        final_segment = others_start, others[-1].end
        final_variants = set()
        for candidate in self.variants:
            slots = []
            for other in others:
                istart, iend = windows_overlap(other.segment, self.segment)
                slot = []
                for variant in other.variants:
                    subseq = variant[istart - other.start : iend - other.start]
                    subcandidate = candidate[
                        istart - self.start : iend - self.start
                    ]
                    if subseq == subcandidate:
                        slot.append(variant)
                slots.append(slot)
            for subseqs in itertools.product(*slots):
                seq = "".join(subseqs)
                matching_seq = seq[
                    self.start - others_start : self.end - others_start
                ]
                if matching_seq == candidate:
                    final_variants.add(seq)
        return MutationChoice(segment=final_segment, variants=final_variants)

    def extract_varying_region(self):
        """Return MutationChoices for the central varying region and 2 flanks.

        For instance:

        >>> choice = MutationChoice((5, 12), [
        >>>     'ATGCGTG',
        >>>     'AAAAATG',
        >>>     'AAATGTG',
        >>>     'ATGAATG',
        >>> ])
        >>> choice.extract_varying_region()

        Result :

        >>> [
        >>>     MutChoice(5-6 A),
        >>>     MutChoice(6-10 TGCG-AATG-TGAA-AAAA),
        >>>     MutChoice(10-12 TG)
        >>> ]

        """

        if len(self.variants) <= 1:
            return [self]
        variants = list(self.variants)
        reference = variants[0]
        start = -1
        end = len(reference)
        for i in range(len(reference)):
            for variant in variants[1:]:
                if variant[i] != reference[i]:
                    if start == -1:
                        start = i
                    end = i + 1
                    break
        result = []
        if start > 0:
            result.append(
                MutationChoice(
                    (self.start, self.start + start), set([reference[:start]])
                )
            )
        result.append(
            MutationChoice(
                (self.start + start, self.start + end),
                set([v[start:end] for v in variants]),
            )
        )
        if end < len(reference):
            result.append(
                MutationChoice(
                    (self.start + end, self.end),
                    set([v[end:] for v in variants]),
                )
            )
        return result

    def __repr__(self):
        """Represent."""
        subsequences = "-".join(self.variants)
        return "MutChoice(%d-%d %s)" % (self.start, self.end, subsequences)

    def __str__(self):
        """Represent."""
        subsequences = "-".join(self.variants)
        return "MutChoice(%d-%d %s)" % (self.start, self.end, subsequences)


class MutationSpace:
    """Class for mutation space (set of sequence segments and their variants).

    Parameters
    ----------

    choices_index
      A list L such that L[i] gives the MutationChoice governing the mutations
      allowed at position i (ansd possibly around i)


    Examples
    --------

    >>> # BEWARE: below, similar mutation choices are actually the SAME OBJECT
    >>> space = MutationSpace([
            MutationChoice((0, 2), {'AT', 'TG'}),
            MutationChoice((0, 2), {'AT', 'TG'}),
            MutationChoice((2, 5), {'TTC', 'TTA', 'TTT'}), # same
            MutationChoice((2, 5), {'TTC', 'TTA', 'TTT'}), #
            MutationChoice((2, 5), {'TTC', 'TTA', 'TTT'}),
        ])
    """

    def __init__(self, choices_index, left_padding=0):
        """

        choices_index = [MutationChoice(0-2), MutationChoice(0-2),
                         MutationChoice(3-5), MutationChoice(3-5),
                         MutationChoice(3-5), ... ]
        """
        self.choices_index = left_padding * [None] + choices_index
        self.choices_list = []
        self.unsolvable_segments = []
        self.determined_segments = []
        self.multichoices = []
        for c in choices_index:
            if c is None:
                continue
            if len(self.choices_list) == 0 or (c != self.choices_list[-1]):
                self.choices_list.append(c)
                nvariants = len(c.variants)
                if nvariants == 0:
                    self.unsolvable_segments.append(c.segment)
                elif nvariants == 1:
                    self.determined_segments.append(
                        (c.segment, list(c.variants)[0])
                    )
                else:
                    self.multichoices.append(c)

    @property
    def choices_span(self):
        """Return (start, end), segment where mutiple choices are possible"""
        if self.multichoices == []:
            return None
        return self.multichoices[0].start, self.multichoices[-1].end

    def constrain_sequence(self, sequence):
        """Return a version of the sequence compatible with the mutation space.

        All nucleotides of the sequence that are incompatible with the
        mutation space are replaced by nucleotides compatible with the space.
        """
        new_sequence = bytearray(sequence.encode())
        for choice in self.choices_list:
            variants = choice.variants
            if len(choice.variants) == 0:
                raise ValueError(
                    "Cannot constrain a sequence when some "
                    "positions are unsolvable, in location "
                    "(%d-%d)" % (choice.start, choice.end)
                )
            elif len(variants) == 1:
                variant = list(variants)[0]
                new_sequence[choice.start : choice.end] = variant.encode()
            elif sequence[choice.start : choice.end] not in variants:
                variant = list(variants)[0]
                new_sequence[choice.start : choice.end] = variant.encode()
        return new_sequence.decode()

    def localized(self, location):
        """Return a new version with only mutations overlaping the location."""
        if hasattr(location, "start"):
            start, end = location.start, location.end
        else:
            start, end = location
        return MutationSpace(self.choices_index[start:end], left_padding=start)

    @property
    def space_size(self):
        """Return the number of possible mutations"""
        if len(self.multichoices) == 0:
            return 0
        return np.prod(
            [1.0] + [len(choice.variants) for choice in self.multichoices]
        )

    def pick_random_mutations(self, n_mutations, sequence):
        """Draw N random mutations"""
        n_mutations = min(len(self.multichoices), n_mutations)
        if n_mutations == 1:
            index = np.random.randint(len(self.multichoices))
            choice = self.multichoices[index]
            return [(choice.segment, choice.random_variant(sequence=sequence))]

        return [
            (choice_.segment, choice_.random_variant(sequence=sequence))
            for choice_ in [
                self.multichoices[i]
                for i in np.random.choice(
                    len(self.multichoices), n_mutations, replace=False
                )
            ]
        ]

    def apply_random_mutations(self, n_mutations, sequence):
        """Return a sequence with n random mutations applied."""
        new_sequence = bytearray(sequence.encode())
        for segment, seq in self.pick_random_mutations(n_mutations, sequence):
            start, end = segment
            new_sequence[start:end] = seq.encode()
        return new_sequence.decode()

    def all_variants(self, sequence):
        """Iterate through all sequence variants in this mutation space."""
        new_sequence = bytearray(sequence.encode())
        choice_start, choice_end = self.choices_span
        encoded_segment = sequence[choice_start:choice_end].encode()

        def sort_variants_by_distance_to_current(choice):
            """This function iterates through the variants of a given choice
            using not the alphabetical (which would bias AC over GT) but rather
            a kind of 'least-change' order, which biases towards solutions
            close to the current sequence.

            Impact on overall algorithm speed is < 0.5%"""
            current = sequence[choice.segment[0] : choice.segment[1]]
            alphasort = {v: i for i, v in enumerate(sorted(choice.variants))}

            def sort_key(v):
                return (abs(alphasort[v] - alphasort[current]), v)

            return sorted(choice.variants, key=sort_key)

        variants_slots = [
            [
                (choice_.segment, v.encode())
                for v in sort_variants_by_distance_to_current(choice_)
            ]
            for choice_ in self.multichoices
        ]
        for variants in itertools.product(*variants_slots):
            new_sequence[choice_start:choice_end] = encoded_segment
            for ((start, end), variant) in variants:
                new_sequence[start:end] = variant
            yield new_sequence.decode()

    @staticmethod
    def from_optimization_problem(problem, new_constraints=None):
        """Create a mutation space from a DNA optimization problem.

        This can be used either to initialize mutation spaces for new problems,
        or to

        """

        sequence = problem.sequence

        if new_constraints is None:
            variants = {"A": "ATGC", "T": "TACG", "G": "GCAT", "C": "CGTA"}
            choices_index = [
                MutationChoice(
                    (i, i + 1), variants=variants[c], is_any_nucleotide=True
                )
                for i, c in enumerate(sequence)
            ]
            constraints = problem.constraints
        else:
            choices_index = [c for c in problem.mutation_space.choices_index]
            constraints = new_constraints
        mutation_choices = sorted(
            [
                choice
                if isinstance(choice, MutationChoice)
                else MutationChoice(segment=choice[0], variants=set(choice[1]))
                for cst in constraints
                for choice in cst.restrict_nucleotides(sequence)
            ],
            key=lambda choice: (choice.end - choice.start, choice.start),
        )
        for choice in mutation_choices:
            underlying_choices = choices_index[choice.start : choice.end]
            if underlying_choices == []:
                new_choice = choice
            elif all(c.is_any_nucleotide for c in underlying_choices):
                new_choice = choice
            else:
                new_choice = choice.merge_with(set(underlying_choices))
            for choice in new_choice.extract_varying_region():
                if choice.end > len(choices_index):
                    choices_index += (choice.end - len(choices_index)) * [None]
                for i in range(choice.start, choice.end):
                    choices_index[i] = choice
            # for i in range(new_choice.start, new_choice.end):
            #     choices_index[i] = new_choice
        return MutationSpace(choices_index)
