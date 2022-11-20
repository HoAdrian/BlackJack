# state = (playerCardValueExcludingAce, dealerCardValue, hasUsableAce)
# denotes dealerCardValue = {1, 2, 3, 4, ..., 10}

from mdp import *
import random

class QLearningAgent:
    def __init__(self, alpha, epsilon, gamma=1):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.qValues = {}
        
    def update(self, state, action, nextState, reward):
        sample = reward + self.gamma*self.getValueFromQValue(nextState)
        oldQ = self.getQValue(state, action)
        self.qValues[(state,action)] = (1-self.alpha)*oldQ + self.alpha * sample
        
    def getQValue(self, state, action):
        return self.qValues.get((state, action), 0)
        
    def getValueFromQValue(self, state):
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return 0
        actionValues = [self.getQValue(state, action) for action in legalActions]
        return max(actionValues)
            
    def getActionFromQValue(self, state):
        legalActions = self.getLegalActions(state)
        if len(legalActions)==0:
          return None
        actionValues = {action: self.getQValue(state, action) for action in legalActions}
        bestActionValue = max(actionValues.values())
        bestActions = [action for action in legalActions if actionValues[action]==bestActionValue]
        return random.choice(bestActions)
    
    def getEpsilonGreedyAction(self, state):
        # Pick Action
        legalActions = self.getLegalActions(state)
        isRandomAction = self.flipCoin(self.epsilon)
        
        if(isRandomAction):
          return random.choice(legalActions)

        return self.getActionFromQValue(state)
    
    def getLegalActions(self, state):
        if isTerminal(state):
            return []
        else:
            return ["hit", "stand"]
    
    def flipCoin(self, p):
        r = random.random()
        return r < p
    


################# Game Loop ########################

agent = QLearningAgent(alpha=0.5, epsilon=0)

numGames = 3

for iter in range(numGames):
    # create deck and configure game
    cards = [[i,i,i,i] for i in range(1, 11, 1)]
    deck = []
    for fourCards in cards:
        deck.extend(fourCards)

    playerCards = {}
    dealerCards = []
    for i in range(2):
        dealCard(deck, dealerCards, playerCards, isToPlayer=True)
    for i in range(2):
        dealCard(deck, dealerCards, playerCards, isToPlayer=False)
            
    playerCardValue, numAces = getPlayerCardValueExcludeAce(playerCards)
    # assume the second card of the dealer is revealed
    state = (playerCardValue, dealerCards[1], numAces)
    
    while (True):
        action = agent.getActionFromQValue(state)
        
        if action == "hit":
            dealCard(deck, dealerCards, playerCards, isToPlayer=True)
            
            playerCardValue, numAces = getPlayerCardValueExcludeAce(playerCards)
            
            #transition
            nextState = (playerCardValue, dealerCards[1], numAces)
            
            reward = 0
            playerTotalValue = computePlayerTotalValue(playerCards)
            if playerTotalValue > 21:
                reward = -1
                agent.update(state, action, nextState, reward)
                break
            elif playerTotalValue == 21:
                reward = dealerPlay(dealerCards, deck, playerCards)
                agent.update(state, action, nextState, reward)
                break
            else:
                agent.update(state, action, nextState, reward)
                
            state = nextState
            
        elif action == "stand":
            nextState = (playerCardValue, dealerCards[1], numAces)
            playerCardValue, dealerCard, numAces = nextState
            reward = dealerPlay(dealerCards, deck, playerCards)
            agent.update(state, action, nextState, reward)
            break
        
        else:
            print("bug")
            
    print(f"iter: {iter+1}/{numGames}: ", f"reward: {reward}")
    #print(agent.qValues)
            
        
        
            
            
    
            
            
            

    
    
    

