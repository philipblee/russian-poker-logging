# using Tkinter to display a hand of 13 random card images
# each time you click the canvas
# this program runs in python27
# program needs Cards_gif to get card images and Probability1Wild.csv
#TODO-cl use IDE - pycharm
#TODO-cl use Github for version control
#TODO-cl use logging
#TODO-cl use more object-oriented
#TODO-cl use unittest
#TODO-cl use machine learning
#TODO-pl improve performance
#TODO-pl branch to Pyramid Poker
#TODO-pl create output which stores cards and results only
#TODO-pl merge Interactive and Batch
#TODO-pl performance testing
#TODO-pl clean up code in general
#TODO-pl change "Probability0Wild.csv" file at runtime
#TODO-pl put key variables into PARAMETERS
import time
from Tkinter import *
import sys
from random import shuffle
import csv
import logging
logging.basicConfig(format='%(asctime)s:%(levelno)s:%(funcName)s:%(message)s',
                    filemode="w", filename= "russian-output.txt", level=logging.WARN)

f = open ('card_list2.csv', 'w')
prob_file = False
prob_chart = [0,0,0]
prob_chart = 1200 * [prob_chart]
prob_array1 = [0,0,0]
prob_array1 = 600 * [prob_array1]
prob_array2 = [0,0,0]
prob_array2 = 600 * [prob_array2]
prob_array3 = [0,0,0]
prob_array3 = 600 * [prob_array3]

class Hand(list):
  pass

class Deck(object):
  suit = 1*'SHDC'
  rank = 'AKQJT98765432'
  
  def deal(self, n):
    deck = [s+r for s in Deck.suit for r in Deck.rank]
    #deck.append("WX")
    for i in range(1):
        shuffle(deck)
    return [Hand(deck[i::n]) for i in xrange(n)]

  @staticmethod
  def cmpkey(card):
    return Deck.suit.index(card[0]), Deck.rank.index(card[1])

def rank_sort(a,b):
    suit = "SHDC"
    rank = "23456789TJQKA"
    if rank.index(a[1]) > rank.index(b[1]):
        return 1
    return -1
  
def straightcount (rankcount):
    """ count straights - takes in rankcount(list of ranks), and returns straightct
        array with straights in straightct [1:10] - if 1, it's A2345, if 2 it's23456
        finally straightct [15] = total number of straights
        used mainly by analyze()"""
    straightct = 16 * [0]
    for i in range(1,11):
        straightct [i] = 1
        for j in range (0,5):
            if rankcount[i+j] == 0:
                straightct[i] = 0
    straightct[15] = sum(straightct[1:11])
    return (straightct)

def analyze (card_list):
    """ returns suit_rank_array[i] where i is row
     0 - S           6 - SF S        10 - singles_list    15 - S_list
     1 - H           7 - SF H        11 - pairs_list      16 - H_list
     2 - D           8 - SF D        12 - trips_list      17 - D_list
     3 - C           9 - SF C        13 - fourks_list     18 - C_list
     4 - Frequency                   14 - fiveks_list
     5 - Straights                        
     column 15 is always sum of row - for flushes [5][15]
     """
    suits = "SHDC"
    ranks = "123456789TJQKA"
    
    x = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    suit_rank_array = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [],[],[],[],[],[],[],[],[]]
    #print " 0",
    for card in card_list:
        suit_int = suits.index(card[0]) #0:3
        rank_int = ranks.index(card[1]) + 1 #1:14
        suit_rank_array[suit_int][rank_int] += 1 #increment[i][j] by 1

    for i in range (4): # count number of cards per suit
        suit_rank_array[i][1] = suit_rank_array[i][14]  #set up Ace as 1 for straights
        suit_rank_array[i][15] = sum(suit_rank_array[i][0:14]) #put suit frequency in 15

    suit_rank_array[6][14] = suit_rank_array[6][15] + suit_rank_array[7][15] + \
                      suit_rank_array[8][15] + suit_rank_array[9][15] #straightflushes

    flushes = 0  # count flushes
    for i in range(4):
        if suit_rank_array[i][15] >= 5:
             flushes = flushes + 1
    suit_rank_array[4][15] = flushes #store sum of flushes in [4][15]
    
    for i in range(4):
        for j in range(1,15):
            suit_rank_array[4][j] += suit_rank_array[i][j]

    #print suit_rank_array[4], "rank freq/flush sum"

    # 5 card straights
    suit_rank_array[5] = straightcount(suit_rank_array[4])
    no_straight =  True
    #print suit_rank_array[5], "straights"

    # 5 card straight flush
    for i in range (6,10):
        suit_rank_array[i] = straightcount(suit_rank_array[i-6])
        #print suit_rank_array[i], "SF", suits[i-6]

    ranks = "0123456789TJQKA"
    hand_x = []
    card_id = []
    
    # Go through all 15 ranks and count singles, pairs, trips, etc.
    for j in range(14,1,-1):      
        if suit_rank_array[4][j] == 1:
            suit_rank_array[10].append(ranks[j])
        if suit_rank_array[4][j] == 2:
            suit_rank_array[11].append(ranks[j])
        if suit_rank_array[4][j] == 3: 
            suit_rank_array[12].append(ranks[j])
        if suit_rank_array[4][j] == 4:
            suit_rank_array[13].append(ranks[j])
        if suit_rank_array[4][j] == 5:
            suit_rank_array[14].append(ranks[j])
        for i in range (4):
           if suit_rank_array[i][j] >= 1:
              suit_rank_array[15+i].append(ranks[j])
              
