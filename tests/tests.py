import unittest
from countminsketch.countminsketch import CountMinSketch


class TestCountMinSketch(unittest.TestCase):

    def test_add(self):
        cms = CountMinSketch(10, 15)

        assert(cms.query('test_val') == 0)
        cms.add('test_val')
        assert(cms.query('test_val') == 1)
        cms.add('test_val')
        assert cms.query('test_val') == 2

    def test_subtract(self):
        cms = CountMinSketch(10, 12)
        assert cms.query('test_val2') == 0
        cms.subtract('test_val2')
        cms.query('test_val2') == 0
        cms.add('test_val2')
        cms.subtract('test_val2')
        cms.query('test_val2') == 0

    def test_hash_function(self):
        d = 10
        w = 1000
        cms = CountMinSketch(d, w)
        bin_indexes = cms._hash('test_val')

        assert(len(bin_indexes) == d)
        # Assert indexes are unique
        assert(len(bin_indexes) == len(set(bin_indexes)))

    def test_error(self):
        d = 10
        w = 1000
        cms = CountMinSketch(d, w)
        err1, prob1 = cms.error()

        cms = CountMinSketch(d * 10, w)
        err2, prob2 = cms.error()

        cms = CountMinSketch(d, w * 10)
        err3, prob3 = cms.error()

        assert err3 <= err1
        assert err2 <= err1

    def test_big_scale(self):
        import random
        d = 20
        w = 1000
        num_values = 30
        max_count = 1000
        min_count = 1
        data = {}
        cms = CountMinSketch(d, w)
        for i in range(num_values):
            item_count = random.randint(min_count,max_count)
            data[i] = item_count
            for _ in range(item_count):
                cms.add(i)

        errors = {}
        for item in data.keys():
            count_est, count_est_err, count_est_err_prob = cms.query(item, return_error=True)
            errors[item] = abs(count_est - data[item])/data[item] # Abs percent diff
            assert errors[item] < count_est_err



