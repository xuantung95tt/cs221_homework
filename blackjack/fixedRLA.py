import util
import submission

vi = submission.ValueIteration()
vi.solve(submission.originalMDP)
fixedRLA = util.FixedRLAlgorithm(vi.pi)
rewards = util.simulate(submission.newThresholdMDP, fixedRLA, numTrials=30000) 
print "average utility " + str(sum(rewards)/float(len(rewards)))
rewards = util.simulate(submission.originalMDP, fixedRLA, numTrials=30000) 
print "average utility " + str(sum(rewards)/float(len(rewards)))

mdp2 = submission.newThresholdMDP
learning = submission.QLearningAlgorithm(mdp2.actions, 1, submission.blackjackFeatureExtractor)
rewards = util.simulate(mdp2, learning, numTrials=30000) 
print "average utility " + str(sum(rewards)/float(len(rewards)))
vi2 = submission.ValueIteration()
vi2.solve(submission.newThresholdMDP)
fixed2 = util.FixedRLAlgorithm(vi2.pi)
rewards = util.simulate(submission.newThresholdMDP, fixed2, numTrials=30000) 
print "average utility " + str(sum(rewards)/float(len(rewards)))
