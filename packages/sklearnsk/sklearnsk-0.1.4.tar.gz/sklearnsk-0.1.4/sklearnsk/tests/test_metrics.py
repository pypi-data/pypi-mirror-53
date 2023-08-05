from unittest import TestCase

from sklearnsk import helpers
from sklearn import metrics
import random

class TestMetrics(TestCase):

    def __build_random(self, length=100, classes=[0,1]):

        vals = []
        for i in range(0,length):
            vals.append(random.choice(classes))

        print(vals)
        return vals


    def test_recall(self):

        # test binary
        for i in range(0,10):

            gold = self.__build_random()
            pred = self.__build_random()


            direct = metrics.recall_score(gold, pred)
            indirect = helpers.get_score(gold, pred, 'recall_score')

            self.assertEqual(direct, indirect)

        # test multiclass

        for i in range(0,10):

            gold = self.__build_random(classes=['green','amber','red','crisis'])
            pred = self.__build_random(classes=['green','amber','red','crisis'])

            direct = metrics.recall_score(gold, pred, average='macro')
            indirect = helpers.get_score(gold, pred, 'recall_score', {'average':'macro'})

            self.assertEqual(direct, indirect)

        assert (direct == indirect)

    def test_precision(self):

        # test binary
        for i in range(0, 10):
            gold = self.__build_random()
            pred = self.__build_random()

            direct = metrics.precision_score(gold, pred)
            indirect = helpers.get_score(gold, pred, 'precision_score')

            self.assertEqual(direct, indirect)

        # test multiclass

        for i in range(0, 10):
            gold = self.__build_random(classes=['green', 'amber', 'red', 'crisis'])
            pred = self.__build_random(classes=['green', 'amber', 'red', 'crisis'])

            direct = metrics.precision_score(gold, pred, average='macro')
            indirect = helpers.get_score(gold, pred, 'precision_score', {'average': 'macro'})

            self.assertEqual(direct, indirect)

        assert (direct == indirect)

    def test_f1_score(self):

        # test binary
        for i in range(0, 10):
            gold = self.__build_random()
            pred = self.__build_random()

            direct = metrics.f1_score(gold, pred)
            indirect = helpers.get_score(gold, pred, 'f1_score')

            self.assertEqual(direct, indirect)

        # test multiclass

        for i in range(0, 10):
            gold = self.__build_random(classes=['green', 'amber', 'red', 'crisis'])
            pred = self.__build_random(classes=['green', 'amber', 'red', 'crisis'])

            direct = metrics.f1_score(gold, pred, average='macro')
            indirect = helpers.get_score(gold, pred, 'f1_score', {'average': 'macro'})

            self.assertEqual(direct, indirect)

        assert (direct == indirect)