##    for i in range(10,19):
##        print i, suit_rank_array[i], len(suit_rank_array[i])
              
    return (suit_rank_array)

def best_13card_hand(card_list2):
    card_list = list(card_list2)
    card_list2_string = ""
    for i in card_list2:
        card_list2_string = card_list2_string + i + ","
    suits = "SHDC"
    ranks = "0A23456789TJQKA"
    suit_rank_array = analyze(card_list2)
    straightflushes = suit_rank_array[6][14]
    flushes = suit_rank_array[4][15]
    straights = suit_rank_array[5][15]
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]
    singles = len(singles_list)
    pairs = len(pairs_list)
    trips = len(trips_list)
    fourks = len(fourks_list)
    fiveks = len(fiveks_list)

    for i in range(6):
        logging.debug((i, suit_rank_array[i]))
    if straightflushes > 1:
        for i in range(6, 10):
            logging.debug((i, suit_rank_array[i]))
    for i in range(10, 19):
        logging.debug((i, suit_rank_array[i]))

    hand3 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [],
             [], [], [], [], [], [], [], [], [], [], [], [], []]

    hand2 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [],
             [], [], [], [], [], [], [], [], [], [], [], [], []]

    hand1 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [],
             [], [], [], [], [], [], [], [], [], [], [], [], []]

    valid_hand = [True]
    valid_hand = 25 * valid_hand

    score_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    cards_remaining = [[], [], [], [], [], [], [], [], [], [], [], [], [], [],
                       [], [], [], [], [], [], [], [], [], [], [], [], []]

    # for each hand_x in hand3, get hand2 with score and then get hand1
    hand3 = best_hand3(card_list2)

    hand_num = 0
    card_z = []
    for hand_x in hand3:
        if len(hand_x) > 0:
            sorted(hand_x, cmp=rank_sort, reverse=True)
            # print "sorted hand_x", hand_x
            score_array[3][hand_num] = score(hand3[hand_num], "3")
            cards_remaining[hand_num] = list(card_list)
            for card_x in hand_x:
                for card_y in cards_remaining[hand_num]:
                    if card_x == card_y:
                        cards_remaining[hand_num].remove(card_y)
            logging.info((hand3[hand_num], score_array[3][hand_num]))
            logging.info(("cards_rem - hand2", cards_remaining[hand_num]))

            hand2[hand_num] = best_hand2(cards_remaining[hand_num], score_array[3][hand_num])
            score_array[2][hand_num] = score(hand2[hand_num], "2")
            # print "hand2", hand2[hand_num], score_array[2][hand_num]
            for card_x in hand2[hand_num]:
                for card_y in cards_remaining[hand_num]:
                    if card_x == card_y:
                        cards_remaining[hand_num].remove(card_x)
            logging.info((hand2[hand_num], score_array[2][hand_num]))
            logging.info(("cards_rem hand1", cards_remaining[hand_num]))

            hand1[hand_num] = best_hand1(cards_remaining[hand_num], score_array[2][hand_num])
            for card_x in hand1[hand_num]:
                for card_y in cards_remaining[hand_num]:
                    if card_x == card_y:
                        cards_remaining[hand_num].remove(card_x)
            score_array[1][hand_num] = score(hand1[hand_num], "1")
            logging.info((hand1[hand_num], score_array[1][hand_num]))
            logging.info(("cards_rem fillers", cards_remaining[hand_num]))
            cards_remaining[hand_num] = sorted(cards_remaining[hand_num], cmp=rank_sort, reverse = True)
            # print "hand1 cards remaining", cards_remaining[hand_num]
            while (len(hand1[hand_num]) < 3 and len(cards_remaining[hand_num]) > 0):
                card_z = cards_remaining[hand_num][0]
                hand1[hand_num].append(card_z)
                cards_remaining[hand_num].remove(card_z)

            while (len(hand2[hand_num]) < 5 and len(cards_remaining[hand_num]) > 0):
                card_z = cards_remaining[hand_num][0]
                hand2[hand_num].append(card_z)
                cards_remaining[hand_num].remove(card_z)

            while (len(hand3[hand_num]) < 5 and len(cards_remaining[hand_num]) > 0):
                # print "filler3", cards_remaining[hand_num][0]
                card_z = cards_remaining[hand_num][0]
                hand3[hand_num].append(card_z)
                cards_remaining[hand_num].remove(card_z)


            hand3[hand_num] = sorted(hand3[hand_num], cmp=rank_sort, reverse=True)
            hand2[hand_num] = sorted(hand2[hand_num], cmp=rank_sort, reverse=True)
            hand1[hand_num] = sorted(hand1[hand_num], cmp=rank_sort, reverse=True)
            total_score = score_array[3][hand_num][1] + score_array[2][hand_num][1] + score_array[1][hand_num][1]

            logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
            logging.info((hand_num, hand2[hand_num], score_array[2][hand_num]))
            logging.info((hand_num, hand1[hand_num], score_array[1][hand_num]))
            logging.info((total_score))
            hand_num = hand_num + 1

    # print "Searching for Valid Hands"
    for i in range(hand_num):
        score_array[3][i] = score_final(hand3[i], "3")
        score_array[2][i] = score_final(hand2[i], "2")
        score_array[1][i] = score_final(hand1[i], "1")

    for i in range(hand_num):
        is_valid_hand = True
        if score_array[1][i][0] > score_array[2][i][0]:
            is_valid_hand = False
        if score_array[2][i][0] > score_array[3][i][0]:
            is_valid_hand = False
        if is_valid_hand == False:
            valid_hand[i] = False  # marks valid_hand{i] False
            logging.warning(("Invalid Hand", i, score_array[3][i], score_array[2][i], score_array[1][i]))

    # Find best_hand based on total_score
    best_total_score = 0
    best_hand_score = [0,0], [0,0], [0,0], 0
    best_hand = 0
    for i in range(hand_num):
        total_score = round(score_array[3][i][1] + score_array[2][i][1] + score_array[1][i][1],3)
        logging.info((i, score_array[3][i][1], score_array[2][i][1], score_array[1][i][1], total_score, valid_hand[i]))
        if total_score > best_total_score and valid_hand[i]:
            best_total_score = total_score
            best_hand = i
            best_hand_score = score_array[3][best_hand], score_array[2][best_hand], score_array[1][best_hand], best_total_score
    logging.info(("best", best_hand, score_array[3][best_hand], score_array[2][best_hand], score_array[1][best_hand],
                  best_total_score, valid_hand[best_hand]))

    card_list_string = str(best_hand) + ", "
    for i in range(3, 0, -1):
        for j in range(2):
            # print "i, j, score_array[i][best_hand]", i, j, score_array[i][best_hand]
            card_list_string += str(score_array[i][best_hand][j]) + ", "
    card_list_string += str(best_total_score) + "\n"
    # print card_list_string

    card_listx = hand3[best_hand] + hand2[best_hand] + hand1[best_hand]
    # print "best_hand", card_listx
    return [card_listx, best_hand_score]

