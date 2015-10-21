import time
import submission
import util

def simulation(mdp1, feature=submission.identityFeatureExtractor):
    learning = submission.QLearningAlgorithm(mdp1.actions, 1, feature)
    rewards = util.simulate(mdp1, learning, numTrials=30000) 

    learning.explorationProb = 0
#states = mdp1.computeStates()
    vi = submission.ValueIteration()
    vi.solve(mdp1)

    total = 0
    same = 0
    for state in mdp1.states:
        print state, vi.pi[state],learning.getAction(state)
        if ( vi.pi[state] == learning.getAction(state) ):
            same += 1
        total += 1
    print "utility %.2f same action percentage is %.2f" % ( sum(rewards) / float(len(rewards)), same / float(total))

# original
mdp1 = submission.smallMDP
simulation(mdp1)
#mdp2 = submission.largeMDP
#simulation(mdp2)
mdp1 = submission.smallMDP
simulation(mdp1, submission.blackjackFeatureExtractor)
start = time.time()
#mdp2 = submission.largeMDP
#simulation(mdp2, submission.blackjackFeatureExtractor)

#vi = submission.ValueIteration()
#vi.solve(submission.largeMDP)
finish = time.time()
print finish - start
# Make sure the succAndProbReward function is implemented correctly.
#mdp1 = None
#preBustState = (6, None, (1, 1))
#postBustState = (11, None, None)
#tests = [
#    ([((1, None, (1, 2)), 0.5, 0), ((5, None, (2, 1)), 0.5, 0)], mdp1, preBustState, 'Take'),
#    ([((0, 0, (2, 2)), 0.5, -1), ((0, 1, (2, 2)), 0.5, -1)], mdp1, preBustState, 'Peek'),
#    ([((0, None, None), 1, 0)], mdp1, preBustState, 'Quit'),
#    ([((7, None, (0, 1)), 0.5, 0), ((11, None, None), 0.5, 0)], mdp1, preBustState, 'Take'),
#    ([((6, None, None), 1, 6)], mdp1, preBustState, 'Quit'),
#    ([], mdp1, (6, None, None), 'Take'),
#    ([], mdp1, (6, None, None), 'Peek'),
#    ([], mdp1, (6, None, None), 'Quit'),
#    ([], mdp1, (7, 1, (0, 1)), 'Peek'),
#    ([], mdp1, postBustState, 'Take'),
#    ([], mdp1, postBustState, 'Peek'),
#    ([], mdp1, postBustState, 'Quit'),
#]
#
#for _ in xrange(10000):
#    for gold, mdp, state, action in tests:
#        _ = submission.blackjackFeatureExtractor(state,action)
