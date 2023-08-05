import tqdm

import numpy as np
import scipy

from abc import ABC, abstractmethod
from sklearn import metrics, dummy

from . import helpers


class CVResults:
    '''
    This class describes the results of comparing different classifier configurations via cross-fold validation.


        If evaluating regression, it will return r2, explained variaence, and mean squared error.

        It will print out pairwise comparisons of f-measures (for classification) or r2 scores (for regression)
        achieved by the different configurations, and show whether the difference between each pair is
        statistically significant.
    '''

    def __init__(self, configs, metrics, individual_runs):
        '''


            :param configs: the different classifier configurations that were compared
            :param metrics:
            :param individual_runs:
        '''

        self.configs = configs
        self.metrics = metrics

        self.individual_runs = individual_runs

        self.scores = {}
        for config, configRuns in individual_runs.items():

            self.scores[config] = {}

            for metric, run_scores in configRuns.items():
                self.scores[config][metric] = np.mean(run_scores)

        self.pairwise_comparison_metric = self.metrics[0]
        self.pairwise_comparisons = []

        configKeys = list(self.scores.keys())

        for a in range(0, len(configKeys)):

            keyA = configKeys[a]

            for b in range(a + 1, len(configKeys)):
                keyB = configKeys[b]

                t, prob = scipy.stats.ttest_rel(
                    individual_runs[keyA][self.pairwise_comparison_metric],
                    individual_runs[keyB][self.pairwise_comparison_metric]
                )

                self.pairwise_comparisons.append({
                    "a": keyA,
                    "b": keyB,
                    "t-statistic": t,
                    "prob": prob
                })

class Results:

    def __init__(self, configs, metrics, scores):

        self.configs = configs
        self.metrics = metrics

        self.scores = scores


