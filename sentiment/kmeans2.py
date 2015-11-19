from util import *
import submission
import time

#examples = generateClusteringExamples(10, 4, 2)
#centers, assignment, loss = submission.kmeans(examples,3, 1000)
#
#outputClusters("./cluster.out", examples, centers, assignment)

st = time.time()
examples = generateClusteringExamples(numExamples=100000, numWordsPerTopic=3, numFillerWords=1)
submission.kmeans(examples, 3, 100)
print "kmeans took {:.1f} seconds to execute".format(time.time() - st)
