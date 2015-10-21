import collections, util, math, random

############################################################
class ValueIteration(util.MDPAlgorithm):
    '''
    Solve the MDP using value iteration.  Your solve() method must set
    - self.V to the dictionary mapping states to optimal values
    - self.pi to the dictionary mapping states to an optimal action
    Note: epsilon is the error tolerance: you should stop value iteration when
    all of the values change by less than epsilon.
    The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
    '''
    def solve(self, mdp, epsilon=0.001):
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi

        V = collections.Counter()  # state -> value of state
        numIters = 0
        while True:
            newV = {}
            for state in mdp.states:
                newV[state] = max(computeQ(mdp, V, state, action) for action in mdp.actions(state))
            numIters += 1
            if max(abs(V[state] - newV[state]) for state in mdp.states) < epsilon:
                V = newV
                break
            V = newV
            #print V, newV

        # Compute the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        print "ValueIteration: %d iterations" % numIters
        self.pi = pi
        self.V = V

############################################################
# Problem 2a

# If you decide 2a is true, prove it in writeup.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    def startState(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return (0)
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return ['jump']
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return [(0, 0.25, 10), (1, 0.25,0), (2, 0.5, 0)] 
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return 0
        # END_YOUR_CODE


class CounterexampleMDP2(util.MDP):
    def startState(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return (0)
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return ['jump']
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return [(0, 0.375, 10), (1, 0.375,0), (2, 0.25, 0)] 
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        return 0

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 55 lines of code expected)
        if state[2] is None:
            return []
        elif action == 'Quit':
            if ( state[0] > self.threshold ):
                return [((state[0], None, None), 1, 0)]
            else:
                return [((state[0], None, None), 1, state[0])]
        elif action == 'Take':
            if ( state[1] is not None ) :
                sumState = state[0] + self.cardValues[state[1]]
                if sumState > self.threshold :
                    return []
                else:
                    deck = list(state[2])
                    deck[state[1]] -= 1
                    deck = tuple(deck)
                    if sum(deck) == 0 :
                        deck = None
                    return [((sumState, None, deck), 1,0)]
            else:
                results = []
                rewards = []
                validActions = 0
                for m in range(len(self.cardValues)):
                    if ( state[2][m] == 0 ):
                        continue
                    value = state[0]+self.cardValues[m]
                    validActions += 1
                    reward = 0
                    if value > self.threshold:
                        deck = None
                    else:
                        deck = list(state[2])
                        deck[m] -= 1
                        deck = tuple(deck)
                        if sum(deck) == 0 :
                            deck = None
                            reward = value
                    #results.append(((value, None, deck), float(1/len(self.cardValues)), 0))
                    results.append((value, None, deck))
                    rewards.append(reward)
                return [ (r, 1/float(validActions),rewards[i]) for i,r in enumerate(results)]
        elif action == 'Peek':
            if ( state[1] is not None):
                return []
            else:
                results = []
                validActions = 0
                results = [ (state[0], m, state[2]) for m in range(len(self.cardValues)) if state[2][m] > 0]
                #for m in range(len(self.cardValues)):
                #    if ( state[2][m] > 0 ):
                #        validActions += 1
                #        results.append((state[0], m, state[2]))
                return [ (r, 1/float(len(results)), -1 * self.peekCost) for r in results]
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (around 2 lines of code expected)
    return BlackjackMDP(cardValues=[15,4,6], multiplicity=2,
                                   threshold=20, peekCost=1)
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = collections.Counter()
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        #print state
        if ( newState is None ) :
            Vopt = 0
        else:
            Vopt = max(self.getQ(newState, newAction) for newAction in self.actions(newState))
        Qopt = self.getQ(state,action)
        for key, v in self.featureExtractor(state,action):
            self.weights[key] = self.weights[key] - self.getStepSize() * (Qopt - reward - self.discount * Vopt)*v
        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning

# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (around 10 lines of code expected)
    if counts is not None:
        features = [None, None]
    else:
        features = [None]
    app = features.append
    ext = features.extend
    features[0] = ((total,action), 1)
    if counts is not None:
        features[1] = ((tuple([int(bool(k)) for k in counts]), action), 1)
        ext([(("deck_" + str(i),k, action), 1) for i,k in enumerate(counts)])
    return features
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!
# objective function is minimizating Qopt and r + discount * Vopt
# what is the relationship between reward/utility and the capability to reproduce the optimal value through value iteration
# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)
