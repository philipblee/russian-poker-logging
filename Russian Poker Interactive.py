# using Tkinter to display a hand of 13 random card images
# each time you click the canvas

from deck import *
from Tkinter import *
#import random
from random import shuffle

#TODO-pl let user set up his cards to compare with program

def create_images():
    """create all card images as a card_name:image_object dictionary"""
    global image_dict
    global first_time_images
    if first_time_images == True:
        card_list = Deck().deal(1)[0]
        image_dict = {}
        for card in card_list:
            # all images have filenames the match the card_list names + extension .gif
            image_dict[card] = PhotoImage(file=image_dir+card+".gif")
            # print image_dir+card+".gif"  # test
        image_dict["Deck3"] = PhotoImage(file=image_dir+"Deck3"+".gif")
        first_time_images = False
    return image_dict

#PARAMETERS
NUMBER_OF_CARDS = 13
BATCH = True
INTERACTIVE = True
first_time_deck = True
first_time_images = True
image_dir = "Cards_gif/"

if BATCH == True:
    root = Tk()
    card_list_string = "w,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,  h3,  p3,   h2, p2,   h1, p1,   total\n"
    # print card_list_string
    with open("card_list2.csv", "w") as f:
        f.write(card_list_string)
    root.title("Click me!")

def next_hand(event):
    """ Create the card list use Deck().deal(4) and display them"""
    global first
    global a
    if first_time_deck == True:
        a = Deck().deal(4)
        first = False
    logging.info ("\n=========== New Hand ===============\n")
    card_list = a[0]
    print card_list
    # now display the card images at the proper location on the canvas
    x = 10
    y = 10
    canvas1.delete("all")
    card_list3 = sorted(card_list, reverse = True)
    for card in card_list3:  #all cards
        canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
        x += 72

    root.title(card_list)  # test

    start_time = time.time()
    card_list2 = list (card_list[0:NUMBER_OF_CARDS])  #deal NUMBER_OF_CARDS
    card_list3 = list (sorted(card_list2[0:NUMBER_OF_CARDS]))

    card_list2_string = ", ".join(card_list2)
    logging.info(card_list2_string)
    best_wild_card, best_card_list1, best_hand_score = best13_with_wild(card_list2)
    card_list_string = best_wild_card + ", "
    score3, score2, score1, score4 = best_hand_score[0], best_hand_score[1], best_hand_score[2], best_hand_score[3]
    card_list1_to_string = ",".join(best_card_list1)
    card_list_string += card_list1_to_string + ","
    card_list_string += str(score3[0]) + ", " + str(score3[1]) + ", "
    card_list_string += str(score2[0]) + ", " + str(score2[1]) + ", "
    card_list_string += str(score1[0]) + ", " + str(score1[1]) + ", " + str(score4) + "\n"
    print card_list_string
    with open("card_list2.csv","a") as f:
        f.write(card_list_string)

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
    print "finished", start_time, end_time, lapse_time
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

# load a sample card to get the size
photo1 = PhotoImage(file=image_dir+"C2.gif")

# make canvas 14 times the width of a card
width1 = (NUMBER_OF_CARDS + 2) * photo1.width() + 80
#height1 = 12 * photo1.height() + 100
height1 = 2 * photo1.height() + 100

canvas1 = Canvas(width=width1, height=height1)
canvas1.pack()

# now load all card images into a dictionary
image_dict = create_images()
#print image_dict  # test

# best_hand_dict ={"9": "Five of a Kind",
#                  "8": "Straight Flush", "7": "Four of a Kind",
#                  "6": "Full House", "5": "Flush", "4": "Straight",
#                  "3": "Trips", "2": "Two Pairs", "1": "One Pair", "0": "High Card"}
# bind left mouse click on canvas to next_hand display
canvas1.bind('<Button-1>', next_hand)

root.mainloop()
