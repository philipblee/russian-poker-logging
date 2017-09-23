# Russian Poker Interactive v6.py - 2 rows, 1 for initial cards that can be re-arranged, 1 for answer
# using Tkinter to display a hand of 13 random card images
# each time you click the canvas
# v7 - adds code for snapping to grid, then I will try to merge code
# v8 - experimental, trying to change the base class of PlayHand from Frame to Canvas
from deck import *
from Tkinter import *
from random import shuffle
card_list = []
#DONE 09-18-2017 TODO-pl let user set up his cards to compare with program
#TODO-pl make cards snap into grid
#DONE 09-19-2017 TODO-pl add space to left of cards
#DONE 09-19-2017 TODO-pl create rectangle objects below cards to help identify where cards are arranged to
#DONE 09-19-2017 TODO-pl fix rank_suit_sort by suit.index[a] * 14+ rank.index{a] in deck
import Tkinter as tk

class SnaptoGrid(Canvas):
    ''' A canvas that bites! ;-)'''

    global card_list

    def __init__(self, master, **kw):
        self.click = None
        Canvas.__init__(self, master, **kw)
        card_list = ["SA", "HA", "DA", "CA", "S2", "DT", "H5", "S7", "HQ", "D6", "H8", "HJ", "C8"]
        # lay out white rectangles first so they are behind all the cards
        rectangle_width = 70
        rectangle_height = 97
        CARD_GAP = 90
        Y_OFFSET = 30
        X_OFFSET = 94
        x = X_OFFSET
        tag_number = 1
        for card in card_list:
            self.create_rectangle((x - 10, Y_OFFSET - 10, x + CARD_GAP - 10, Y_OFFSET -10 + 115), fill="gray", tags=tag_number)
            x += CARD_GAP
            tag_number += 1


        self.create_rectangle(0, 0, rectangle_width, rectangle_height, fill="maroon", tag="R")
        self.create_rectangle(rectangle_width, 0, 2 * rectangle_width, rectangle_height, fill="olive", tag="R")
        self.create_rectangle(2*rectangle_width, 0, 3 * rectangle_width, rectangle_height, fill="purple", tag="R")
        self.create_rectangle(3*rectangle_width, 0, 4 * rectangle_width, rectangle_height, fill="black", tag="R")
        self.create_rectangle(4*rectangle_width, 0, 5*rectangle_width, rectangle_height, fill="green", tag="R")
        self.create_rectangle(5*rectangle_width, 0,  6*rectangle_width, rectangle_height, fill="magenta", tag="R")
        self.create_rectangle(6*rectangle_width, 0, 7 *  rectangle_width, rectangle_height, fill="orange", tag="R")
        self.create_rectangle(7*rectangle_width, 0, 8 *  rectangle_width, rectangle_height, fill="cyan", tag="R")
        self.create_rectangle(8*rectangle_width, 0, 9 *  rectangle_width, rectangle_height, fill="pink", tag="R")
        self.create_rectangle(9*rectangle_width, 0, 10 *  rectangle_width, rectangle_height, fill="blue", tag="R")
        self.create_rectangle(10*rectangle_width, 0, 11 *  rectangle_width, rectangle_height, fill="red", tag="R")
        self.create_rectangle(11*rectangle_width, 0, 12 *  rectangle_width, rectangle_height, fill="yellow", tag="R")
        self.create_rectangle(12*rectangle_width, 0, 13 *  rectangle_width, rectangle_height, fill="hot pink", tag="R")

        # create cards and lay on top of the white rectangles
        x = X_OFFSET
        for card in card_list:
            print "snap", x, Y_OFFSET,card, image_dict[card]
            #self.create_image(x, Y_OFFSET, image=image_dict[card], anchor=NW, tags=("token", card))
            x += CARD_GAP

        self.tag_bind("R", "<Button-1>", self.onClick)
        self.tag_bind("R", "<B1-Motion>", self.onMotion)
        self.tag_bind("R", "<ButtonRelease-1>", self.onRelease)

    def onClick(self, event):
        self.click = event.x, event.y
        #print self.click

    def onMotion(self, event):
        x, y = self.click
        dx = event.x - x
        dy = event.y - y
        self.move('current', dx, dy)
        self.click = event.x, event.y
        print self.click

    def onRelease(self, event):
        mx = event.x//90*90
        my = event.y//90*90
        my = 60 - 20
        print mx, my
        #mx, my - tells image where to snap into place
        rectangle_x = self.coords("current")[0]
        rectangle_y = self.coords("current")[1]
        delta_x = mx - rectangle_x + 5
        delta_y = my - rectangle_y - 11
        print "rectangle coordinates", rectangle_x, rectangle_y, "delta", delta_x, delta_y
        print "where to snap in place", mx, my, "mouse coordinates", event.x, event.y
        print "how much to move x,y", event.x - mx, event.y-my
        self.move("current", delta_x, delta_y)

