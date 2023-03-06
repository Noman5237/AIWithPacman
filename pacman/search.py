# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


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
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    visited = []
    def recursiveDfs(problem: SearchProblem, state):
        nonlocal visited
        visited.append(state[0])
        if problem.isGoalState(state[0]):
            return []
        successors = problem.getSuccessors(state[0])
        if len(successors) == 0:
            return None
        for successor in successors:
            if successor[0] in visited:
                continue
            traversed = recursiveDfs(problem, successor)
            if traversed is not None:
                location, direction, cost = successor
                traversed.append(direction)
                return traversed

    moves = recursiveDfs(problem, (problem.getStartState(), '', 0))
    moves.reverse()
    return moves


def breadthFirstSearch(problem: SearchProblem):
    startState = problem.getStartState()
    visited = [startState]
    queue = [startState]
    path = {
        startState: []
    }

    # while queue is not empty
    while len(queue) != 0:
        # pop from the queue
        node = queue.pop(0)

        if problem.isGoalState(node):
            return path[node]

        successors = problem.getSuccessors(node)
        for successor in successors:
            location, direction, cost = successor
            if location not in visited:
                visited.append(location)
                queue.append(location)
                path[location] = path[node] + [direction]


def uniformCostSearch(problem: SearchProblem):
    startState = problem.getStartState()
    costs = {
        startState: 0
    }
    path = {
        startState: []
    }

    visited = [startState]
    queue = [startState]

    while len(queue) != 0:
        node = queue.pop(0)
        visited.append(node)

        if problem.isGoalState(node):
            return path[node]

        successors = problem.getSuccessors(node)
        for successor in successors:
            location, direction, cost = successor
            if location in visited:
                continue

            if location not in queue:
                queue.append(location)
            if location not in costs:
                costs[location] = costs[node] + cost
                path[location] = path[node] + [direction]
            elif costs[node] + cost < costs[location]:
                costs[location] = costs[node] + cost
                path[location] = path[node] + [direction]

        queue.sort(key=lambda x: costs[x])


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    startState = problem.getStartState()

    costs = {
        startState: 0
    }

    path = {
        startState: []
    }

    visited = [startState]
    queue = [startState]

    while len(queue) != 0:
        node = queue.pop(0)
        visited.append(node)

        if problem.isGoalState(node):
            return path[node]

        successors = problem.getSuccessors(node)
        for successor in successors:
            location, direction, cost = successor
            if location in visited:
                continue

            if location not in queue:
                queue.append(location)
            if location not in costs:
                costs[location] = costs[node] + cost + heuristic(location, problem)
                path[location] = path[node] + [direction]
            elif costs[node] + cost + heuristic(location, problem) < costs[location]:
                costs[location] = costs[node] + cost + heuristic(location, problem)
                path[location] = path[node] + [direction]

        queue.sort(key=lambda x: costs[x])


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
