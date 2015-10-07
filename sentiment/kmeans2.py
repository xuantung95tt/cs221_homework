from util import *
import submission

examples = generateClusteringExamples(10, 4, 2)
centers, assignment, loss = submission.kmeans(examples,3, 1000)

outputClusters("./cluster.out", examples, centers, assignment)
