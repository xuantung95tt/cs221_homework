#!/usr/bin/python

import graderUtil
import util
import time
from util import *
import submission

trainExamples = readExamples('polarity.train')
devExamples = readExamples('polarity.dev')
#featureExtractor = submission.extractCharacterFeatures(5)
featureExtractor = submission.extractExtraCreditFeatures
#featureExtractor = submission.extractWordFeatures
weights = submission.learnPredictor(trainExamples, devExamples, featureExtractor)
outputWeights(weights, 'weights')
outputErrorAnalysis(devExamples, featureExtractor, weights, 'error-analysis')  # Use this to debug
trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
devError = evaluatePredictor(devExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
print "Official: train error = %s, dev error = %s" % (trainError, devError)

words_count = {}
words_unique = {}
for sample in devExamples:
    for word, count in submission.extractWordFeatures(sample[0]).iteritems():
        key = len(word)
        words_unique[word] = 1
        if key not in words_count:
            words_count[key] = 0

        words_count[key] += count

#print words_count
counter = 0
for k in weights.keys():
    if k in words_unique:
        counter += 1

print counter
print counter / float(len(weights))
#
#words_count2 = {}
#for word in words_unique.keys():
#    key = len(word)
#    if key not in words_count2:
#        words_count2[key] = 0
#
#    words_count2[key] += 1
#print words_count2
#for 
