
from random import randint

def signed():
    return(["sjohnson101"])


def newDeck(n=10, suits=('spades', 'hearts', 'clubs', 'diamonds')):
    return[(value,suit) for suit in suits for value in range(1,n+1)]

def displayCard(c):
    '''Returns a string representation of card c, a tuple.'''
    suits = {'spades':'\u2660', 'hearts':'\u2661',
             'diamonds':'\u2662', 'clubs':'\u2663'}
    return(''.join( [ str(c[0]), suits[c[1]] ] ))




def shuffle(D):
    n=len(D) #setting a variable equal to the length of variable
    for i in range(n-1,0,-1): # for loop for being within these parameters
        j=random.randint(0,i)# generates random indices from the seleced range
        D[i],D[j]=D[j],D[i] #swaps elements
        # no return or print statement here
    

import random

def cut(D):
   if len(D)<2: #if the length of list D is less than two, there is no arragement
       return
   slicepoint=random.randint(1,len(D)-1)#function that will allow for random slice
   front=D[:slicepoint]#slices front half
   back=D[slicepoint:]#sliices back half
   D[:]= back + front #returns D as a full modified set, rearranging front and back
       

def deal(D, H):
    num=len(H) #sets num equal to the length of N lists
    cards_dealt=3 #number of cards dealt
    total_cards_needed=num*cards_dealt#total cards needed 
    if len(D)<total_cards_needed:# if there are fewer cards than needed
        cards_to_deal=len(D) #setting length of deck equal to cards needed to deal
    else:
        cards_to_deal=total_cards_needed#setting num* cards dealt equal to cards to deal
    for i in range(cards_to_deal):# for value in range of cards_to_deal
        p_index=i%num # determines player index
        H[p_index].append(D[i])# adds cards to a player's hand
    del D[:cards_to_deal] # removes already dealt cards
    

def inputMove(i, T, H):
    '''Solicit a move, defined as (c, M), where c is the index of a card
       in this player's hand, and M, a (possibly empty) list of
       indexes of cards on the table that sum to the value of c. If M
       is empty, the move is a discard.'''
    # Prompt player i for card to play from H[i].
    while True:
        # Capture any errors from non-integer inputs.
        try:
            c = int(input('Play which card? '))
            # Validate the input; try again if not valid.
            if c < len(T) or c > len(T) + len(H[i]):
                # Invalid card index.
                continue;
            # Good input; normalize to make it wrt to H and not H+T,
            # then abort the loop.
            c = c - len(T)
            break
        except:
            # Wonky input: trap the error and try again.
            print('Choose an index from hand.')
            pass
    # Prompt player i for list of indeces to match.
    while True:
        # Capture any errors from non-integer inputs.
        try:
            M = [ int(m) for m in input('Select matching indexes separated by spaces (blank to discard): ').split() ]
            # Validate the input.
            if not all( [ 0 <= m < len(T) for m in M ] ):
                # Invalid card indexes.
                continue;
            elif M and H[i][c][0] != sum( [ T[m][0] for m in M ] ):
                # Invalid card values (don't add up).
                continue;
            # Good input: abort the loop.
            break
        except:
            # Wonky input: trap the error and try again.
            print('Enter list of indexes separated by spaces.')
            pass
    return((c, M))



def selectMove(i, T, H):
    '''Automatically select a move, defined as (c, M), where c is the
       index of a card from this player's hand, and M, a (possibly
       empty) tuple of indexes of cards on the table that sum to the
       value of c (an empty M represents a discard). '''

    
    def findMoves(value, i=0, match=(), result=[()]):
        if value == 0:
            return(result + [match])
        elif i==len(T) or value < 0:
            return(result)
        result = findMoves(value-T[i][0], i+1, match+(i,), result)
        return(findMoves(value, i+1, match, result))

    
    #loop through each card in the player's hand
    for card_indx,card in enumerate(H[i]):
        value=card[0] #assuming first element is value
        #get possible moves for card
        possible_moves=findMoves(value)
        # define valid moves 
        valid_moves=[move for move in possible_moves if move]
        # if not within valid moves, it iterates over the rest
        if not valid_moves:
            continue
        #selects at random a valid move using random import
        chosen_move=random.choice(valid_moves)
        #returns index of card and chosen move
        return (card_indx,list(chosen_move))
    # if no moves are found
    return (0,[])



    
