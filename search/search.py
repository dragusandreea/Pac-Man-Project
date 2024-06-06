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
##NSEV ordine succesori

class Node:
    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getCost(self):
        return self.cost

    def constructPath(self, node, path):
        while (node != None and node.getParent() != None):
            path.append(node.getAction())
            node = node.getParent()

        path.reverse()
        return path
            
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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    """
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    """
    #cream un nod nou pentru starea initiala
    startNode = Node(problem.getStartState(), None, None, 0)
    #frontiera este o stiva
    frontier = util.Stack()
    # adaugam nodul de start in frontiera
    frontier.push(startNode)
    #lista care contine starile nodurilor expandate
    reached = []
    #calea pe care o urmeaza Pacman pana la goal din starea initiala
    path = []

    #cat timp frontiera nu este goala
    while (not frontier.isEmpty()):
        #scoate un nod din frontiera
       node = frontier.pop()

        #daca acesta stare este goal state construim calea pe care o parcurge Pacman
       if (problem.isGoalState(node.getState())):
            return startNode.constructPath(node, path)

        #daca nu e goal state si daca nodul nostru nu este deja expandat
       if node.getState() not in reached:
            #adaugam starea in lista de noduri expandate
            reached.append(node.getState())
            
            #calculam succesori starii curente
            successors = problem.getSuccessors(node.getState())

            #pentru fiecare succesor
            for state, action, cost in successors:
                #cream un nou nod copil
                childNode = Node(state, node, action, cost)
                
                #daca copilul nu este deja expandat
                if state not in reached:
                    #il adaugam in frontiera
                    frontier.push(childNode)
  
    #returnam calea lui Pacman
    return path
    #util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #cream un nod nou pentru starea initiala
    startNode = Node(problem.getStartState(), None, None, 0)
    #frontiera este o coada
    frontier = util.Queue()
    # adaugam nodul de start in frontiera
    frontier.push(startNode)
    #lista care contine starile nodurilor expandate
    reached = []
    #calea pe care o urmeaza Pacman pana la goal din starea initiala
    path = []

    #cat timp frontiera nu este goala
    while (not frontier.isEmpty()):
        #scoate un nod din frontiera
       node = frontier.pop()

        #daca acesta stare este goal state construim calea pe care o parcurge Pacman
       if (problem.isGoalState(node.getState())):
            return startNode.constructPath(node, path)

        #daca nu e goal state si daca nodul nostru nu este deja expandat
       if node.getState() not in reached:
            #adaugam starea in lista de noduri expandate
            reached.append(node.getState())
            
             #calculam succesori starii curente
            successors = problem.getSuccessors(node.getState())

            #pentru fiecare succesor
            for state, action, cost in successors:
                #cream un nou nod copil
                childNode = Node(state, node, action, cost)

                #daca copilul nu este deja expandat
                if state not in reached:
                    #il adaugam in frontiera
                    frontier.push(childNode)
  
    #returnam calea lui Pacman
    return path
    
    #util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #cream un nod nou pentru starea initiala
    startNode = Node(problem.getStartState(), None, None, 0)
    #frontiera este o coada de prioritati unde prioritatea este reprezentata de costul pana in aceasta stare
    frontier = util.PriorityQueue()
    # adaugam nodul de start in frontiera impreuna cu costul acestuia
    frontier.push(startNode, startNode.getCost())
    #lista care contine starile nodurilor expandate
    reached = []
    #calea pe care o urmeaza Pacman pana la goal din starea initiala
    path = []

    #cat timp frontiera nu este goala
    while (not frontier.isEmpty()):
        #scoate un nod din frontiera
       node = frontier.pop()

        #daca acesta stare este goal state construim calea pe care o parcurge Pacman
       if (problem.isGoalState(node.getState())):
            return startNode.constructPath(node, path)

        #daca nu e goal state si daca nodul nostru nu este deja expandat
       if node.getState() not in reached:
            #adaugam starea in lista de noduri expandate
            reached.append(node.getState())
            
             #calculam succesori starii curente
            successors = problem.getSuccessors(node.getState())

            #pentru fiecare succesor
            for state, action, cost in successors:
                #cream un nou nod copil
                childNode = Node(state, node, action, cost + node.getCost())

                #daca copilul nu este deja expandat
                if state not in reached:
                    #il adaugam in frontiera
                    frontier.push(childNode, childNode.getCost())
  
    #returnam calea lui Pacman
    return path
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #cream un nod nou pentru starea initiala
    startNode = Node(problem.getStartState(), None, None, 0)
    #frontiera este o coada de prioritati unde prioritatea este reprezentata de suma dintre cost si euristica
    frontier = util.PriorityQueue()
    # adaugam nodul de start in frontiera impreuna cu suma dintre cost si euristica
    frontier.push(startNode, startNode.getCost() + (heuristic(problem.getStartState(), problem)))
    #lista care contine starile nodurilor expandate
    reached = []
    #calea pe care o urmeaza Pacman pana la goal din starea initiala
    path = []

    #cat timp frontiera nu este goala
    while (not frontier.isEmpty()):
        #scoate un nod din frontiera
       node = frontier.pop()

        #daca acesta stare este goal state construim calea pe care o parcurge Pacman
       if (problem.isGoalState(node.getState())):
            return startNode.constructPath(node, path)


        #daca nu e goal state si daca nodul nostru nu este deja expandat
       if node.getState() not in reached:
            #adaugam starea in lista de noduri expandate
            reached.append(node.getState())
            
             #calculam succesori starii curente
            successors = problem.getSuccessors(node.getState())

            #pentru fiecare succesor
            for state, action, cost in successors:
                childNode = Node(state, node, action, cost + node.getCost())
                
                #daca copilul nu este deja expandat
                if state not in reached:
                    #il adaugam in frontiera
                    frontier.push(childNode, childNode.getCost() + (heuristic(state, problem)))
  
    #returnam calea lui Pacman
    return path

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