def best_hand3(card_list2):
    """ best_hand3 must find all plausible hand3's by hand type in order
        5K's, SF's, 4K's, FH's, Flushes', Straights', Trip's, 2Ps and P's.
        Each one creates a new hand3[hand_num]
    """
    card_list = list(card_list2)
    suit_rank_array = analyze(card_list2)
    suits = "SHDC"
    ranks = "0A23456789TJQKA"

    straightflushes = suit_rank_array[6][14]
    flushes = suit_rank_array[4][15]
    straights = suit_rank_array[5][15]
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]

    singles = len(singles_list)
    pairs = len(pairs_list)
    trips = len(trips_list)
    fourks = len(fourks_list)
    fiveks = len(fiveks_list)

    for i in range(6):
        logging.debug((i, suit_rank_array[i]))
    if straightflushes > 1:
        for i in range(6, 10):
            logging.debug((i, suit_rank_array[i]))
    for i in range(10, 19):
        logging.debug((i, suit_rank_array[i]))

    hand3 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [],
             [], [], [], [], [], [], [], [], [], [], [], [], []]

    valid_hand = [True]
    valid_hand = 25 * valid_hand

    score_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    hand_num = 0
    for j in range(14, 1, -1):  # fivek
        if suit_rank_array[4][j] == 5:
            for card in card_list2:
                if ranks[j] in card:
                    hand3[hand_num].append(card)
            score_array[3][hand_num] = score(hand3[hand_num], "3")
            logging.info((((hand_num, hand3[hand_num])), score_array[3][hand_num]))
            hand_num = hand_num + 1

    for i in range(4):  # straight flush
        for j in range(1, 11):
            if suit_rank_array[i + 6][j] >= 1:
                for k in range(5):
                    card = suits[i] + ranks[j + k]
                    hand3[hand_num].append(card)
                score_array[3][hand_num] = score(hand3[hand_num], "3")
                logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
                hand_num = hand_num + 1

    for j in range(14, 1, -1):  # fourk
        if suit_rank_array[4][j] == 4:
            for card in card_list2:
                if ranks[j] in card:
                    hand3[hand_num].append(card)
            score_array[3][hand_num] = score(hand3[hand_num], "3")
            logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
            hand_num = hand_num + 1

    for j in range(14, 1, -1):  # full house with one or more pairs
        if suit_rank_array[4][j] == 3 and len(pairs_list) >= 1:  # find trips
            pair_card = pairs_list[-1]
            for card in card_list2:
                if ranks[j] in card or pair_card in card:
                    hand3[hand_num].append(card)
            score_array[3][hand_num] = score(hand3[hand_num], "3")
            logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
            hand_num = hand_num + 1

    for i in range(4):  # flush
        if suit_rank_array[i][15] >= 5:
            for card in card_list2:
                if suits[i] in card:
                    hand3[hand_num].append(card)
            if len(hand3[hand_num]) > 5:
                hand3[hand_num] = flush_overage(hand3[hand_num], card_list2)
            score_array[3][hand_num] = score(hand3[hand_num], "3")
            logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
            hand_num = hand_num + 1

    for j in range(11, 0, -1):  # straight
        if suit_rank_array[5][j] >= 1:
            for k in range(5):
                n = 0
                for card in card_list2:
                    if ranks[j + k] in card and n == 0:
                        hand3[hand_num].append(card)
                        n = 1
            score_array[3][hand_num] = score(hand3[hand_num], "3")
            logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
            hand_num = hand_num + 1

    for j in range(14, 1, -1):  # trips
        if suit_rank_array[4][j] == 3:
            for card in card_list2:
                if ranks[j] in card:
                    hand3[hand_num].append(card)
            score_array[3][hand_num] = score(hand3[hand_num], "3")
            logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
            hand_num = hand_num + 1

    if pairs == 6 and len(trips_list) == 0:  # create two pairs from 6 pairs
        for card in card_list2:
            if pairs_list[-2] in card:
                hand3[hand_num].append(card)
            if pairs_list[1] in card:
                hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num], "3")
        logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
        hand_num = hand_num + 1

    if pairs == 5 and len(trips_list) == 0:  # create two pairs from 5 pairs
        for card in card_list2:
            if pairs_list[-1] in card:
                hand3[hand_num].append(card)
            if pairs_list[1] in card:
                hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num], "3")
        logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
        hand_num = hand_num + 1

    if pairs == 4 and len(trips_list) == 0:  # create two pairs from 4 pairs
        for card in card_list2:  # worst two pairs to play pair, pair, 2p
            if pairs_list[-1] in card:
                hand3[hand_num].append(card)
            if pairs_list[-2] in card:
                hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num], "3")
        logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
        hand_num = hand_num + 1

        for card in card_list2:  # pair[0] and pair[-1] to play mo, 2p, 2p
            if pairs_list[0] in card:
                hand3[hand_num].append(card)
            if pairs_list[-1] in card:
                hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num], "3")
        logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
        hand_num = hand_num + 1

    if (pairs == 3 or pairs == 2) and len(trips_list) == 0:  # use largest pair
        for card in card_list2:
            if pairs_list[0] in card:
                hand3[hand_num].append(card)
        score_array[3][hand_num] = score(hand3[hand_num], "3")
        logging.info((hand_num, hand3[hand_num], score_array[3][hand_num]))
        hand_num = hand_num + 1
    return hand3

