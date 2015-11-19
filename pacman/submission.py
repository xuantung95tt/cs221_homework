from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument 
    is an object of GameState class. Following are a few of the helper methods that you 
    can use to query a GameState object to gather information about the present state 
    of Pac-Man, the ghosts and the maze.
    
    gameState.getLegalActions(): 
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action): 
        Returns the successor state after the specified agent takes the action. 
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game

    
    The GameState class is defined in pacman.py and you might want to look into that for 
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best




    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following: 
      pacman won, pacman lost or there are no legal moves. 

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game
    
      gameState.isWin():
        Returns True if it's a winning state
    
      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue

    """

    # BEGIN_YOUR_CODE (around 30 lines of code expected)
    def getScore(state, agentIndex, d):
        legalActions = state.getLegalActions(agentIndex)
        random.shuffle(legalActions)
        if d == 0:
            return [self.evaluationFunction(state), None]
        elif state.isWin() or state.isLose() or len(legalActions) == 0:
            return [state.getScore(), None]
        else:
            if agentIndex == state.getNumAgents() - 1:
                nextAgent = 0
                depth = d -1
            else:
                nextAgent = agentIndex +1
                depth = d
            nextScores = [getScore(state.generateSuccessor(agentIndex,action), nextAgent, depth)[0] for action in legalActions]
            if agentIndex == 0:
                max_index, max_value = max(enumerate(nextScores), key= lambda p: p[1])
                return [max_value, legalActions[max_index]]
            else:
                min_index, min_value = min(enumerate(nextScores), key= lambda p: p[1])
                return [min_value, legalActions[min_index]]

    score, action = getScore(gameState, self.index, self.depth)
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (around 50 lines of code expected)
    def getScore(state, agentIndex, d, alpha, beta):
        legalActions = state.getLegalActions(agentIndex)
        random.shuffle(legalActions)
        if d == 0:
            return [self.evaluationFunction(state), None]
        elif state.isWin() or state.isLose() or len(legalActions) == 0:
            return [state.getScore(), None]
        else:
            if agentIndex == state.getNumAgents() - 1:
                nextAgent = 0
                depth = d -1
            else:
                nextAgent = agentIndex +1
                depth = d
            if agentIndex == 0:
                v = float("-inf")
                action = None
                scores = []
                for act in legalActions:
                    score = getScore(state.generateSuccessor(agentIndex,act), nextAgent, depth, alpha, beta)
                    if ( score[0] > v ):
                        action = act
                        v = score[0]
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break
                return [v, action]
            else:
                v = float("+inf")
                action = None
                for act in legalActions:
                    score = getScore(state.generateSuccessor(agentIndex,act), nextAgent, depth, alpha, beta)
                    if ( score[0] < v ):
                        action = act
                        v = score[0]
                    beta = min(beta, v)
                    if beta <= alpha:
                        break
                return [v,action]

    score, action = getScore(gameState, self.index, self.depth, float("-inf"), float("+inf"))
    return action
    
    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (around 25 lines of code expected)
    def getScore(state, agentIndex, d):
        legalActions = state.getLegalActions(agentIndex)
        random.shuffle(legalActions)
        if d == 0:
            return [self.evaluationFunction(state), None]
        elif state.isWin() or state.isLose() or len(legalActions) == 0:
            return [state.getScore(), None]
        else:
            if agentIndex == state.getNumAgents() - 1:
                nextAgent = 0
                depth = d -1
            else:
                nextAgent = agentIndex +1
                depth = d
            nextScores = [getScore(state.generateSuccessor(agentIndex,action), nextAgent, depth)[0] for action in legalActions]
            if agentIndex == 0:
                max_index, max_value = max(enumerate(nextScores), key= lambda p: p[1])
                return [max_value, legalActions[max_index]]
                #maxv = max(nextScores)
                #choices = [[v, legalActions[i]] for i, v in enumerate(nextScores) if v == maxv]
                #return random.choice(choices)
            else:
                action = random.choice(legalActions) 
                #min_index, min_value = min(enumerate(nextScores), key= lambda p: p[1])
                return [sum(nextScores)/float(len(legalActions)) , action]
    score, action = getScore(gameState, self.index, self.depth)
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
  """

  # BEGIN_YOUR_CODE (around 30 lines of code expected)
  # need to eat agent
  # need to go for food
  score = currentGameState.getScore()
  foodRadius = 10
  pacPos = currentGameState.getPacmanPosition() 
  foodGrid = currentGameState.getFood()
  foodScore = 0
  wallScore = 0
  for x in range( max(0, pacPos[0] - foodRadius), min( foodGrid.width, pacPos[0] + foodRadius)):
      for y in range( max(0, pacPos[1] - foodRadius), min(foodGrid.height, pacPos[1] + foodRadius ) ):
          if ( currentGameState.hasFood(x,y) ):
              distance = abs(x-pacPos[0]) + abs(y-pacPos[1])
              foodScore += 10 / pow(2, distance)
          elif ( currentGameState.hasWall(x,y) ):
              wallScore += 1
  
  ghostStates = currentGameState.getGhostStates()
  ghostScore = 0
  ghostPositions = currentGameState.getGhostPositions()
  hasScared = False
  for i, ghost in enumerate(ghostStates):
      pos = ghostPositions[i]
      distance = abs(pos[0] - pacPos[0]) + abs(pos[1] - pacPos[1])
      if distance == 0:
          ghostScore -= 1000
      elif ghost.scaredTimer > 0:
          hasScared = True
          ghostScore += 100 / distance
      else:
          ghostScore -= 20 / distance

  capsuleScore = 0
  if False and not hasScared:
      for pos in currentGameState.getCapsules():
          distance = abs(pos[0] - pacPos[0]) + abs(pos[1] - pacPos[1])
          capsuleScore += 10 / distance
  return score + foodScore + ghostScore + capsuleScore

  
  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction


