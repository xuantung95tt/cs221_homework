import grader
import submission


#_realUnigramCost, _realBigramCost = wordsegUtil.makeLanguageModels('toy-will.txt')


def unigramCost(x):
    if x in ['and', 'two', 'three', 'word', 'words', 'there', 'the', 're' ]:
        return 1.0
    else:
        return 1000.0
def equal(a,b):
    if a != b :
        raise "bad " + a + b
equal('', submission.segmentWords('', unigramCost))
equal('word', submission.segmentWords('word', unigramCost))
equal('two words', submission.segmentWords('twowords', unigramCost))
equal('and three words', submission.segmentWords('andthreewords', unigramCost))
equal('there', submission.segmentWords('there', unigramCost))
equal('there word', submission.segmentWords('thereword', unigramCost))
equal('garbage', submission.segmentWords('garbage', unigramCost))