def best_hand2(card_listx, score_prob):
    ##logger.debug('Entering module')

    """ Given card_listx, return hand_x which is best 5 card hand"""
    logging.info ((card_listx, score_prob))
    previous_hand_score = score_prob[0]
    suit_rank_array = analyze(card_listx)
    
    suits = "SHDC"
    ranks = "0123456789TJQKA"
    ranks_straight = "0A23456789TJQKA"
    hand_x = []
    card_id = []

    straightflushes = suit_rank_array[6][14]
    flushes = suit_rank_array[4][15]
    straights = suit_rank_array[5][15]
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]
    
    for i in range(6):
        logging.debug((i, suit_rank_array[i]))
    if straightflushes >= 1:
        for i in range(6,10):
            logging.debug((i, suit_rank_array[i]))
    for i in range(10,19):
        logging.debug((i, suit_rank_array[i]))

    # If hand3 was a King house with score of 71300, we need to
    # prevent a house of Aces in hand2.  The solution was to introduce
    # the lowest possible hand of each hand type.  So if
    # lowest_house_score is 71400 (Ace House), then the house hand type
    # would be skipped over.  If there was a 71200 (Q House), then
    # house hand type would be played

    lowest_straightflush_score = 100000
    lowest_fourks_score = 90000
    lowest_house_score = 80000
    lowest_flush_score = 70000
    lowest_straight_score = 60000
    lowest_trip_score = 50000
    lowest_twopair_score = 40000
    lowest_pair_score = 30000
    lowest_highcard_score = 20000

    if len(fourks_list) >= 1:
        lowest_fourks_score = 80000 + ranks.index(fourks_list[-1]) * 100

    if len(trips_list) >= 1 and len(pairs_list) >=1:
        lowest_house_score = 700000 + 100 * ranks.index(trips_list[-1]) + ranks.index(pairs_list[-1])

    if flushes >= 1:
        for i in range(0,4):
            if suit_rank_array[i][15] >= 5:
                flush_score = 60000 + ranks.index(suit_rank_array[i+15][0]) * 100 + ranks.index(suit_rank_array[i+15][1])
                if flush_score < lowest_flush_score:
                    lowest_flush_score = flush_score

    if straights >= 1:
        for j in range(2,10):
            if suit_rank_array[5][j] >= 1:
                lowest_straight_score = 50000 + (j+4) * 100 + j+3

    if len(trips_list) >= 1:
        lowest_trip_score = 40000 + ranks.index(trips_list[-1]) * 100

    if len(pairs_list) == 3:
        lowest_twopair_score = 30000 + ranks.index(pairs_list[-1]) * 100 + ranks.index(pairs_list[-2])

    if len(pairs_list) == 2:
        lowest_twopair_score = 30000 + ranks.index(pairs_list[-1]) * 100 + ranks.index(pairs_list[1])
        lowest_pair_score = 20000 + ranks.index(pairs_list[-1]) * 100

    if len(pairs_list) == 1:
        lowest_pair_score = 20000 + ranks.index(pairs_list[-1]) * 100

    if len(singles_list) >= 2:
        lowest_highcard_score = 10000 + ranks.index(singles_list[0]) * 100 + ranks.index(singles_list[1])

    if len(singles_list) == 1:
        lowest_highcard_score = 10000 + ranks.index(singles_list[0]) * 100

    logging.debug(("lowest sf, 4k, house", lowest_straightflush_score, lowest_fourks_score, lowest_house_score))
    logging.debug(("lowest flush, straight, trip",lowest_flush_score,lowest_straight_score,lowest_trip_score))
    logging.debug(("lowest 2P, P, HC",lowest_twopair_score,lowest_pair_score,lowest_highcard_score))
    logging.debug(("phs", previous_hand_score))

    # find best hand2 by going through all hand types from best to
    # worst.  5K, SF, 4K, FH, Flush, Straight, Trip, 2P, P, High Card
    # When the best is found, it must have a lowest_blank_score
    # that is less than previous_hand_score, or we would move to
    # next lower hand type

    if len(fiveks_list) > 0 and previous_hand_score >= 110000:
        card_id.append(fiveks_list[0])
        logging.info(("5K", fiveks_list))

    elif straightflushes >=1 and previous_hand_score >= 100000:
        for i in range(6,10):
            for j in range(2,11):
                if suit_rank_array[i][j] >= 1:
                    straight_score = 90000 + (j+4)*100 + j + 3
                    if straightflush_score < lowest_straightflush_score:
                        lowest_straightflush_score = straightflush_score

    elif len(fourks_list) > 0 and previous_hand_score >= lowest_fourks_score:
            card_id.append(fourks_list[0])
            logging.info(("4K", fourks_list))
        
    elif len(trips_list) >= 1 and len(pairs_list)>=1 and previous_hand_score >= lowest_house_score:
            card_id.append(trips_list[0])
            card_id.append(pairs_list[-1])
            logging.info(("Full House", trips_list[0], pairs_list[-1]))
 
    elif flushes >= 1 and previous_hand_score >= lowest_flush_score:
            for i in range(4):
               if suit_rank_array[i][15] >= 5:
                   card_id.append(suits[i])
            logging.info(("flush", suits[i], card_id))
        
    elif straights > 0 and previous_hand_score >= lowest_straight_score:
        straight_found = False
        for j in range (11,0,-1):   #straight
            if straight_found == False:
                if suit_rank_array[5][j] >= 1:
                    straight_found = True
                    for k in range (5):
                        n = 0  #looks for 1 per ranks[j+k]
                        for cardx in card_listx:
                            #print "cardx, ranks[j+k]", cardx, ranks[j+k]
                            if ranks_straight[j+k] in cardx:
                                 if n == 0:
                                    card_id.append(cardx)
                                    n = 1                   
        logging.info(("straight", card_id))

    elif len(trips_list)>= 1 and previous_hand_score >= lowest_trip_score:
        card_id.append(trips_list[0])
        logging.info(("trips", card_id))

    elif len(pairs_list) == 5 and previous_hand_score >= lowest_twopair_score:
            card_id.append(pairs_list[-1])
            card_id.append(pairs_list[-2])
            logging.info(("2 pairs of 5 pairs", card_id))
        
    elif len(pairs_list) == 4 and previous_hand_score >= lowest_twopair_score:
            card_id.append(pairs_list[-1])
            card_id.append(pairs_list[1])
            logging.info(("2 pairs of 4 pairs", card_id))
        
    elif len(pairs_list) == 3 and previous_hand_score > lowest_twopair_score:
            card_id.append(pairs_list[-1])
            card_id.append(pairs_list[-2])
            logging.info(("2 pairs of 3 pairs", card_id))

    elif (len(pairs_list) == 2) and previous_hand_score > lowest_pair_score:
            logging.info(("pairs_list", pairs_list))
            card_id.append(pairs_list[0])

    elif (len(pairs_list) == 1) and previous_hand_score > lowest_pair_score:
            logging.info(("pairs_list", pairs_list))
            card_id.append(pairs_list[0])

    elif len(singles_list) >= 1 and previous_hand_score >= lowest_highcard_score:
        for single in singles_list:
            card_id.append(single)
            break
        logging.info(("high card", card_id))
    else:
        logging.info(("nothing found"))
        pass
    logging.info(("card_id", card_id))
    only_five = 0
    if flushes > 0:
        for id in card_id:
            for cardx in card_listx:
                if id in cardx:
                    hand_x.append(cardx)
        hand_x = flush_overage(hand_x, card_listx)
    else:
        for id in card_id:
            for cardx in card_listx:
                #logging.info(("id", id, "cardx", cardx))
                if id in cardx:
                    hand_x.append(cardx)
    # if hand_x is more than 5 cards,                                   
    hand_x = sorted (hand_x, cmp = rank_sort, reverse= True)
    if len(hand_x) > 0:
        hand_x_score = score(hand_x, "2")
        logging.info((hand_x, hand_x_score))
    else:
        logging.warning(("Why is hand_x empty?", hand_x))
    return (hand_x)
  