class PlayHand(Canvas):
    '''Illustrate how to drag items on a Tkinter canvas'''
    global first_PlayHand
    def __init__(self, parent):
        Canvas.__init__(self, parent)

        # create a canvas
        self.canvas = Canvas(width=1000, height=115)
        self.canvas.pack(fill="both", expand=False)

        # this data is used to keep track of item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        CARD_GAP = 90
        Y_OFFSET = 10
        X_OFFSET = 100
        x = X_OFFSET
        tag_number = 1
        # lay out white rectangles first so they are behind all the cards
        for card in card_list:
            self.canvas.create_rectangle((x-10,Y_OFFSET-10, x+CARD_GAP-10,115), fill="white", tags=tag_number)
            x += CARD_GAP
            tag_number += 1

        # blue top and bottom lines for play_area first
        self.canvas.create_line(90, 3, 1260, 3, fill="blue", width=3)
        self.canvas.create_line(90, 115, 1260, 115, fill="blue", width=3)
        # 12 vertical lines for 13 cards - width=3 lines to separate hands
        self.canvas.create_line(90, 0, 90, 115, fill="blue", width=3)
        self.canvas.create_line(180, 0, 180, 115, fill="blue", width=1)
        self.canvas.create_line(270, 0, 270, 115, fill="blue", width=1)
        self.canvas.create_line(360, 0, 360, 115, fill="blue", width=1)
        self.canvas.create_line(450, 0, 450, 115, fill="blue", width=1)
        self.canvas.create_line(540, 0, 540, 115, fill="blue", width=3)
        self.canvas.create_line(630, 0, 630, 115, fill="blue", width=1)
        self.canvas.create_line(720, 0, 720, 115, fill="blue", width=1)
        self.canvas.create_line(810, 0, 810, 115, fill="blue", width=1)
        self.canvas.create_line(900, 0, 900, 115, fill="blue", width=1)
        self.canvas.create_line(990, 0, 990, 115, fill="blue", width=3)
        self.canvas.create_line(1080, 0, 1080, 115, fill="blue", width=1)
        self.canvas.create_line(1170, 0, 1170, 115, fill="blue", width=1)
        self.canvas.create_line(1260, 0, 1260, 115, fill="blue", width=3)

        # create card images from card_list that can be dragged
        x = X_OFFSET
        for card in card_list:
            self.canvas.create_image(x, Y_OFFSET, image=image_dict[card], anchor=NW, tags=("token", card))
            #self._create_token((x, Y_OFFSET), card)
            x += CARD_GAP

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)

    def _create_token(self, coord, card):
        """Create a token of gif image"""
        x,y = coord
        self.canvas.create_image(x,y, image=image_dict[card], anchor=NW, tags=("token",card))
        # print "on create image", x, y, card

    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        mx = event.x//90*90
        my = event.y//90*90
        my = 100
        # print mx, my
        # mx, my - tells image where to snap into place
        print self.coords("item")
        # rectangle_x = self.coords("current")[0]
        # rectangle_y = self.coords("current")[1]
        # delta_x = rectangle_x - mx
        # delta_y = rectangle_y - my


    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        #print event.x, event.y
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

def show_player_score(event, *args):
    for card in card_list:
        # find out where each card is located
        # score hand3, hand2, hand1
        # total score
        pass

def reset_hand(event):
    PlayHand(root).pack()

def create_images():
    """create all card images as a card_name:image_object dictionary"""
    global image_dict
    global first_time_images
    first_time_images= True
    if first_time_images == True:
        card_list = Deck().deal(1)[0]
        image_dict = {}
        for card in card_list:
            # all images have filenames the match the card_list names + extension .gif
            image_dict[card] = PhotoImage(file=image_dir+card+".gif")
            # print "create_images", card, image_dir + card+ ".gif"
        image_dict["Deck3"] = PhotoImage(file=image_dir+"Deck3"+".gif")
        first_time_images = False
    return image_dict

def show_next_hand(*args):
    """ Create the card list use Deck().deal(4) and display them"""
    global card_list
    a = Deck().deal(4)
    logging.info ("\n=========== New Hand ===============\n")
    card_list = a[0][0:NUMBER_OF_CARDS]
    card_list = sorted(card_list, cmp=suit_rank_sort, reverse=True)
    print "show_next_hand",card_list
    x = 10
    y = 10 + 30
    CARD_GAP = 90
    x_place = 954 + 330
    x = x_place
    PlayHand(root).pack()
    root.title("New Hand")
    # clear out last hand
    canvas1.delete("all")
    total_score_label = Label(text="total score = 0" + 18 * " ", fg="blue", bg="white")
    total_score_label.place(x=x, y=y)
    hand3_score_label = Label(text="hand3 = 0" + 25 * " ", fg="blue", bg="white")
    hand3_score_label.place(x=x, y=y + 75)
    hand2_score_label = Label(text="hand2 = 0" + 25 * " ", fg="blue", bg="white")
    hand2_score_label.place(x=x, y=y + 50)
    hand1_score_label = Label(text="hand1 = 0" + 25 * " ", fg="blue", bg="white")
    hand1_score_label.place(x=x, y=y + 25)

