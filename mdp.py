import random
# state = (playerCardValueExcludingAces, dealerCardValue, numAces)
# dealerCardValue belongs to {1, 2, 3, 4, ..., 10}

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
            numAces+=1
            
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
        return playerCardValue+numAces
    if playerCardValue+numAces == 21 or playerCardValue+numAces*11 == 21:
        return 21
    if playerCardValue+numAces < 21:
        if playerCardValue+numAces*11 > 21:
            return playerCardValue+numAces
        else:
            return playerCardValue+numAces*11
    
def computeDealerTotalValue(dealerCards):
    dealerCardValue, numAces = getDealerCardValueExcludeAce(dealerCards)
    if dealerCardValue+numAces > 21:
        return dealerCardValue+numAces
    if dealerCardValue+numAces == 21 or dealerCardValue+numAces*11 == 21:
        return 21
    if dealerCardValue+numAces<21:
        if dealerCardValue+numAces*11 > 21:
            return dealerCardValue+numAces
        else:
            return dealerCardValue+numAces*11

def dealerPlay(dealerCards, deck, playerCards):
    dealerCardValue, numAcesDealer = getDealerCardValueExcludeAce(dealerCards)

    while dealerCardValue+numAcesDealer < 17 or dealerCardValue+numAcesDealer*11 < 17:
        dealCard(deck, dealerCards, playerCards, isToPlayer = False)
        dealerCardValue, numAcesDealer = getDealerCardValueExcludeAce(dealerCards)
    
    dealerFinal = computeDealerTotalValue(dealerCards)
    playerFinal = computePlayerTotalValue(playerCards)
    reward = 0
    if dealerFinal > 21:
        reward = 1
    elif dealerFinal < playerFinal:
        reward = 1
    elif dealerFinal == playerFinal:
        reward == 0
    else:
        reward = -1
        
    return reward

def isTerminal(state):
    playerCardValue, dealerCard, numAces = state
    if playerCardValue+numAces > 21 or playerCardValue+numAces == 21 or playerCardValue+numAces*11 == 21:
        return True
    else:
        return False
    
        
    