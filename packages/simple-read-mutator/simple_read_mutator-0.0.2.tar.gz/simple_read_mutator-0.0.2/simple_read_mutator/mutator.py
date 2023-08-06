import logging
import numpy as np
from numpy.random import random
import math


class Mutator:
    def __init__(self, sequence_length=150):
        self.length = sequence_length
        self.random_bases = [
            np.array(list("ACGT" * math.ceil(self.length / 4)))[0:self.length],
            np.array(list("CGTA" * math.ceil(self.length / 4)))[0:self.length],
            np.array(list("GTAC" * math.ceil(self.length / 4)))[0:self.length],
        ]

    def mutate_sequence(self, sequence, snv_prob=0.01, deletion_prob=0.01, insertion_prob=0.01):

        snv_prob = snv_prob * 1.25  # Adjust up, since 1/4 of substitutions will be to same letter

        sequence = np.array(list(sequence), dtype='U3')
        # SNVs
        snv_locations = random(self.length) <= snv_prob
        sequence[snv_locations] = self.random_bases[np.random.randint(0, 3)][snv_locations]

        # Deletions
        deletion_locations = random(self.length) <= deletion_prob
        sequence[deletion_locations] = ""

        # Insertions
        insertion_locations = random(self.length) <= insertion_prob
        insertions = self.random_bases[np.random.randint(0, 3)][insertion_locations]
        replacements = np.core.defchararray.add(sequence[insertion_locations], insertions)
        sequence[insertion_locations] = replacements
        return ''.join(sequence)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s, %(levelname)s: %(message)s")
    mutator = Mutator(150)
    for i in range(100000):
        if i % 10000 == 0:
            logging.info("%d processed" % i)
        orig_sequence = "A" * 150
        mutated_seq = mutator.mutate_sequence(orig_sequence)