def show_best_hand(*args):
    """ Given card_list, find the best hand and show scoring"""
    global card_list
    global message_left_click_label
    message_left_click_label = Label(text="")
    if card_list == []:
        message_left_click_label = Label(text="Start new hand by left-clicking mouse")
        message_left_click_label.pack()
        return
    message_left_click_label.pack_forget()

    #TODO-pl calculate score of played hand -TBD

    card_list2 = list(card_list[0:NUMBER_OF_CARDS] ) # deal NUMBER_OF_CARDS
    card_list3 = list(card_list2)
    card_list2_string = ", ".join(card_list2)
    logging.info(card_list2_string)

    # calling best13_with_wild to return best_wild_card
    best_wild_card, best_card_list1, best_hand_score = best13_with_wild(card_list2)
    card_list_string = best_wild_card + ", "

    # start_time = time.time()
    score3, score2, score1, score4 = best_hand_score[0], best_hand_score[1], best_hand_score[2], best_hand_score[3]
    # end_time = time.time()
    # lapse_time = end_time - start_time
    # print "finished", start_time, end_time, lapse_time

    # creating string to write to "card_list2.csv"
    card_list1_to_string = ",".join(best_card_list1)
    card_list_string += card_list1_to_string + "," + str(score3[0]) + ", " + str(score3[1]) + ", "
    card_list_string += str(score2[0]) + ", " + str(score2[1]) + ", "
    card_list_string += str(score1[0]) + ", " + str(score1[1]) + ", " + str(score4) + "\n"
    with open("card_list2.csv", "a") as f:
        f.write(card_list_string)

    # placing objects on canvas1, which will show when
    x = 10
    y = 10 + 90
    CARD_GAP = 90
    x_place = 954
    canvas1.delete("all")
    root.title("Solved")
    #card_list3 = list(card_list)

    # for card in card_list3:
    #     canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
    #     x += CARD_GAP
    # canvas1.create_line(0,115,1400,115,fill="blue", width = 3)
    #card_list2 = list(card_list)
    j = 0

    for i in range(1):
        x = 10 + 90
        y = 10 * (j + 1)
        j += 1
        for card in best_card_list1[0:5]:  # hand3
            canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
            x += CARD_GAP

        for card in best_card_list1[5:10]:  # hand2
            canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
            x += CARD_GAP

        for card in best_card_list1[10:13]:  # hand1
            canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
            x += CARD_GAP
        x += 18

        y = 10 + 30
        total_score_label = Label(text="total score = "+str(score4), fg="blue", bg="white")
        total_score_label.place(x=x,y=y)
        hand3_score_label = Label(text="hand3 = " + str(score3), fg="blue", bg="white")
        hand3_score_label.place(x=x, y=y+75)
        hand2_score_label = Label(text="hand2 = " + str(score2), fg="blue", bg="white")
        hand2_score_label.place(x=x, y=y+50)
        hand1_score_label = Label(text="hand1 = " + str(score1), fg="blue", bg="white")
        hand1_score_label.place(x=x, y=y+25)

# PROGRAM BEGINS
# PARAMETERS
NUMBER_OF_CARDS = 13
BATCH = True
INTERACTIVE = True
first_time_deck = True
first_time_images = True
image_dir = "Cards_gif/"

root = Tk()
# frame = Frame(root)
# bottomframe = Frame(root)
card_list_string = "w,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,  h3,  p3,   h2, p2,   h1, p1,   total\n"
# print card_list_string
with open("card_list2.csv", "w") as f:
    f.write(card_list_string)

# load a sample card to get the size
photo1 = PhotoImage(file=image_dir+"C2.gif")

# make canvas width = (NUMBER_OF_CARD + 2) * width of card
width1 = (NUMBER_OF_CARDS + 2) * photo1.width() + 400

# height1 = 2 * photo1.height() + 40
height1 = 1 * photo1.height() + 40
canvas1 = Canvas(width=width1, height=height1)
show_next_hand_button = Button(root, text="Show Next Hand", command=show_next_hand)
show_best_hand_button = Button(root, text="Show Best Hand", command=show_best_hand)
show_player_score_button = Button(root, text="Show Player Hand Score",
                                    command=show_player_score)
show_next_hand_button.pack()
show_best_hand_button.pack()
#show_player_score_button.pack()
#frame.pack()
canvas1.pack()

# now load all card images into a dictionary
image_dict = create_images()

canvas1.bind('<Button-1>', show_next_hand)
canvas1.bind('<Button-3>', show_best_hand)
canvas1.bind('<Button-2>', reset_hand)

#snapit = SnaptoGrid(root, width=1500, height=170, bg="white")
#snapit.pack()

root.mainloop()