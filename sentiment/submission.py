#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    counter = collections.Counter(x.split())
    return dict(counter)
    # END_YOUR_CODE

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, return the weight vector (sparse feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    numIters refers to a variable you need to declare. It is not passed in.
    '''
    weights = {}  # feature => weight
    numIters = 15
    # if stepSize > 0.1 it overfits
    stepSize = 0.04
    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    for i in range(0, numIters):
        totalLoss = 0
        for sample in trainExamples:
            feature = featureExtractor(sample[0])
            wphix = 0
            for key in feature:
                if key not in weights:
                    weights[key] = 0
                wphix += weights[key] * feature[key]

            #calulatedLoss = 1 - wphix * sample[1]
            loss = max(0, (1 - wphix * sample[1]))
            totalLoss += loss
            if ( loss > 0 ) :
                grad = {}
                for key in feature:
                    gradKey = feature[key] * sample[1] * -1
                    #grad[key] = gradKey
                    weights[key] -= stepSize * gradKey
        trainLoss = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        testLoss = evaluatePredictor(testExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        print "At iteration %d, loss on training is %f, loss on predictor is %f " % \
            (i, trainLoss, testLoss)
    # END_YOUR_CODE
    return weights

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        while True:
            keys = random.sample(weights.keys(), random.randint(1, len(weights)))
            phi = { k: random.random() - 0.5 for k in keys }
            y_new = dotProduct(phi, weights) 
            if y_new == 0:
                continue
            elif y_new > 0:
                y = 1
            else :
                y = -1
            break
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3f: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        trimmed = ''.join(x.split())
        weight = {}
        if ( len(trimmed) < n ) :
            return weight
        for i in range(0, len(trimmed)-n + 1):
            key = trimmed[i:i+n]
            if key not in weight:
                weight[key] = 0
            weight[key] += 1
        return weight
        # END_YOUR_CODE
    return extract

############################################################
# Problem 3h: extra credit features

def extractExtraCreditFeatures(x):
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    y = extractWordFeatures(x)
    #extractor = extractCharacterFeatures(5)
    #extractor2 = extractCharacterFeatures(8)
    #feature2 = extractor(x)
    #y = extractor2(x)
    #feature1 = y.copy()
    #feature1.update(feature2)
    for k in y:
        if y[k] > 2:
            y[k] = 2
    return y
    # END_YOUR_CODE

############################################################
# Problem 4: k-means
############################################################


def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (around 35 lines of code expected)
    def distance2(exa, exb):
        keys = set(exa.keys() + exb.keys())
        return sum([(exa[k] - exb[k])**2 for k in keys])
    def sumByKey(points):
        keys = set([k for p in points for k in p.keys() ])
        return {k: sum([p[k] for p in points]) for k in keys }

    centers = random.sample(examples, K)

    assignment = []
    # assignment step
    last_square_loss = 0
    square_loss = -1
    for counter in xrange(maxIters):
        square_loss = 0
        new_assignment = []
        for i, k in enumerate(examples):
            dist_all = [distance2(k, c) for c in centers]
            min_idx, min_dist2 = min(enumerate(dist_all), key = lambda p: p[1])
            new_assignment.append(min_idx)
            square_loss = square_loss + min_dist2
        # update step
        new_centers = []
        # TODO possible to have empty point sets?
        for c, m in enumerate(centers):
            centered_points = [examples[ex] for ex, cen in enumerate(new_assignment) if cen == c]
            sumDistance = sumByKey(centered_points)
            new_centers.append(collections.Counter({k: (v/float(len(centered_points))) for k,v in sumDistance.iteritems()}))
        centers = new_centers
        assignment = new_assignment
        print "square loss is %f at iteration %d\n " % (square_loss, counter)
        if ( counter > 0 and square_loss == last_square_loss  ):
            break
        else:
            last_square_loss = square_loss

    return centers, assignment, square_loss
    # END_YOUR_CODE
