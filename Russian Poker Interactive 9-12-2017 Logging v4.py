# using Tkinter to display a hand of 13 random card images
# each time you click the canvas

from deck_wild_logging_v4 import *
from Tkinter import *
import random
from random import shuffle
from collections import Counter 

#import logging
#logging.basicConfig(format='%(levelname)s:%(lineno)d:%(message)s', level=logging.INFO)

root = Tk()
f = open ('card_list2.csv', 'w')

root.title("Click me!")
def create_images():
    """create all card images as a card_name:image_object dictionary"""
    a = Deck().deal(1)[0]
    card_list = a
    image_dict = {}
    for card in card_list:
        # all images have filenames the match the card_list names + extension .gif
        image_dict[card] = PhotoImage(file=image_dir+card+".gif")
        #print image_dir+card+".gif"  # test
    image_dict["Deck3"] = PhotoImage(file=image_dir+"Deck3"+".gif")
    return image_dict

def next_hand(event):
    """ Create the card list use Deck().deal(4) and display them"""
    a = Deck().deal(4)
    for i in range (0,1):
        logging.info ("\n\n=========== New Hand ===============\n")
    card_list = a[0]
    root.title(card_list)  # test

    ###########################################################
    ################### program begins  #######################
    ###########################################################
    start_time = time.time()
    card_list2 = list (card_list[0:number_of_cards])  #deal number_of_cards
    card_list3 = list (sorted(card_list2[0:number_of_cards]))
    card_list2_string = ""
    for i in card_list2:
        card_list2_string = card_list2_string + i+ ","
    logging.info(card_list2_string)

    wild_card_present = False
    wild_card = "N/A"

    for cardx in card_list2:
        if cardx == "WX":
            wild_card_present = True
            card_list2.remove("WX")
            
    if wild_card_present == True:
        pass
        #print "wild card", wild_card_index
        #loop through all 52 cards
        wild_list = [s+r for s in "SHDC" for r in "23456789TJQKA"]
        best_wild_hand_score = 0
        best_wild_card_score = [0,0,0,0,0]
        best_wild_card = ""
        for wild_card in wild_list:
            card_list2.append(wild_card)
            #print "After wild", card_list2
            card_list1, best_hand_score = best_13card_hand(card_list2)
            print wild_card, best_hand_score[0], best_hand_score[1], best_hand_score[2], best_hand_score[3]
            if best_hand_score[3] > best_wild_hand_score:
                 best_wild_card_score = best_hand_score[0:4]
                 best_wild_hand_score = best_hand_score[3]
                 best_card_list1 = card_list1
                 best_wild_card = wild_card
                 #print best_wild_card, best_wild_hand_score
            #print "After best_13card", card_list1      
            #print wild_card, best_hand_score
            card_list2.remove(wild_card)
        #print "best_wild_card", best_wild_card, best_wild_card_score
        best_hand_score = best_wild_card_score
        i = 0
        #print best_card_list1, best_wild_card
        for card in best_card_list1:
              #print i, card, best_wild_card
              if card == best_wild_card:
                   best_card_list1[i] = "WX"
                   break
              i += 1
        #print i
    else:
        best_card_list1, best_hand_score = best_13card_hand(card_list2)
        best_wild_card = "none"
    
    card_list_string = best_wild_card + ", "
    score3 = best_hand_score[0]
    score2 = best_hand_score[1]
    score1 = best_hand_score[2]
    score4 = best_hand_score[3]
    card_list_string += str(score3[0]) + ", " + str(score3[1]) + ", "
    card_list_string += str(score2[0]) + ", " + str(score2[1]) + ", "
    card_list_string += str(score1[0]) + ", " + str(score1[1]) + ", "
    card_list_string += str(score4) + "\n"
    #print card_list_string
####    for i in range (2,-1,-1):
####         #print "i, j, score_array[i][best_hand]", i, j, score_array[i][best_hand]
####         card_list_string += str(best_hand_score[i]) + ", "
##    card_list_string += str(best_hand_score) + "\n"
##    #print card_list_string
    with open("card_list2.csv","a") as f:
        f.write(card_list_string)
    f.close()
    

                                  
# now display the card images at the proper location on the canvas
    x = 10
    y = 10
    canvas1.delete("all")
    card_list3 = sorted(card_list3, reverse = True)
    for card in card_list3:  #all cards
        canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
        x += 72
        
    card_list2 = list(card_list)
    j = 0
    end_time = time.time()
    lapse_time = end_time - start_time
    print "finished", lapse_time
    for i in range(1):
        #if invalid_hand[i] == False:  # and i == best_hand:
            x = 10
            y = 120 * (j+1)
            j += 1
            #y = 120
            for card in best_card_list1[0:5]:   #hand3
                canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
                x += 72            
            x += 36
            
            for card in best_card_list1[5:10]:   #hand2
                canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
                x += 72            
            x += 36
            
            for card in best_card_list1[10:13]:    #remaining
                canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
                x += 72
            x += 36


##            if i == best_hand:
##                canvas1.create_image(x, y, image=image_dict["Deck3"], anchor=NW)
                
            #card_list2 = list(card_list)
     
image_dir = "Cards_gif/"
 
# load a sample card to get the size
photo1 = PhotoImage(file=image_dir+"C2.gif")

number_of_cards = 13

# make canvas 14 times the width of a card
width1 = (number_of_cards + 2) * photo1.width() + 80
#height1 = 12 * photo1.height() + 100
height1 = 2 * photo1.height() + 100

canvas1 = Canvas(width=width1, height=height1)
canvas1.pack()
 
# now load all card images into a dictionary
image_dict = create_images()
#print image_dict  # test

best_hand_dict ={
        "8": "Straight Flush", "7": "Four of a Kind",
        "6": "Full House", "5": "Flush", "4": "Straight",
        "3": "Trips", "2": "Two Pairs", "1": "One Pair", "0": "High Card"}
# bind left mouse click on canvas to next_hand display
canvas1.bind('<Button-1>', next_hand)
 
root.mainloop()
