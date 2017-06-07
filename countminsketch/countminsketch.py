"""


"""

import hashlib
import math


class CountMinSketch:

    """
    CountMinSketch is a algorithm used to count elements in a stream. It will track the number of times
    unique elements have been seen and provided a probabalistic return count when asked.
    """

    def __init__(self, d, w):
        """
        Create a hash table of `w` columns and `d` rows.
        `w` controls the number of hash bins (less collisions)
        `d` controls the number of unique hashes
        """

        self.w = w
        self.d = d
        self.N = 0

        self.table = [[0 for _ in range(w)] for _ in range(d)]

        self.eta = math.e / self.w
        self.delta = 1 / math.exp(self.d)

    def _hash(self, x):
        """
        Hash the input `d` different times and return the values binned to `w` values
        :param x: element to hash
        :return: list of `d` bins bounded (0, w]
        """
        m = hashlib.md5()
        bin_index = []
        for i in range(self.d):
            m.update(str(x).encode('utf-8'))
            bin_index.append(int(m.hexdigest(), 16) % self.w)

        return bin_index

    def query(self, x, return_error=False):
        """
        Find the count estimate for `x`. If `return_error` is true, return the estimate,
        the estimate+error and the probability of exceeding that value.
        :param x:
        :param return_error: Default False to not return error
        :return: count estimate, [count+error, probability of error]
        """

        counts = []
        bin_indexes = self._hash(x)
        for i, k in zip(range(self.d), bin_indexes):
            counts.append(self.table[i][k])

        if not return_error:
            return min(counts)
        else:
            err, prob = self.error()
            return min(counts), min(counts) + err, prob

    def _summation(self, x, weight=1, increment=True):
        """
        Add or subtract elements from the data structure.
        :param increment: add to the count (True), or subtract from the count (False)
        :param x: element to increment/decrement
        """

        bin_indexes = self._hash(x)
        for i, k in zip(range(self.d), bin_indexes):
            if increment:
                self.table[i][k] += weight
            else:
                if self.table[i][k] <= weight:
                    self.table[i][k] = 0
                else:
                    self.table[i][k] -= weight

    def add(self, x, weight=1):
        """

        :return:
        """
        self.N += weight
        self._summation(x, weight=weight, increment=True)

        return None

    def subtract(self, x, weight=1):
        """

        :return:
        """

        self.N -= weight
        self._summation(x, weight=weight, increment=False)

    def error(self):
        """
        Return the error in estimate and the probability of error
        :return: (estimate error, probability of error)
        """

        return self.eta*self.N, (1 - self.delta)

    def __len__(self):
        """
        Return the number of elements that have been added to the sketch
        """
        return self.N
