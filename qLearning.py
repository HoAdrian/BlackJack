# state = (playerCardValueExcludingAce, dealerCardValue, hasUsableAce)
# denotes dealerCardValue = {1, 2, 3, 4, ..., 10}

from blackjackHelper import *
import random
import matplotlib.pyplot as plt 

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
        legalActions = getLegalActions(state)
        if len(legalActions) == 0:
            return 0
        actionValues = [self.getQValue(state, action) for action in legalActions]
        return max(actionValues)
            
    def getActionFromQValue(self, state):
        legalActions = getLegalActions(state)
        if len(legalActions)==0:
          return None
        actionValues = {action: self.getQValue(state, action) for action in legalActions}
        bestActionValue = max(actionValues.values())
        bestActions = [action for action in legalActions if actionValues[action]==bestActionValue]
        return random.choice(bestActions)
    
    def getEpsilonGreedyAction(self, state):
        # Pick Action
        legalActions = getLegalActions(state)
        isRandomAction = self.flipCoin(self.epsilon)
        
        if(isRandomAction):
          return random.choice(legalActions)

        return self.getActionFromQValue(state)
    
    def decayEpsilon(self):
        self.epsilon *= 0.9
    
    def decayAlpha(self):
        self.alpha *= 0.9
    
    def flipCoin(self, p):
        r = random.random()
        return r < p
    

####################################################
################# Game Loop ########################
####################################################
print("++++++++++++training")
agent = QLearningAgent(alpha=0.2, epsilon=0.2, gamma=0.6)
numGames = 1000000
# for checking progress
printIter = 10000
decayIter = 10000
cumReward = 0
numWin = 0
numLose = 0
numDraw = 0
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
    
    transitions = []
    
    while (True):
        action = agent.getEpsilonGreedyAction(state)
        states.add(state)
        
        if action == "hit":
            dealCard(deck, dealerCards, playerCards, isToPlayer=True)
            playerCardValue, numAces = getPlayerCardValueExcludeAce(playerCards)
            nextState = (playerCardValue, dealerCards[1], numAces)
            
            reward = 0.0
            playerTotalValue = computePlayerTotalValue(playerCards)
            
            if playerTotalValue > 21:
                numLose+=1
                reward = -1.0
                cumReward+=reward
                # propagate the reward to previous states
                cumGamma = agent.gamma**len(transitions)
                for s, a, s_prime in transitions:
                    agent.update(s, a, s_prime, cumGamma*reward)
                    cumGamma/=agent.gamma
                agent.update(state, action, nextState, reward)
                break
            elif playerTotalValue == 21:
                numWin+=1
                reward = dealerPlay(dealerCards, deck, playerCards)
                #reward = 1.0
                cumReward+=reward
                # propagate the reward to previous states
                cumGamma = agent.gamma**len(transitions)
                for s, a, s_prime in transitions:
                    agent.update(s, a, s_prime, cumGamma*reward)
                    cumGamma/=agent.gamma
                agent.update(state, action, nextState, reward)
                break
            else:
                #agent.update(state, action, nextState, 0.5)
                transitions.append((state, action, nextState))
                
            state = nextState
            
        elif action == "stand":
            nextState = (playerCardValue, dealerCards[1], numAces)
            reward = dealerPlay(dealerCards, deck, playerCards)
            if reward==0:
                numDraw+=1
            elif reward==1:
                numWin+=1
            else:
                numLose+=1
            cumReward+=reward
            # propagate the reward to previous states
            cumGamma = agent.gamma**len(transitions)
            for s, a, s_prime in transitions:
                agent.update(s, a, s_prime, cumGamma*reward)
                cumGamma/=agent.gamma
            agent.update(state, action, nextState, reward)
            break
        
        else:
            print("++++++++++++++++++++++++++++++bug++++++++++++++++++++++")
    
    if(iter+1)%decayIter==0:
        agent.decayEpsilon()
        agent.decayAlpha()
    
    # iter+1 ranges from 1 to numGames
    if (iter+1)%printIter==0:
        print(f"iter: {iter+1}/{numGames}: ", f"cumReward: {cumReward} ", f"numWin, numDraw numLose: {numWin}, {numDraw}, {numLose}")
        cumReward = 0
        numWin=0
        numDraw=0
        numLose=0

        
 
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
    
        
        
        





