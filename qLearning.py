# state = (playerCardValueExcludingAce, dealerCardValue, hasUsableAce)
# denotes dealerCardValue = {1, 2, 3, 4, ..., 10}

from mdp import *
import random
import matplotlib.pyplot as plt 
import numpy as np 

"""
Author: Shing Hei Ho (Adrian)
"""
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
    
    def decayEpsilon(self):
        self.epsilon *= 0.999
    
    def decayAlpha(self):
        self.alpha *= 0.999
    
    def getLegalActions(self, state):
        if self.isTerminal(state):
            return []
        else:
            return ["hit", "stand"]
        
    def isTerminal(self, state):
        playerCardValue, dealerCard, numAces = state
        if playerCardValue+numAces > 21 or playerCardValue+numAces == 21 or playerCardValue+numAces*11 == 21:
            return True
        else:
            return False
    
    def flipCoin(self, p):
        r = random.random()
        return r < p
    

####################################################
################# Game Loop ########################
####################################################
print("++++++++++++training")
agent = QLearningAgent(alpha=0.2, epsilon=0.1)
numGames = 10000
printIter = 1000
cumReward = 0

# for visualizing policy
states = set()

for iter in range(numGames):
    # create deck and deal initial cards
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
    
    states.add(state)
    
    if playerCardValue+numAces*11 == 21:
        #print("blackjack, not useful information to learn")
        continue
    
    while (True):
        action = agent.getEpsilonGreedyAction(state)
        states.add(state)
        
        if action == "hit":
            dealCard(deck, dealerCards, playerCards, isToPlayer=True)
            playerCardValue, numAces = getPlayerCardValueExcludeAce(playerCards)
            #transition
            nextState = (playerCardValue, dealerCards[1], numAces)
            
            reward = 0
            playerTotalValue = computePlayerTotalValue(playerCards)
            if playerTotalValue > 21:
                reward = -1
                cumReward+=reward
                agent.update(state, action, nextState, reward)
                break
            elif playerTotalValue == 21:
                reward = dealerPlay(dealerCards, deck, playerCards)
                #reward = 1
                cumReward+=reward
                agent.update(state, action, nextState, reward)
                break
            # else:
            #     agent.update(state, action, nextState, reward)
                
            state = nextState
            
        elif action == "stand":
            nextState = (playerCardValue, dealerCards[1], numAces)
            reward = dealerPlay(dealerCards, deck, playerCards)
            cumReward+=reward
            agent.update(state, action, nextState, reward)
            break
        
        else:
            print("++++++++++++++++++++++++++++++bug++++++++++++++++++++++")
    
    # iter+1 ranges from 1 to numGames
    if (iter+1)%printIter==0:
        print(f"iter: {iter+1}/{numGames}: ", f"cumReward: {cumReward}")
        cumReward = 0
        # agent.decayEpsilon()
        # agent.decayAlpha()

        

 
#################################################################           
################### Visualization of policy #####################  
#################################################################
policies = []
for numAce in range(5):
    policy = {}
    for playerCardValue in range(1,22,1):
        for dealerCard in range (1,11,1):
            state = (playerCardValue, dealerCard, numAce)
            if state not in states:
                continue    
            action = agent.getActionFromQValue(state)
            policy[state] = action
            
    policies.append(policy)
    
print(len(policies))
for i in range(len(policies)):
    policy = policies[i]
    playerStates = []
    dealerStates = []
    actions = []
    for key, value in policy.items():
        playerStates.append(key[0])
        dealerStates.append(key[1])
        actions.append(value)
    
    colors = []
    for action in actions:
        if action=="hit":
            colors.append("red")
        elif action=="stand":
            colors.append("green")
        else:
            colors.append("black")
    
    plt.scatter(dealerStates, playerStates, c=colors)
    plt.title(f"policy for number of ace = {i}")
    plt.xlabel("dealerCard")
    plt.ylabel("PlayerCardValueExcludingAces")
    plt.show()
    
        
        
        





