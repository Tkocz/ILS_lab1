#-*- coding: utf-8 -*-

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

import sys

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

        """
        här är skitkoden som funkar dåligt.

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

        # Find the nearest ghost.
        ghost_distance = sys.maxint
        for ghost_state in newGhostStates:
            dist = manhattan_distance(ghost_state.getPosition(), newPos)
            ghost_distance = min(ghost_distance, dist)

        # Find the nearest food.
        food_distance = sys.maxint
        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]:
                    dist = manhattan_distance(newPos, (x,y))
                    food_distance = min(food_distance, dist)

        # Make sure we can handle situations without any ghosts or food.
        if ghost_distance == sys.maxint: ghost_distance = 0
        if food_distance  == sys.maxint: food_distance  = 0

        # Start with the 'default' state score.
        score = successorGameState.getScore()

        # The ghost is nearby - penalize Pacman by slapping him across the face
        # with negative points. Since our evaluation need not be continuous (ie.
        # it's ok to have abrupt changes missing derivatives), using an if-
        # statement here is a cheap way to make this evaluation function pretty
        # much unbeatable. One could also imagine some kind of polynomial
        # function mimicking the if-statement without breaking continuity.
        if ghost_distance < 6:
            score -= 100.0 / (ghost_distance+1)

        # Help Pacman detect nearby food slightly.
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

    def state_utility(self, state, index, depth):
        """
        Finds the state utility value for the specified state using the Minimax
        algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value - should always be set to zero when called
                      externally.

        :return: The maximum utility value for the specified state.
        """
        index = (index+1) % state.getNumAgents()

        if index==0: depth+=1

        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        if index == 0:
            return self.max_state_utility(state, index, depth)
        else:
            return self.min_state_utility(state, index, depth)

    def max_state_utility(self, state, index, depth):
        """
        Finds the maximum state utility for the specified state using the
        Minimax algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value.

        :return: The maximum state utility for the specified state.
        """

        max_value = -sys.maxint

        for action in state.getLegalActions(index):
            successor_state = state.generateSuccessor(index, action)
            value           = self.state_utility(successor_state, index, depth)
            max_value       = max(max_value, value)

        return max_value

    def min_state_utility(self, state, index, depth):
        """
        Finds the minimum state utility for the specified state using the
        Minimax algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value.

        :return: The minimum state utility for the specified state.
        """

        min_value = sys.maxint

        for action in state.getLegalActions(index):
            successor_state = state.generateSuccessor(index, action)
            value           = self.state_utility(successor_state, index, depth)
            min_value       = min(min_value, value)

        return min_value

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

        best_action = None
        max_utility = -sys.maxint

        # NOTE: For whatever reason, the state utility value calculated by our
        #       Minimax evaluation function for the initial state is -491.0
        #       using the following command line:
        #
        #   `pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4`
        #
        #       The assignment spec. tells us to expect the value -492.0. I have
        #       no idea why this happens. Investigate, plz!

        # Try all actions from the current game state and select the best one
        # according to minimax. This is actually a job for the max_state_utility
        # function, but having this code here lets us simplify the others a bit.
        for action in gameState.getLegalActions(0):
            next_state    = gameState.generateSuccessor(0, action)
            utility_value = self.state_utility(next_state, 0, 0)

            if utility_value > max_utility:
                max_utility = utility_value
                best_action = action

        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning
    """
    def state_utility(self, state, index, depth, max_option, min_option):
        """
        Finds the state utility value for the specified state using the Minimax
        algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value - should always be set to zero when called
                      externally.

        :return: The maximum utility value for the specified state.
        """
        index = (index+1) % state.getNumAgents()

        if index == 0: depth += 1

        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        if index == 0:
            return self.max_state_utility(state, index, depth, max_option, min_option)
        else:
            return self.min_state_utility(state, index, depth, max_option, min_option)

    def max_state_utility(self, state, index, depth, max_option, min_option):
        """
        Finds the maximum state utility for the specified state using the
        Minimax algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value.

        :return: The maximum state utility for the specified state.
        """

        max_value = -sys.maxint

        for action in state.getLegalActions(index):
            successor_state = state.generateSuccessor(index, action)
            value           = self.state_utility(successor_state, index, depth, max_option, min_option)
            max_value       = max(max_value, value)
            if max_value > min_option: return max_value
            max_option      = max(max_option, max_value)

        return max_value

    def min_state_utility(self, state, index, depth, max_option, min_option):
        """
        Finds the minimum state utility for the specified state using the
        Minimax algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value.

        :return: The minimum state utility for the specified state.
        """

        min_value = sys.maxint

        for action in state.getLegalActions(index):
            successor_state = state.generateSuccessor(index, action)
            value           = self.state_utility(successor_state, index, depth, max_option, min_option)
            min_value       = min(min_value, value)
            if min_value < max_option: return min_value
            min_option      = min(min_option, min_value)

        return min_value

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        best_action = None
        max_utility = -sys.maxint
        max_option = -sys.maxint
        min_option = sys.maxint

        # NOTE: For whatever reason, the state utility value calculated by our
        #       Minimax evaluation function for the initial state is -491.0
        #       using the following command line:
        #
        #   `pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4`
        #
        #       The assignment spec. tells us to expect the value -492.0. I have
        #       no idea why this happens. Investigate, plz!

        # Try all actions from the current game state and select the best one
        # according to minimax. This is actually a job for the max_state_utility
        # function, but having this code here lets us simplify the others a bit.

        for action in gameState.getLegalActions(0):
            next_state    = gameState.generateSuccessor(0, action)
            utility_value = self.state_utility(next_state, 0, 0, max_option, min_option)

            if utility_value > max_utility:
                max_utility = utility_value
                best_action = action

            if max_utility > min_option:
                return best_action

            max_option = max(max_option, max_utility)

        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def state_utility(self, state, index, depth, max_option, min_option):
        """
        Finds the state utility value for the specified state using the Expectimax
        algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value - should always be set to zero when called
                      externally.

        :return: The expected maximum utility value for the specified state.
        """
        index = (index+1) % state.getNumAgents()

        if index == 0: depth += 1

        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        if index == 0:
            return self.max_state_utility(state, index, depth+1, max_option, min_option)
        else:
            return self.exp_state_utility(state, index, depth, max_option, min_option)

    def max_state_utility(self, state, index, depth, max_option, min_option):
        """
        Finds the maximum state utility for the specified state using the
        Expectimax algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value.

        :return: The maximum state utility for the specified state.
        """

        max_value = -sys.maxint

        for action in state.getLegalActions(index):
            successor_state = state.generateSuccessor(index, action)
            value           = self.state_utility(successor_state, index, depth, max_option, min_option)
            max_value       = max(max_value, value)
            if max_value > min_option: return max_value
            max_option      = max(max_option, max_value)

        return max_value

    def exp_state_utility(self, state, index, depth, max_option, min_option):
        """
        Finds the expected state utility for the specified state using the
        Expectimax algorithm.

        :param state: The game state to search from.
        :param index: The agent index.
        :param depth: The depth value.

        :return: The utility-value for the specified state.
        """

        value = 0

        for action in state.getLegalActions(index):
            successor_state = state.generateSuccessor(index, action)
            probability     = 1.0 / len(state.getLegalActions(index))
            value           += probability * self.state_utility(successor_state, index, depth, max_option, min_option)

        return value

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        best_action = None
        max_utility = -sys.maxint
        max_option = -sys.maxint
        min_option = sys.maxint

        # Try all actions from the current game state and select the best one
        # according to expectimax. This is actually a job for the max_state_utility
        # function, but having this code here lets us simplify the others a bit.
        for action in gameState.getLegalActions(0):
            next_state    = gameState.generateSuccessor(0, action)
            utility_value = self.state_utility(next_state, 0, 0, max_option, min_option)

            if utility_value > max_utility:
                max_utility = utility_value
                best_action = action
        return best_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

      DESCRIPTION: <write something here so we know what you did>
    """
    from searchAgents import manhattan_distance

    import sys

    newPos             = currentGameState.getPacmanPosition()
    newFood            = currentGameState.getFood()
    newGhostStates     = currentGameState.getGhostStates()
    newScaredTimes     = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Find the nearest ghost.
    ghost_distance = sys.maxint
    for ghost_state in newGhostStates:
        dist = manhattan_distance(ghost_state.getPosition(), newPos)
        ghost_distance = min(ghost_distance, dist)

    # Find the nearest food.
    food_distance = sys.maxint
    for x in range(newFood.width):
        for y in range(newFood.height):
            if newFood[x][y]:
                dist = manhattan_distance(newPos, (x,y))
                food_distance = min(food_distance, dist)

    # Make sure we can handle situations without any ghosts or food.
    if ghost_distance == sys.maxint: ghost_distance = 0
    if food_distance  == sys.maxint: food_distance  = 0

    # Start with the 'default' state score.
    score = currentGameState.getScore()

    # The ghost is nearby - penalize Pacman by slapping him across the face
    # with negative points. Since our evaluation need not be continuous (ie.
    # it's ok to have abrupt changes missing derivatives), using an if-
    # statement here is a cheap way to make this evaluation function pretty
    # much unbeatable. One could also imagine some kind of polynomial
    # function mimicking the if-statement without breaking continuity.
    if ghost_distance < 6:
        score -= 100.0 / (ghost_distance+1)

    # Help Pacman detect nearby food slightly.
    score += 1.0 / (food_distance+1)

    return score

# Abbreviation
better = betterEvaluationFunction
