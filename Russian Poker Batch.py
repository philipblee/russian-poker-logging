# using Tkinter to display a hand of 13 random card images
# each time you click the canvas
# (images are in GIF format for Tkinter to display properly)
import datetime
from deck import *
from Tkinter import *
from random import *

start_time = time.time()
f = open ('card_list2.csv', 'w')
card_list_string = "w,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,  h3,  p3,   h2, p2,   h1, p1,   total\n"
#print card_list_string
with open("card_list2.csv", "w") as f:
    f.write(card_list_string)

#PARAMETERS
NUMBER_OF_HANDS = 100
NUMBER_OF_CARDS = 13

for k in range (NUMBER_OF_HANDS):
    if k%10 == 0:
        print k
    a = Deck().deal_n_cards(NUMBER_OF_CARDS)
    card_list = a[0]
    logging.debug((card_list))
    card_list2 = list (card_list[0:13])  #deal number_of_cards
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
    #print card_list_string

    with open("card_list2.csv","a") as f:
        f.write(card_list_string)
end_time = time.time()
lapse_time = end_time - start_time
print "finished", lapse_time, lapse_time/NUMBER_OF_HANDS
