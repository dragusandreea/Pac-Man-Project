# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class RandomAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        chosenIndex = random.choice(range(0, len(legalMoves)))
        return legalMoves[chosenIndex]

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #distante manhattan intre noua pozitie a lui Pacman si fantome
        ghostDistances = []
        for ghost in newGhostStates:
            ghostDistances.append(util.manhattanDistance(newPos, ghost.getPosition()))
        
        #distante manhattan intre noua pozitie a lui Pacman si mancare
        foodDistances = []
        for food in newFood.asList():
            foodDistances.append(util.manhattanDistance(newPos, food))

        score = successorGameState.getScore()
        
        #daca noua pozitie a lui Pacman coincide cu cea actuala => returnam o valuare mica
        if currentGameState.getPacmanPosition() == newPos:
            return -10000
        
        #daca avem mancare ramasa, din scor scadem cea mai mica distanta pana la mancare
        if (len (foodDistances) > 0):
            score -= min(foodDistances)
        
        #daca avem fantome
        if (len (ghostDistances) > 0):
            #calculam distanta minima pana la fantoma
            minGhost = min(ghostDistances)
            
            #daca distanta minima pana la fantoma e 0, inseamna ca pozitiile lui Pacman si a fantomei coincid => Pacman e omorat de fantoma
            if (minGhost == 0):
                #scorul aferent fantomelor ia o valoare mica 
                minGhost = -10000
            else:
                #daca distanta minima pana la fantoma nu e 0, scorul aferent fantomelor este unul negativ, deoarece fantomele reprezinta un lucru rau
                #si este invers proportional cu distanta pana la cea mai apropriata fantoma
                #daca fantoma e aproape minGhost va avea o valoare mai mica
                #daca fantoma e departe minGhost va avea o valoare mai mare
                minGhost = -1 / minGhost
            
            #adunam la scorul total scorul aferent fantomelor
            score += minGhost
        #din scorul total scadem numarul bucatilor de mancare ramase * 10 
        score -= 10 * len(newFood.asList())

        #returnam scorul
        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #returnam actiunea, adica al doilea elemnt din tupla rezultata din apelul minmax_decision
        return self.minmax_decision(gameState, 0, 0)[1]

        #util.raiseNotDefined()

    def minmax_decision(self, gameState, agentIndex, depth):
        #in cazul in are am ajuns la nod terminal, vom apela functia de evaluare
        if(gameState.isWin() or gameState.isLose() or depth == self.depth):
            return self.evaluationFunction(gameState), ""
        
        #daca nu am ajuns la nod terminal, verificam tipul agentului
        #daca este Pacman
        if (agentIndex == 0):
            #suntem pe nivel de maxim
            return self.max_value(gameState, agentIndex, depth)
        #daca este fantoma
        else:
            #sutem pe nivel de minim
            return self.min_value(gameState, agentIndex, depth)

    def max_value(self, gameState, agentIndex, depth):
        #initializam valoarea maxima cu o valoare foarte mica (-infinit)
        maxValue = -9999999
        
        maxAction = ""

        #preluam actiunile legale pe care le poate efectua Pacman din starea curenta
        actions = gameState.getLegalActions(agentIndex)
        
        #pentru fiecare actiune pe care o poate efectua Pacman
        for action in actions: 
            #generam urmatorul game state pentru starea curenta a lui Pacman daca ar face actiunea action
            successor = gameState.generateSuccessor(agentIndex, action)
            successorIndex = agentIndex + 1
            successorDepth = depth
            
            #daca am ajuns cu indexul la numarul total al agentilor, inseamna ca am ajuns la Pacman
            #deoarece Pacman are agentIndex = 0 iar fantomele au agentIndex = 1, numAgents() - 1
            if (successorIndex == gameState.getNumAgents()):
                successorIndex = 0
                #daca am ajuns iar la Pacman inseamna ca s-a terminat un nivel max-min si crestem adancimea pentru a trece la urmatorul
                successorDepth = depth + 1
            
            #apelam minmax_decision pentru a ne propaga recursiv pana la nodurile terminale pentru a obtine valorile date de evaluation function
            currentAgent = self.minmax_decision(successor, successorIndex, successorDepth)
            
            #suntem pe nivel de maxim, deci vom calcula valoarea maxima si vom retine actiunea pentru care se realizeaza
            if (currentAgent[0] > maxValue):
                maxValue = currentAgent[0]
                maxAction = action
        
        #returnam valoarea maxima alaturi de actiunea care trebuie realizata pentru a o atinge
        return maxValue, maxAction

    def min_value(self, gameState, agentIndex, depth):
        #initializam valoarea minima cu o valoare mare
        minValue = 9999999
        minAction = ""

        #preluam actiunile legale pe care le poate realiza fantoma 
        actions = gameState.getLegalActions(agentIndex)
        
        #pentru fiecare actiune legala pe care o poate realiza fantoma
        for action in actions: 
            #generam urmatorul game state pentru fantoma daca ar face actiunea action
            successor = gameState.generateSuccessor(agentIndex, action)
            successorIndex = agentIndex + 1
            successorDepth = depth
            
            #daca am ajuns cu indexul la numarul total al agentilor, inseamna ca am ajuns la Pacman
            #deoarece Pacman are agentIndex = 0 iar fantomele au agentIndex = 1, numAgents() - 1
            if (successorIndex == gameState.getNumAgents()):
                successorIndex = 0
                #daca am ajuns iar la Pacman inseamna ca s-a terminat un nivel max-min si crestem adancimea pentru a trece la urmatorul
                successorDepth = depth + 1

            #apelam minmax_decision pentru a ne propaga recursiv pana la nodurile terminale pentru a obtine valorile date de evaluation function
            currentAgent = self.minmax_decision(successor, successorIndex, successorDepth)
            
            #fiind pe nivel de minim, vom calcula valoarea minima si vom retine actiunea pe care trebuie sa o faca Fantoma pentru a o atinge
            if (currentAgent[0] < minValue):
                minValue = currentAgent[0]
        
                minAction = action
        #returnam valoarea minima alaturi de actiunea care trebuie realizata pentru a o atinge
        return minValue, minAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #returnam al doilea element dintre cele 2 returnate de alpha_beta_search, adica actiunea
        #initial, agentIndex = 0 adica Pacman, depth = 0 , alpha = -inf, beta = inf
        return self.alpha_betha_search(gameState, 0, 0, -999999999, 999999999)[1]

        util.raiseNotDefined()

    def alpha_betha_search(self, gameState, agentIndex, depth, alpha, betha):
        #in cazul in are am ajuns la nod terminal, vom apela functia de evaluare
        if(gameState.isWin() or gameState.isLose() or depth == self.depth):
            return self.evaluationFunction(gameState), ""
        
        #in cazul in care nu suntem in nod terminal
        #daca agentul e Pacman 
        if (agentIndex == 0):
            #suntem pe nivel de maxim
            return self.max_value(gameState, agentIndex, depth, alpha, betha)
        #daca agentul e fantoma
        else:
            #suntem pe nivel de minim
            return self.min_value(gameState, agentIndex, depth, alpha, betha)

    def max_value(self, gameState, agentIndex, depth, alpha, betha):
        #initializam valoarea maxima cu o valoare mica
        maxValue = -9999999
        maxAction = ""

        #preluam actiunile legale pe care le poate realiza Pacman 
        actions = gameState.getLegalActions(agentIndex)
        
        #pentru fiecare actiune pe care o poate realiza Pacman
        for action in actions: 
            #generam urmatorul game state pentru starea curenta a lui Pacman daca ar face actiunea action
            successor = gameState.generateSuccessor(agentIndex, action)
            successorIndex = agentIndex + 1
            successorDepth = depth
            
            #apelam alpha_beta_search pentru a ne propaga recursiv pana la nodurile terminale pentru a obtine valorile date de evaluation function
            currentAgent = self.alpha_betha_search(successor, successorIndex, successorDepth, alpha, betha)
        
            #fiind pe nivel de maxim, vom calcula valoarea maxima si vom retine actiunea pe care trebuie sa o faca Pacman pentru a o atinge
            if (currentAgent[0] > maxValue):
                maxValue = currentAgent[0]
                maxAction = action
            
            #momentam suntem pe nivel de maxim, deci urmatorul nivel va fi de minim
            #daca valoarea maxima obtinuta e mai mare decat beta, atunci nu vom continua cautarea pe ramura respectiva
            #deoarece, calculand minimul obtinem: min(beta, ceva>beta) = beta
            if (maxValue > betha):
                return maxValue, maxAction
            
            #in cazul in care maxValue < beta
            #actualizam alpha ca maximul dintre valoarea sa actuala si maxValue
            alpha = max(alpha, maxValue)
        
        return maxValue, maxAction

    def min_value(self, gameState, agentIndex, depth, alpha, betha):
        #initializam valoarea minima cu o valoare mare
        minValue = 9999999
        minAction = ""

        #preluam actiunile legale pe care le poate realiza fantoma
        actions = gameState.getLegalActions(agentIndex)
        
        #pentru fiecare actiune legala care poate fi facuta de fantoma
        for action in actions:
            #generam urmatorul game state pentru starea curenta a fantomei  daca ar face actiunea action
            successor = gameState.generateSuccessor(agentIndex, action)
            successorIndex = agentIndex + 1
            successorDepth = depth

            #daca am ajuns cu indexul la numarul total al agentilor, inseamna ca am ajuns la Pacman
            #deoarece Pacman are agentIndex = 0 iar fantomele au agentIndex = 1, numAgents() - 1
            if (successorIndex == gameState.getNumAgents()):
                successorIndex = 0
                #daca am ajuns iar la Pacman inseamna ca s-a terminat un nivel max-min si crestem adancimea pentru a trece la urmatorul
                successorDepth = depth + 1

            #apelam alpha_beta_search pentru a ne propaga recursiv pana la nodurile terminale pentru a obtine valorile date de evaluation function
            currentAgent = self.alpha_betha_search(successor, successorIndex, successorDepth, alpha, betha)
            
            #fiind pe nivel de maxim, vom calcula valoarea minima si vom retine actiunea pe care trebuie sa o faca fantoma pentru a o atinge
            if (currentAgent[0] < minValue):
                minValue = currentAgent[0]
                minAction = action
            
            #momentam suntem pe nivel de minim, deci urmatorul nivel va fi de maxim
            #daca valoarea minima obtinuta e mai mica decat alpha, atunci nu vom continua cautarea pe ramura respectiva
            #deoarece, calculand maximul obtinem: max(alpha, ceva<alpha) = alpha
            if (minValue < alpha):
                return minValue, minAction

            #daca valoarea nu e mai mica, atunci actualizam beta   
            betha = min(betha, minValue)


        return minValue, minAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """"
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "* YOUR CODE HERE *"
        
        #returnam al doilea element dintre cele 2 returnate de expectimax, adica actiunea
        return self.expectimax(gameState, self.index, 0)[1]

    def expectimax(self, gameState, agentIndex, depth):
        #daca suntem in nod terminal, returnam valoarea functiei de evaluare
        if(gameState.isWin() or gameState.isLose() or depth == self.depth):
            return self.evaluationFunction(gameState), ""
        
        #daca nu suntem in nod terminal, verificam tipul agentului
        #daca e Pacman
        if (agentIndex == 0):
            #suntem pe nivel de maxim
            return self.max_value(gameState, agentIndex, depth)
        #daca e fantoma
        else:
            #suntem pe nivel de probabilitate
            return self.prob_value(gameState, agentIndex, depth)


    def prob_value(self, gameState, agentIndex, depth):
        probValue = 0
        options = 0 
        probAction = ""

        #preluam toate actiunile legale pe care poate fantoma sa le faca
        actions = gameState.getLegalActions(agentIndex)
    
        #pentru fiecare actiune legala care poate fi executata de fantoma
        for action in actions:
            #generam urmatorul game state in care ne vom afla daca fantoma face actiunea action
            successor = gameState.generateSuccessor(agentIndex, action)
            successorIndex = agentIndex + 1
            successorDepth = depth
            
            #daca am ajuns cu indexul la numarul total al agentilor, inseamna ca am ajuns la Pacman
            #deoarece Pacman are agentIndex = 0 iar fantomele au agentIndex = 1, numAgents() - 1
            if (successorIndex == gameState.getNumAgents()):
                successorIndex = 0
                #daca am ajuns iar la Pacman inseamna ca s-a terminat un nivel max-prob si crestem adancimea pentru a trece la urmatorul
                successorDepth = depth + 1
            
            #apelam expectimax pentru a ne propaga recursiv pana la nodurile terminale pentru a obtine valorile date de evaluation function
            currentAgent = self.expectimax(successor, successorIndex, successorDepth)
            #suma valorilor nodurilor (la nodurile terminale e data de functia de evaluare, iar la nodurile neterminala e probabilitatea)
            probValue += currentAgent[0]
            #numarul optiunilor (a ramurilor)
            options += 1
        
        #valoarea nodului e data de suma probabilitatior impartita la numar de optiuni (deci e practic tot o probabilitate)
        return float(probValue) / options, probAction

    def max_value(self, gameState, agentIndex, depth):
        maxValue = -9999999
        maxAction = ""

        #preluam actiunile legale pe care le poate face Pacman
        actions = gameState.getLegalActions(agentIndex)

        #pentru fiecare actiune legala 
        for action in actions:
            #generam urmatorul game state in care ne vom afla daca Pacman face actiunea action
            successor = gameState.generateSuccessor(agentIndex, action)
            successorIndex = agentIndex + 1
            successorDepth = depth

            #apelam expectimax pentru a ne propaga recursiv pana la nodurile terminale pentru a obtine valorile date de evaluation function
            currentAgent = self.expectimax(successor, successorIndex, successorDepth)
            
            #fiind pe nivel de maxim vom calula valoarea maxima si o vom retine impreuna cu actiunea pe care trebuie sa o faca Pacman pentru a o obtine
            if (currentAgent[0] > maxValue):
                maxValue = currentAgent[0]
                maxAction = action

        return maxValue, maxAction


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    #calculam distantele Manhattan intre Pacman si fantome
    ghostDistances = []
    for ghost in newGhostStates:
        ghostDistances.append(util.manhattanDistance(newPos, ghost.getPosition()))
    
    #calculam distantele Manhattan intre Pacman si mancare
    foodDistances = []
    for food in newFood.asList():
        foodDistances.append(util.manhattanDistance(newPos, food))
    
    #calculam distanta minima pana la cea mai apropiata fantoma
    minGhostDistance = min(ghostDistances) if len(ghostDistances) > 0 else 0
    
    #calculam distanta minima pana la cea mai apropiata bucata de mancare
    minFoodDistance = min(foodDistances) if (len(foodDistances) > 0)  else 0
    
    #calculam timpul minim in care fantomele au fost inactive
    minScaredTime = min(newScaredTimes) if (len(newScaredTimes) > 0)  else 0
    
    ghost_score = 0
    food_score = 0
    scared_score = 0


    #daca distanta pana la fantoma e 0, inseamna ca ea si Pacman se afla pe aceeasi pozitie
    #in acest caz, Pacman e omorat de fantoma, motiv pentru care ghost_score va a avea o valoare foarte mica
    if(minGhostDistance == 0):
        ghost_score = -10000000
    else:
        #daca suntem aproape de fantoma activa, minDistance va avea o valoare mica, deci 1/minDistance va fi o valoare mai mare 
        #insa, faptul ca Pacman e in apropierea unei fantome nu e un avantaj, astfel ca ghost_score ia  valoarea negativa
        ghost_score = -1/ minGhostDistance

        #daca fantoma e inactiva avem un avantaj, deci nu vom da o valoare negative ghost_score=> 
        if (minScaredTime != 0):
            ghost_score = 1/minGhostDistance
            #faptul ca am speriat fantoma ne ofera din nou un avantaj, insa nu atat de semnificativ
            scared_score = 0.5 * minScaredTime
    
    #daca ramane mancare =>  
    if (len(newFood.asList()) > 0):
        #food_score va lua o valoare negativa, direct proportionala cu numarul de bucati de mancare ramase
        food_score = -len(newFood.asList())
        #daca mancarea e aproape, avem un beneficiu mai mare pe care il adunam la food_score, deoarece 0.5/minFoodDistance va avea o valoare mai mica
        #daca mancarea e departe, avem un beneficiu mai mic pe care il adunam la food_score 
        food_score += 0.5/minFoodDistance

    
    #noua functie de evaluare returneaza suma tuturor scorurilor
    return ghost_score + scared_score + food_score + currentGameState.getScore() * 0.6


# Abbreviation
better = betterEvaluationFunction
