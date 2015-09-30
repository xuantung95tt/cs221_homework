#!/usr/bin/env python

import graderUtil, collections, random

grader = graderUtil.Grader()
submission = grader.load('submission')

############################################################
# Problems 1 and 2

grader.addBasicPart('writeupValid', lambda : grader.requireIsValidPdf('writeup.pdf'))


############################################################
# Problem 3a: computeMaxWordLength

grader.addBasicPart('3a-0', lambda :
        grader.requireIsEqual('longest', submission.computeMaxWordLength('which is the longest word')))


############################################################
# Problem 3b: manhattanDistance

grader.addBasicPart('3c-0', lambda : grader.requireIsEqual(6, submission.manhattanDistance((3, 5), (1, 9))))
grader.addBasicPart('3c-0', lambda : grader.requireIsEqual(16, submission.manhattanDistance((3, 5), (1, -9))))


############################################################
# Problem 3c: mutateSentences

def test():
    grader.requireIsEqual(sorted(['a a a a a']), sorted(submission.mutateSentences('a a a a a')))
    grader.requireIsEqual(sorted(['the cat']), sorted(submission.mutateSentences('the cat')))
    grader.requireIsEqual(sorted(['and the cat and the', 'the cat and the mouse', 'the cat and the cat', 'cat and the cat and']), sorted(submission.mutateSentences('the cat and the mouse')))
grader.addBasicPart('3b-0', test)


############################################################
# Problem 3d: dotProduct

grader.addBasicPart('3d-0', lambda : grader.requireIsEqual(15, submission.sparseVectorDotProduct(collections.Counter({'a': 5}), collections.Counter({'b': 2, 'a': 3}))))


############################################################
# Problem 3e: incrementSparseVector

def test():
    v = collections.Counter({'a': 5})
    submission.incrementSparseVector(v, 2, collections.Counter({'b': 2, 'a': 3}))
    grader.requireIsEqual(collections.Counter({'a': 11, 'b': 4}), v)
    submission.incrementSparseVector(v, 0, collections.Counter({'b': 2, 'a': 3}))
    submission.incrementSparseVector(v, -2, collections.Counter({'b': 2, 'a': 3}))
    grader.requireIsEqual(collections.Counter({'a': 5, 'b':0}), v)
grader.addBasicPart('3e-0', test)


############################################################
# Problem 3f

def test3f():
    grader.requireIsEqual((set(['the', 'fox']), 2), submission.computeMostFrequentWord('the quick brown fox jumps over the lazy fox'))
    grader.requireIsEqual([()], submission.computeMostFrequentWord(''))
grader.addBasicPart('3f-0', test3f)


############################################################
# Problem 3g

def test3g():
    # Test around bases cases
    grader.requireIsEqual(0, submission.computeLongestPalindrome(""))
    grader.requireIsEqual(1, submission.computeLongestPalindrome("a"))
    grader.requireIsEqual(2, submission.computeLongestPalindrome("aa"))
    grader.requireIsEqual(1, submission.computeLongestPalindrome("ab"))
    grader.requireIsEqual(3, submission.computeLongestPalindrome("animal"))
    grader.requireIsEqual(5, submission.computeLongestPalindrome("ababa"))
grader.addBasicPart('3g-0', test3g)


grader.grade()