def best_hand1(card_listx, score_prob):
    logging.info((card_listx, score_prob))
    if len(card_listx) == 0:
        logging.warn(("card_listx is empty, something is wrong"))
    """ Given card_listx, return hand_x which is best 3-card hand less than score_prob"""
    suit_rank_array = analyze(card_listx)
    previous_hand_score = score_prob[0]
    suits = "SHDC"
    ranks = "0A23456789TJQKA"
    hand_x = []
    card_id = []
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    
    # find best hand 3 card hand (mo, pair or trip only)
    logging.info((card_listx, score_prob))
    #print "hand2 cannot be > than", previous_hand_score

    if len(trips_list)>0 and len(pairs_list) == 0 and previous_hand_score > 40000:
        card_id.append(trips_list[0])
        #print "trips", card_id

    elif len(pairs_list) == 2 and previous_hand_score > 20000:
          #print "pairs_list", pairs_list
          card_id.append(pairs_list[0])
            
    elif len(pairs_list) == 1 and previous_hand_score > 20000:
          #print "pairs_list", pairs_list
          card_id.append(pairs_list[0])   
        
    elif len(singles_list) >= 3 and previous_hand_score > 10000:
          #print "singles_list", singles_list
          card_id.append(singles_list[0])
          card_id.append(singles_list[1])
          card_id.append(singles_list[2])
          
    else:
        #print "nothing found", card_id
        pass
        
    #print "card_id", card_id

    for id in card_id:
        for cardx in card_listx:
            #print "id", id, "cardx", cardx
            if id in cardx:
                hand_x.append(cardx)                              
    sorted (hand_x, cmp = rank_sort, reverse= True)
    logging.info(hand_x)#, score(hand_x,"1"))
    return (hand_x)
  
