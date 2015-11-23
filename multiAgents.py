#-*- coding: utf-8 -*-

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide. You are welcome to change
      it in any way you see fit, so long as you don't touch the method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos             = successorGameState.getPacmanPosition()
        newFood            = successorGameState.getFood()
        newGhostStates     = successorGameState.getGhostStates()
        newScaredTimes     = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """
        här är skitkoden som funkar dåligt.

        import sys
        from searchAgents import manhattan_distance

        score = successorGameState.getScore()

        # gd = närmaste spöke
        gd = sys.maxint
        for ghost_state in newGhostStates:
            gd = min(gd, manhattan_distance(ghost_state.getPosition(), newPos))

        # nf = närmaste mat
        nf = sys.maxint
        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]: nf = min(nf, manhattan_distance(newPos, (x,y)))

        if gd == sys.maxint: gd = 0
        if nf == sys.maxint: nf = 0

        score += 10.0/(nf+1)**0.25
        score += 10*gd**0.5*0.07
        """

        from searchAgents import manhattan_distance

        import sys

        ghost_distance = sys.maxint
        for ghost_state in newGhostStates:
            dist = manhattan_distance(ghost_state.getPosition(), newPos)
            ghost_distance = min(ghost_distance, dist)

        food_distance = sys.maxint
        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]:
                    dist = manhattan_distance(newPos, (x,y))
                    food_distance = min(food_distance, dist)

        score = successorGameState.getScore()

        if ghost_distance == sys.maxint: ghost_distance = 0
        if food_distance  == sys.maxint: food_distance  = 0

        if ghost_distance < 6:
            score -= 100.0 / (ghost_distance+1)

        score += 1.0 / (food_distance+1)

        return score

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
      add functionality to all your adversarial search agents. Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended. Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent
    """

    def assvalue(self, state, n):
        if n >= self.depth:
            return state.getScore()

        if self.index == 0:
            return self.max_value(state, n+1)

        return self.min_value(state, n+1)

    def max_value(self, state, n):
        v = -9999999
        for action in state.getLegalActions(self.index):
            s = state.generateSuccessor(self.index, action)
            v = max(v, self.assvalue(state, n+1))
        return v

    def min_value(self, state, n):
        v = 9999999
        for action in state.getLegalActions(self.index):
            s = state.generateSuccessor(self.index, action)
            v = min(v, self.assvalue(state, n+1))
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        print self.index
        if self.index == 0:
            qk = -999999
            best_action = None
            for action in gameState.getLegalActions(self.index):
                av = self.assvalue(gameState, 0)
                print av
                print action
                if av > qk:
                    qk = av
                    best_action = action
            print best_action
            return best_action
        else:
            qk = 999999
            best_action = None
            for action in gameState.getLegalActions(self.index):
                av = self.assvalue(gameState, 0)
                if av < qk:
                    qk = av
                    best_action = action
            return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