def updateScores(C, S, W):
#initialize variables for later use
    max_ori_player=-1
    max_ori_count=0
    max_cards_player=-1
    max_cards_count=0
    primiera_scores=[0]*len(C)
    for i in range(len(C)): #Determine who has the mos ori and who has most cards
        ori_count=C[i].count('ori') # assuming 'ori' is a placedholder for gold
        card_count=len(C[i])
        if ori_count>max_ori_count: #updates the maximum ori
            max_ori_count=ori_count
            max_ori_player=i
        if card_count>max_cards_count:# update max cards
            max_cards_count=card_count
            max_cards_player=i
        # calculate primiera score for player
        primiera_scores[i] = ori_count
        #updates scores
    if max_ori_player!=-1:
        S[max_ori_player]+=1# Sette Bello
    if max_cards_player!=-1:
         S[max_cards_player]+=1#Most cards
    #Update for best primiera
    best_primiera_player=primiera_scores.index(max(primiera_scores))
    S[best_primiera_player]+=1 # best score increment
        #check if scores exceed W
    return any(score>W for score in S)
        
        
            
    

def play(N=2, K=10, suits=('spades', 'hearts', 'clubs', 'diamonds'), W=11):
    '''Manages a game up to W points for N players using a len(S)*N deck of cards.'''
    S = [ 0 ] * N		   # Player scores (human is S[0])
    # Record last player to take a card from T

    # Play a game.
    while max(S) < W:
        D = newDeck(K, suits)	       # Create a deck
        H = [ [] for i in range(N) ]   # Player hands (human is H[0])
        C = [ [] for i in range(N) ]   # Player's capture pile (human is C[0])
        last = None                    # Last player to capture from table
        # Play the hand.
        while D:
            # Cut the deck and deal the cards.
            print("\n=========\nDealing...", end='')
            # Shuffle the deck.
            shuffle(D)
            # Cut the deck.
            cut(D)
            # Deal 3 cards to each player in H.
            deal(D, H)
            # Create a list T representing the table, and populate it with
            # the first 4 cards from what remains of D (make sure to
            # remove cards on T from what remains of D).
            T,D[:4] = D[:4],[]
            print("{} cards remain".format(len(D)))

            # Hand continues while the first player's hand is not empty.
            while H[0]:
                # For each player.
                for i in range(0, len(H)):
                    if not H[i]:
                        break
                    
                    
                    print("\n=========\nPlayer {}'s turn:".format(i))
                    print('  Table:  {}'.format(', '.join([ "[{}] {}".format(i, displayCard(T[i])) for i in range(len(T)) ] )))

                    if i == 0:
                        # Human player
                        print('  MyHand: {}'.format(', '.join([ "[{}] {}".format(j+len(T), displayCard(H[i][j])) for j in range(len(H)) if j<len(H[i]) ] )))
                        (c, M) = inputMove(i, T, H)
                    else:
                        # Auto player
                        (c, M) = selectMove(i, T, H)

                    
                    played_card=H[i][c]# card being played
                    H[i].pop(c) #remove played card from hand
                    
                    if M: # if M is not empty
                        captured_cards=[T[index] for index in M]#obtains captures
                        for index in sorted(M,reverse=True):#removes captures
                            del T[index]
                        C[i].extend(captured_cards)# add captured cards to player pile
                        last=i #update last to current player
                        print(f"Player {i} played {played_card} and captured cards {captured_cards}.")
                    else:# if M is empty you discard
                        print(f"Player {i} played {played_card} and discarded it.")
                    if M and not T:
                        print("\n=========\nScopa! Scopa!\n=========\n")
                        S[i] = S[i]+1

            if T:
                print("Done: awarding {} from table to Player {}".format(', '.join([ displayCard(c) for c in T ]), last))
                C[last].extend(T)
            if updateScores(C, S, W):
                break

    # Game over. Indicate who won.
    print("Game over: Player {} wins with a score of {} points.".format(S.index(max(S)), S[S.index(max(S))]))