def flush_overage (card_listx, card_list2):
    ##logger.debug('Entering module')
    """ Is there a flush overage?
        If yes, return one card which is useful for cards_remaining hand
        If not, return empty"""
    suits = "SHDC"
    flush_overage_card = ""
    found = False
    #print "flush_overage", "card_listx", card_listx
    #print "flush_overage", "card_list2", card_list2
    suit_rank_array = analyze(card_list2)
    extra_cards = len(card_listx) - 5
    for i in range (extra_cards):
        #print "flush overage i", i
        if len(suit_rank_array[13]) > 0 and found == False: # if there are 4K
             for cardx in card_listx:
                 for y in suit_rank_array[13]:
                      if y in cardx:
                          found = True
                          #print "found 4K", cardx
                          flush_overage_card = cardx
                       
        if len(suit_rank_array[12]) > 0 and found == False: # if there are Trips
             for cardx in card_listx:
                  for y in suit_rank_array[12]:
                      if y in cardx:
                          found = True
                          #print "found Trips", cardx
                          flush_overage_card = cardx
                          
        #print "pairs", suit_rank_array[11]
        if len(suit_rank_array[11]) > 0 and found == False: # if there are Pairs 
             for cardx in card_listx:
                  if found == False:
                      for y in suit_rank_array[11]:
                          #print "y, cardx", y, cardx
                          if y in cardx:
                              found = True
                              flush_overage_card = cardx
        if found == False:
            flush_overage_card = card_listx[0]
            found = True
            
        if found == True:
            card_listx.remove(flush_overage_card)
            flush_overage_card = ""
            found = False
            #print "after removal", card_listx
            
    return card_listx

