# using Tkinter to display a hand of 13 random card images
# each time you click the canvas
# (images are in GIF format for Tkinter to display properly)
import datetime
from deck_wild_logging_v4 import *
from Tkinter import *
from random import *

###########################################################
################### program begins  #######################
###########################################################
start_time = time.time()
f = open ('card_list2.csv', 'w')
card_list_string = "c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,x,h3,p3,h2,p2,h1,p1,total\n"
#print card_list_string
with open("card_list2.csv", "w") as f:
    f.write(card_list_string)

#PARAMETERS
NUMBER_OF_HANDS = 10

for k in range (NUMBER_OF_HANDS):
    if k%10 == 0:
        print k
    a = Deck().deal(4)
    for i in range (0,1):
        #print "=========== New Hand ==============="
        card_list = a[0]
    card_list2 = list (card_list[0:13])  #deal number_of_cards
    #print card_list2

    # wild_card_present = False
    # wild_card = "N/A"
    #
    # for cardx in card_list2:
    #     if cardx == "WX":
    #         wild_card_present = True
    #         card_list2.remove("WX")
    #
    # if wild_card_present == True:
    #     #print "wild card", wild_card_index
    #     #loop through all 52 cards
    #     wild_list = [s+r for s in "SHDC" for r in "23456789TJQKA"]
    #     best_wild_hand_score = 0
    #     best_wild_card_score = [0,0,0,0,0]
    #     best_wild_card = ""
    #     for wild_card in wild_list:
    #         card_list2.append(wild_card)
    #         #print "After wild", card_list2
    #         card_list1, best_hand_score = best_13card_hand(card_list2)
    #         #print wild_card, best_hand_score[0], best_hand_score[1], best_hand_score[2], best_hand_score[3]
    #         if best_hand_score[3] > best_wild_hand_score:
    #              best_wild_card_score = best_hand_score[0:4]
    #              best_wild_hand_score = best_hand_score[3]
    #              best_wild_card = wild_card
    #              #print best_wild_card, best_wild_hand_score
    #         #print "After best_13card", card_list1
    #         #print wild_card, best_hand_score
    #         card_list2.remove(wild_card)
    #     #print "best_wild_card", best_wild_card, best_wild_card_score
    #     best_hand_score = best_wild_card_score
    # else:
    #     card_list1, best_hand_score = best_13card_hand(card_list2)
    #     best_wild_card = "none"
    best_wild_card, best_card_list1, best_hand_score = best13_with_wild(card_list2)
    card_list_string = best_wild_card + ", "
    score3 = best_hand_score[0]
    score2 = best_hand_score[1]
    score1 = best_hand_score[2]
    score4 = best_hand_score[3]
    card_list1_to_string = ",".join(best_card_list1)
    card_list_string += card_list1_to_string + ","
    card_list_string += str(score3[0]) + ", " + str(score3[1]) + ", "
    card_list_string += str(score2[0]) + ", " + str(score2[1]) + ", "
    card_list_string += str(score1[0]) + ", " + str(score1[1]) + ", "
    card_list_string += str(score4) + "\n"
    print card_list_string

    #print card_list_string
####    for i in range (2,-1,-1):
####         #print "i, j, score_array[i][best_hand]", i, j, score_array[i][best_hand]
####         card_list_string += str(best_hand_score[i]) + ", "
##    card_list_string += str(best_hand_score) + "\n"
##    #print card_list_string
    with open("card_list2.csv","a") as f:
        f.write(card_list_string)
    f.close()

end_time = time.time()
lapse_time = end_time - start_time
print "finished", lapse_time, lapse_time/NUMBER_OF_HANDS