class Evaluator(ABC):
    """
    This provides a tool to evaluate and compare different configurations of your classification algorithm.
    """

    @abstractmethod
    def initialize_algorithm(self, config):
        """
        Initializes an algorithm (which must extend ConfigurableAlgorithm) with the given configuration

        :param config: a configuration for the algorithm
        :return the initialized, configured algorithm
        """

        pass

    def __init__(self, items, labels=None, scores=None, scorers=None, scorer_config=None, dummy_strategy='uniform', random_runs=None):
        """
        Initializes the evaluator, with the given dataset of items and labels

        :param items: an array of items
        :param labels: an array of ground-truth labels, to be specified if you are performing classification
        :param scores: an array of ground-truth scores, to be specified if you are performing regression
        :param scorers: an array of scorers (i.e. names of functions under sklearn.metrics). If performing classification, this defaults to ['f1_score','recall_score','precision_score']. If performing regression, it defaults to ['r2_score', 'explained_variance_score', 'mean_absolute_error']. re.
        :param scorer_config: a dictionary of additional parameters used to configure the scorers. If performing multiclass classification, this defaults to {'average': 'macro'}. Otherwise it defaults to an empty dictionary.
        :param dummy_strategy: the strategy used for the random baseline. Defaults to 'uniform'
        :param random_runs: the number of times to run the random baseline to average out results. Defaults to 100
        """

        self.dataset = helpers.Dataset(items, labels, scores)
        self.dummy_strategy = dummy_strategy

        if scorers is None:
            if self.dataset.for_classification():
                self.scorers = ['f1_score', 'recall_score', 'precision_score']
            else:
                self.scorers = ['r2_score', 'explained_variance_score', 'mean_absolute_error']
        else:
            self.scorers = scorers

        if scorer_config is None:
            if self.dataset.for_classification() and not self.dataset.is_binary():
                self.scorer_config = {'average': 'macro'}
            else:
                self.scorer_config = {}
        else:
            self.scorer_config = scorer_config

        if random_runs is None:
            self.random_runs = 100
        else:
            self.random_runs = random_runs


    def evaluate(self, configs, runs=10, folds=10):
        """
        Evaluates and compares the given list of classifier or regressor configs.

        This will return a CVResults object describing the performance of all the different configurations across the different runs.

        :param configs: a list of algorithm configurations
        :param runs: the number of seperate runs to perform (defaults to 10)
        :param folds: the number of folds to split the data into during each run (defaults to 10)
        """

        results = self.__calculateResults(configs, runs, folds)

        return CVResults(configs, self.scorers, results)


    def evaluate_with_testset(self, configs, items, labels=None, scores=None):
        """
        Evaluates and compares the given list of classifier or regressor configs, using the given seperate test set.

        This will return a Results object describint the performance of all the different configurations on the test set.


        :param configs: a list of algorithm configurations
        :param items: the test set items
        :param labels: the test set labels, if performing classification
        :param scores: the test set scores, if performing regression
        """

        results = self.__calculateResultsWithTestSet(configs, items, labels, scores)

        return Results(configs, self.scorers, results)

    def __calculateResultsWithTestSet(self, configs, items, labels=None, scores=None):

        dataset = helpers.Dataset(items, labels, scores)

        configKeys = self.__getKeys(configs)

        predByKey = {}
        gold = None

        if self.dataset.type == 'c':
            gold = dataset.labels
        else:
            gold = dataset.scores

        for c in configs:
            alg = self.initialize_algorithm(c)

            if self.dataset.type == 'c':
                alg.fit(self.dataset.items, self.dataset.labels)
            else:
                alg.fit(self.dataset.items, self.dataset.scores)

            cId = c.get('id', 'unknown')
            predByKey[cId] = alg.predict(items)

        results = {}
        for key in configKeys:
            results[key] = {}
            for scorer in self.scorers:
                results[key][scorer] = helpers.get_score(gold, predByKey[key], scorer, self.scorer_config)

        if self.random_runs > 0:
            random_results = {}
            for i in range(0,self.random_runs):
                r_pred = None
                if self.dataset.type == 'c':
                    r_pred = self.__pred_randomly(self.dataset.items, self.dataset.labels, dataset.items)
                else:
                    r_pred = self.__pred_randomly(self.dataset.items, self.dataset.scores, dataset.items)

                for scorer in self.scorers:
                    r_score = helpers.get_score(gold, r_pred, scorer, self.scorer_config)
                    if scorer in random_results:
                        random_results[scorer].append(r_score)
                    else:
                        random_results[scorer] = [r_score]

            results['random'] = {}
            for scorer in self.scorers:
                results['random'][scorer] = np.mean(random_results[scorer])

        return results

    def __calculateResults(self, configs, n_runs, n_folds):

        configKeys = self.__getKeys(configs)

        results = {}
        for key in configKeys:
            results[key] = {}
            for scorer in self.scorers:
                results[key][scorer] = []


        # do n_runs of cross-fold validation, since each time we do it we get slightly different results
        with tqdm.tqdm_notebook(total=n_runs * n_folds * len(configs)) as progress:
            for run in range(0, n_runs):

                folds = self.dataset.build_folds(n_folds)

                gold = []

                predByKey = {}
                for key in configKeys:
                    predByKey[key] = []

                random_preds = []
                for i in range(0, self.random_runs):
                    random_preds.append([])

                for train_index, test_index in folds:

                    X_train, X_test = self.dataset.items[train_index], self.dataset.items[test_index]

                    if self.dataset.type == 'c':
                        y_train, y_test = self.dataset.labels[train_index], self.dataset.labels[test_index]
                    else:
                        y_train, y_test = self.dataset.scores[train_index], self.dataset.scores[test_index]

                    gold = np.concatenate((gold, y_test))

                    for c in configs:
                        alg = self.initialize_algorithm(c)
                        alg.fit(X_train, y_train)

                        pred = alg.predict(X_test)

                        cId = c.get('id', 'unknown')
                        predByKey[cId] = np.concatenate((predByKey[cId], pred))
                        progress.update(1)

                    for i in range(0, self.random_runs):
                        random_preds[i] = np.concatenate((random_preds[i], self.__pred_randomly(X_train, y_train, X_test)))

                for key in configKeys:
                    if key == 'random':
                        continue

                    for scorer in self.scorers:
                        results[key][scorer].append(helpers.get_score(gold, predByKey[key], scorer, self.scorer_config))

                if self.random_runs > 0:

                    for scorer in self.scorers:
                        scores = []
                        for random_pred in random_preds:
                            scores.append(helpers.get_score(gold, random_pred, scorer, self.scorer_config))

                        results['random'][scorer].append(np.mean(scores))

        return results

    def __pred_randomly(self, X_train, y_train, X_test):

        dummyX_train = [[0] for x in X_train]
        dummyX_test = [[0] for x in X_test]

        clf = None

        if self.dataset.type == 'c':
            clf = dummy.DummyClassifier(strategy=self.dummy_strategy)
        else:
            clf = dummy.DummyRegressor()

        clf.fit(dummyX_train, y_train)

        pred = clf.predict(dummyX_test)

        return pred



    def __getKeys(self, configs):

        keys = []
        uniq = set()
        for c in configs:
            keys.append(c.get('id', 'unknown'))
            uniq.add(c.get('id', 'unknown'))

        if self.random_runs > 0:
            keys.append('random')
            uniq.add('random')

        if len(keys) > len(uniq):
            raise ValueError('configurations must have unique ids')

        return keys