def score(card_listx, hand):
    #logger.debug('Entering module')
    """ given 1-5 cards, returns initial score and prob depending on hand 1,2 or 3"""
    suit_rank_array = analyze (card_listx)
    suits = "SHDC"
    ranks = "0123456789TJQKA"
    hand_x = []
    card_id = []
    straightflushes = suit_rank_array[6][14]
    flushes = suit_rank_array[4][15]
    straights = suit_rank_array[5][15]
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]

    for i in range(6,10):
        if suit_rank_array[i][15] >=1:
            straightflushes += 1
            straightflushsuit = i
            
    if len(fiveks_list) > 0:
        #print "5K", fiveks_list
        score = 100000
        score += ranks.index(suit_rank_array[14][0]) * 100
        
    # need to add straight flush
    elif straightflushes >=1:
        score = 90000
        score += ranks.index(suit_rank_array[straightflushsuit+9][0]) * 100 
        
    elif len(fourks_list) > 0:
        #print "4K", fourks_list
        score = 80000
        score += ranks.index(suit_rank_array[13][0]) * 100
        
    elif len(trips_list) > 0 and len(pairs_list)>=1:
        #print "Full House", trips_list[0], pairs_list[-1]
        score = 70000
        score += ranks.index(trips_list[0]) * 100 + ranks.index(pairs_list[-1])
 
    elif flushes > 0:
        for i in range(4):     #print "flush", card_id
           if suit_rank_array[i][15] >= 5:
               score = 60000
               #print "cards in flush", suit_rank_array[15+i]
               score += ranks.index(suit_rank_array[15+i][0]) * 100 + ranks.index(suit_rank_array[15+i][1])
    
    elif straights > 0:           
        for j in range (11,0,-1):   #straight
            if suit_rank_array[5][j] >= 1:
                score = 50000
                if j == 1:
                    score += 1402
                else:
                    score += (j+4)*100 #Highest card in straight
                    score += j+3 #next highest card in straight                    
        #print "straight", card_id

    elif len(trips_list)>0 and len(pairs_list) == 0:
        score = 40000
        score += ranks.index(trips_list[0]) * 100
        #print "trips", card_id
                    
    elif len(pairs_list) > 1:
        score = 30000
        score += ranks.index(pairs_list[0]) * 100 + ranks.index(pairs_list[-1])
        #print "2 pairs", card_id

    elif len(pairs_list) == 1:
        score = 20000
        score += ranks.index(pairs_list[0]) * 100

    else:
        #print "nothing found - high/2nd high cards", card_listx
        score = 10000
        if len(card_listx) > 0:
            score += ranks.index(card_listx[0][1]) * 100
            
    prob = win_prob(score, hand)
    
    if hand == "3":
        if score >= 100000:
            prob = prob * 6
        elif score >= 90000:
            prob = prob * 5
        elif score >= 80000:
            prob = prob * 4
    elif hand == "2":
        if score >= 100000:
            prob = prob * 12
        elif score >= 90000:
            prob = prob * 10
        elif score >= 80000:
            prob = prob * 8
        elif score >= 70000:
            prob = prob * 2
    elif hand == "1":
        if score >= 40000:
            prob = prob * 3
    logging.debug((card_listx, score))
    return (score, prob)

