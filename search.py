#-*- coding: utf-8 -*-

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

""" ----------------------------------------------------------------------- """
""" Code below by: PYTHON TRIFORCE TEAM   ▲
                                         ▲ ▲
"""

"""-----------------------------------------------
 " CLASS
 "---------------------------------------------"""

class Node:
    """ Represents a search node. """

    """-----------------------------------------------
     " METHODS
     "---------------------------------------------"""

    def __init__(self, parent, action, state, depth, cost):
        """
        Constructor.

        :param parent: The parent node.
        :param action: The action responsible for the node state.
        :param state:  The node state.
        :param depth:  The depth of the node (in a graph).
        :param cost:   The cost (g) to reach the node from the root.

        :return:       A node with the specified parameters set.
        """

        self.action = action
        self.cost   = cost
        self.depth  = depth
        self.parent = parent
        self.state  = state

    def createChild(self, action, state, cost):
        """
        Creates a child node.

        :param action: The action taken to reach the child node from its
                       parent.
        :param state:  The child node state.
        :param cost:   The cost of reaching the child node state from its
                       parent node state through taking the specified action.

        :return: A child node.
        """
        return Node(self, action, state, self.depth+1, cost)

    @staticmethod
    def createRoot(state):
        """
        Creates a root node.

        :param state: The root node state.

        :return: A node representing the specified state.
        """
        return Node(None, None, state, 0, 0)

"""-----------------------------------------------
 " FUNCTIONS
 "---------------------------------------------"""

def graphSearch(problem):
    """
    Solves the specified problem by using a graph search algorithm.

    :param problem: The problem to solve.

    :return: A list containing the actions required to solve the specified
             problem.
    """

    closed = []
    fringe = []

    """ Add the root node. It doesn't have a parent, nor an action or cost, and
        the depth is zero. """
    rootNode = Node.createRoot(problem.getStartState())
    fringe.append(rootNode)

    while fringe:
        """ TODO: Let client specify fringe. """
        node = fringe.pop(0)

        """ Check if we have reached the goal state. This is what the pseudo-
            code tells us to do, as opposed to what Mr. Gabrielsson claims;
            that we should NOT detect goal state nodes directly after popping
            them from the fringe! How peculiar! ;-) Either way, it seems to
            work fine. """
        if problem.isGoalState(node.state): return gsSolution(node)

        """ Make sure we don't expand this particular state more than once. """
        if node.state not in closed:
            closed.append(node.state)
            fringe.extend(gsExpand(node, problem))

    """ The fringe was exhausted; no solution could be found. """
    return None


def gsExpand(node, problem):
    """
    Expands the specified node.

    :param node:    The node to expand.
    :param problem: The problem related to the node.

    :return:        A list containing the successor state nodes for the
                    specified node.
    """

    successors = []
    for nextState, action, cost in problem.getSuccessors(node.state):
        childNode = node.createChild(action, nextState, cost)
        successors.append(childNode)

    return successors

def gsSolution(node):
    """
    Retrieves the solution as a list containing the actions needed to go from
    the root node state to the specified node state.

    :param node: The end (goal) node.

    :return: A list containing the actions needed to reach the end node.
    """

    solution = []

    while (node.parent is not None):
        solution.append(node.action)
        node = node.parent

    """ The solution needs to be reversed since we are working our way from the
        goal state back (through the graph) towards the initial state! """
    solution.reverse()
    return solution


""" ----------------------------------------------------------------------- """


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
