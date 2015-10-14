import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return self.query
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        return state == ''
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        results = []
        for i in range(0, len(state)+1): 
            results.append((state[0:i], state[i:], self.unigramCost(state[0:i])))
        return results
        # END_YOUR_CODE

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_CODE (around 3 lines of code expected)
    if ( len(ucs.actions) > 0 ):
        return ' '.join(ucs.actions)
    else:
        return query
    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        if ( len(self.queryWords) > 0 ) :
            return (0,(wordsegUtil.SENTENCE_BEGIN, self.queryWords[0]))
        else:
            return (0,(wordsegUtil.SENTENCE_BEGIN,))
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        return state[0] == len(self.queryWords)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        results = []
        fills = self.possibleFills(state[1][1])
        newIndx = state[0] + 1
        if newIndx >= len(self.queryWords):
            nextSegment = None
        else:
            nextSegment = self.queryWords[newIndx]
        if len(fills) == 0 :
            fills.add(state[1][1])

        for f in fills:
            filledState = (newIndx, (state[1][0],f))
            results.append((f, (newIndx,(f,nextSegment)), self.bigramCost(state[1][0], f)))
        return results
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (around 3 lines of code expected)
    ucs = util.UniformCostSearch()
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))
    return ' '.join(ucs.actions)
    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        return (0, wordsegUtil.SENTENCE_BEGIN)
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        return state[0] == len(self.query)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        results = []
        indx = state[0]
        currentword = state[1]
        for i in range(indx+1, len(self.query)+1):
            pretext = self.query[indx:i]
            fills = self.possibleFills(pretext)
            for f in fills:
                results.append((f, (i, f), self.bigramCost(currentword, f)))
        return results
        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))
    if ( ucs.actions is not None ) :
        return ' '.join(ucs.actions)
    else: 
        return ''
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