def score_final(card_listx, hand):   
    """ given either 3 or 5 cards, return score and prob depending on hand 1,2 or 3
        """
    suit_rank_array = analyze (card_listx)
    suits = "SHDC"
    ranks = "0123456789TJQKA"
    hand_x = []
    card_id = []

    straightflushes = suit_rank_array[6][14]
    flushes = suit_rank_array[4][15]
    straights = suit_rank_array[5][15]
    singles_list = suit_rank_array[10]
    pairs_list = suit_rank_array[11]
    trips_list = suit_rank_array[12]
    fourks_list = suit_rank_array[13]
    fiveks_list = suit_rank_array[14]

    for i in range(6,10):
        if suit_rank_array[i][15] >=1:
            straightflushsuit = i
            
    if len(fiveks_list) > 0:
        #print "5K", fiveks_list
        score = 100000
        score += ranks.index(suit_rank_array[14][0]) * 100
        
    # need to add straight flush
    elif straightflushes >=1:
        score = 90000
        score += ranks.index(suit_rank_array[straightflushsuit+9][0]) * 100
        
    elif len(fourks_list) > 0:
        #print "4K", fourks_list
        score = 80000
        score += ranks.index(suit_rank_array[13][0]) * 100
        
    elif len(trips_list) > 0 and len(pairs_list)>=1:
        #print "Full House", trips_list[0], pairs_list[-1]
        score = 70000
        score += ranks.index(trips_list[0]) * 100 + ranks.index(pairs_list[-1])
 
    elif flushes > 0:
        for i in range(4):     #print "flush", card_id
           if suit_rank_array[i][15] >= 5:
               score = 60000
               score += ranks.index(suit_rank_array[15+i][0]) * 100 + ranks.index(suit_rank_array[15+i][1])        

    elif straights > 0:           
        for j in range (11,0,-1):   #straight
            if suit_rank_array[5][j] >= 1:
                score = 50000
                if j == 1:
                    score += 1402
                else:
                    score += (j+4)*100 #Highest card in straight
                    score += j+3 #next highest card in straight

    elif len(trips_list)>0 and len(pairs_list) == 0:
        score = 40000
        score += ranks.index(trips_list[0]) * 100
        #print "trips", card_id
                    
    elif len(pairs_list) > 1:
        score = 30000
        score += ranks.index(pairs_list[0]) * 100 + ranks.index(pairs_list[-1])
        #print "2 pairs", card_id

    elif len(pairs_list) == 1:
        score = 20000
        score += ranks.index(pairs_list[0]) * 100
        if len(singles_list) > 0:
            score += ranks.index(singles_list[0]) 
        #print "singles_list", singles_list
        #print "high card", card_id

    else:
        #print "nothing found - high/2nd high cards", card_listx
        score = 10000
        if len(card_listx) > 0:
            score += ranks.index(card_listx[0][1]) * 100
            score += ranks.index(card_listx[1][1])
            logging.info(("singles only", card_listx, score))
            
    prob = win_prob(score, hand)
    # specials scoring
    if hand == "3":
        if  score >= 100000:
            prob = prob * 6
        elif score >= 90000:
            prob = prob * 5
        elif score >= 80000:
            prob = prob * 4
    elif hand == "2":
        if score >= 100000:
            prob = prob * 12
        elif score >= 90000:
            prob = prob * 10
        elif score >= 80000:
            prob = prob * 8
        elif score >= 70000:
            prob = prob * 2
    elif hand == "1":
        if score >= 40000:
            prob = prob * 3
    #print "debug score 1", score, hand, prob
    #print "score", card_listx, score
    return ([score, prob])

def win_prob(score, hand):
    global prob_file
    global prob_chart
    global prob_array
    global prob_hand
    if prob_file is False:
        with open("probability0wild.csv","rb") as f:
            reader = csv.reader(f)
            x = list(reader)
        prob_file = True
        inum = 0
        # store probability in b
        prob_hand = [0,0,0,0]
        for a in x:
            a[1], a[2] = int(a[1]), float(a[2])
            #logging.debug((inum, a))
            prob_chart[inum] = a
            inum += 1
        i = j = k = 0   
        for m in range(inum):
            #print prob_chart[m][0]
            if "1" in prob_chart[m][0]:
                prob_array1[i] = list(prob_chart[m])
                logging.debug((i, prob_array1[i]))
                i += 1
            if "2" in prob_chart[m][0]:
                prob_array2[j] = list(prob_chart[m])
                logging.debug((j, prob_array2[j]))
                j += 1
            if "3" in prob_chart[m][0]:
                prob_array3[k] = (list(prob_chart[m]))
                logging.debug((k, prob_array3[k]))
                k += 1
                
        prob_hand[1] = i
        prob_hand[2] = j
        prob_hand[3] = k

    index = 0

    if hand in prob_array1[0][0]:
        index = bin_search (prob_array1, prob_hand[1], score)
        prob = prob_array1[index][2]

    if hand in prob_array2[0][0]:
        index = bin_search (prob_array2, prob_hand[2], score)
        prob = prob_array2[index][2]
        
    if hand in prob_array3[0][0]:
        index = bin_search (prob_array3, prob_hand[3], score)
        prob = prob_array3[index][2]
        
    return prob

def bin_search(prob_array, items, score):
    orig_items = items
    for i in range(0, items):      
        if score > prob_array[i][1]:
            answer = i
            break
    low = 0
    high = items
    test = (high + low) / 2
    diff = high - low
    #print "before 1 ", diff
    while (diff > 3):
          #print "abs(score-prob[test]", score, test, prob_array[test][1]
          if score >= prob_array[test][1]:
                high = test
          if score <= prob_array[test][1]:
                low = test
          test = (high + low)/2
          diff = high - low
          #print "after 1 ", score, prob_array[test][1], low, high
                                        
    #print "after2", score, "from", low, "to", high, "iterations", answer-low     
    for i in range(low, high+5):      
        if score > prob_array[i][1]:
            index = i
            break
    #print "after 3", index
    return index