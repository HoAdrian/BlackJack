import random
# state = (playerCardValueExcludingAces, dealerCardValue, numAces)
# dealerCardValue belongs to {1, 2, 3, 4, ..., 10}

"""
Author: Shing Hei Ho (Adrian)
"""
###### helper method of the world dynamics #######

def dealCard(deck, dealerCards, playerCards, isToPlayer):
    card = random.choice(deck)
    deck.remove(card)
    if isToPlayer:
        playerCards[card] = playerCards.get(card, 0) + 1
    else:
        dealerCards.append(card)
    return card

def getPlayerCardValueExcludeAce(playerCards):
    cardValuesExcludeAces = 0
    numAces = 0
    for card, count in playerCards.items():
        if card != 1:
            cardValuesExcludeAces += card * count
        else:
            numAces+=count
            
    return cardValuesExcludeAces, numAces

    
def getDealerCardValueExcludeAce(dealerCards):
    cardValuesExcludeAces = 0
    numAces = 0
    for card in dealerCards:
        if card != 1:
            cardValuesExcludeAces += card
        else:
            numAces+=1
            
    return cardValuesExcludeAces, numAces

def computePlayerTotalValue(playerCards):
    playerCardValue, numAces = getPlayerCardValueExcludeAce(playerCards)
    
    if playerCardValue+numAces > 21:
        #bust
        return playerCardValue+numAces
    
    # values by caes
    if numAces==0:
        return playerCardValue
    elif numAces==1:
        options = [playerCardValue+1, playerCardValue+11]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    elif numAces==2:
        options = [playerCardValue+2, playerCardValue+11+1]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    elif numAces==3:
        options = [playerCardValue+3, playerCardValue+11+2]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    elif numAces==4:
        options = [playerCardValue+4, playerCardValue+11+3]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    
def computeDealerTotalValue(dealerCards):
    dealerCardValue, numAces = getDealerCardValueExcludeAce(dealerCards)
    
    if dealerCardValue+numAces > 21:
        #bust
        return dealerCardValue+numAces
    
    # values by caes
    if numAces==0:
        return dealerCardValue
    elif numAces==1:
        options = [dealerCardValue+1, dealerCardValue+11]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    elif numAces==2:
        options = [dealerCardValue+2, dealerCardValue+11+1]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    elif numAces==3:
        options = [dealerCardValue+3, dealerCardValue+11+2]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    elif numAces==4:
        options = [dealerCardValue+4, dealerCardValue+11+3]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue
    
    
def getLegalActions(state):
        if isTerminal(state):
            return []
        else:
            return ["hit", "stand"]
        
def isTerminal(state):
    playerCardValue, _, numAces = state
    if playerCardValue+numAces > 21:
        #bust
        return True
    
    # values by caes
    if numAces==0:
        return playerCardValue==21
    elif numAces==1:
        options = [playerCardValue+1, playerCardValue+11]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue==21
    elif numAces==2:
        options = [playerCardValue+2, playerCardValue+11+1]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue==21
    elif numAces==3:
        options = [playerCardValue+3, playerCardValue+11+2]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue==21
    elif numAces==4:
        options = [playerCardValue+4, playerCardValue+11+3]
        bestValue = 0
        for value in options:
            if value <= 21 and value > bestValue:
                bestValue = value
        return bestValue==21
    


def dealerPlay(dealerCards, deck, playerCards):
    dealerTotal = computeDealerTotalValue(dealerCards)

    while dealerTotal < 17:
        dealCard(deck, dealerCards, playerCards, isToPlayer = False)
        dealerTotal = computeDealerTotalValue(dealerCards)
    
    dealerTotal = computeDealerTotalValue(dealerCards)
    playerTotal = computePlayerTotalValue(playerCards)
    reward = 0.0
    if dealerTotal > 21:
        reward = 1.0
    elif dealerTotal < playerTotal:
        reward = 1.0
    elif dealerTotal == playerTotal:
        reward == 0.0
    else:
        reward = -1.0
        
    return reward
    
        
    