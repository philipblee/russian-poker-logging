# Russian Poker Interactive v3.py - Takes 4 rows, 2 for hand and answer, 1 for cards, 1 for arranging hand
# using Tkinter to display a hand of 13 random card images
# each time you click the canvas

from deck import *
from Tkinter import *
from random import shuffle
card_list = []
#TODO-pl let user set up his cards to compare with program - started 09-18-2017

class Play_Area(Frame):
    '''Illustrate how to drag items on a Tkinter canvas'''
    global card_list

    def __init__(self, parent):
        Frame.__init__(self, parent)

        # create a canvas
        self.canvas = Canvas(width=1000, height=230)
        self.canvas.pack(fill="both", expand=False)
        # top line and bottom line for play_area
        self.canvas.create_line(0, 3, 1170, 3, fill="blue", width=3)
        self.canvas.create_line(0, 115, 1170, 115, fill="blue", width=3)
        # 12 vertical lines for 13 cards
        self.canvas.create_line(3, 0, 3, 230, fill="blue", width=3)
        self.canvas.create_line(90, 0, 90, 230, fill="blue", width=1)
        self.canvas.create_line(180, 0, 180, 230, fill="blue", width=1)
        self.canvas.create_line(270, 0, 270, 230, fill="blue", width=1)
        self.canvas.create_line(360, 0, 360, 230, fill="blue", width=1)
        self.canvas.create_line(450, 0, 450, 230, fill="blue", width=3)
        self.canvas.create_line(540, 0, 540, 230, fill="blue", width=1)
        self.canvas.create_line(630, 0, 630, 230, fill="blue", width=1)
        self.canvas.create_line(720, 0, 720, 230, fill="blue", width=1)
        self.canvas.create_line(810, 0, 810, 230, fill="blue", width=1)
        self.canvas.create_line(900, 0, 900, 230, fill="blue", width=3)
        self.canvas.create_line(990, 0, 990, 230, fill="blue", width=1)
        self.canvas.create_line(1080, 0, 1080, 230, fill="blue", width=1)
        self.canvas.create_line(1170, 0, 1170, 230, fill="blue", width=3)
        self.canvas.delete("All")
        # this data is used to keep track of item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create card images from card_list that can be moved around
        x = 10
        CARD_GAP = 90
        for card in card_list:
            self._create_image_token((x, 130), card)
            x += CARD_GAP

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)

    def _create_image_token(self, coord, card):
        """Create a token of gif image"""
        x,y = coord
        self.canvas.create_image(x,y, image=image_dict[card], anchor=NW, tags="token")

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

def reset_hand(event):
    Play_Area(root).pack_forget()

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
        image_dict["Deck3"] = PhotoImage(file=image_dir+"Deck3"+".gif")
        first_time_images = False
    return image_dict

def show_next_hand(event):
    """ Create the card list use Deck().deal(4) and display them"""
    global card_list
    a = Deck().deal(4)
    logging.info ("\n=========== New Hand ===============\n")
    card_list = a[0][0:NUMBER_OF_CARDS]
    card_list = sorted(card_list, reverse=True)
    # for widget in root.winfo_children()
    #     widget.destroy()
    Play_Area(root).pack()
    root.title("New Hand")

    # now clear and display card images on canvas1
    x = 10
    y = 10
    CARD_GAP = 90
    canvas1.delete("all")

    card_list3 = sorted(card_list, reverse = True)
    for card in card_list3:  #all cards
        canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
        x += CARD_GAP


    

def show_best_hand(event):
    """ Given card_list, find the best hand and show scoring"""
    global card_list
    global message_left_click_label
    message_left_click_label = Label(text="")
    if card_list == []:
        message_left_click_label = Label(text="Start new hand by left-clicking mouse")
        message_left_click_label.pack()
        return
    message_left_click_label.pack_forget()
    card_list2 = list(card_list[0:NUMBER_OF_CARDS])  # deal NUMBER_OF_CARDS
    card_list3 = sorted((card_list2), reverse=True)
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
    y = 10
    CARD_GAP = 90
    x_place = 954
    canvas1.delete("all")
    root.title("Solved")
    card_list3 = sorted(card_list, reverse=True)

    for card in card_list3:
        canvas1.create_image(x, y, image=image_dict[card], anchor=NW)
        x += CARD_GAP
    canvas1.create_line(0,230,1400,230,fill="blue", width = 3)

    #card_list2 = list(card_list)
    j = 0

    for i in range(1):
        x = 10
        y = 120 * (j + 1)
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

        total_score_label = Label(text="total score = "+str(score4), fg="blue", bg="white")
        total_score_label.place(x=x,y=y)
        hand3_score_label = Label(text="hand3 = " + str(score3), fg="blue", bg="white")
        hand3_score_label.place(x=x, y=y+75)
        hand2_score_label = Label(text="hand2 = " + str(score2), fg="blue", bg="white")
        hand2_score_label.place(x=x, y=y+50)
        hand1_score_label = Label(text="hand1 = " + str(score1), fg="blue", bg="white")
        hand1_score_label.place(x=x, y=y+25)

#PARAMETERS
NUMBER_OF_CARDS = 13
BATCH = True
INTERACTIVE = True
first_time_deck = True
first_time_images = True
image_dir = "Cards_gif/"

root = Tk()
card_list_string = "w,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,  h3,  p3,   h2, p2,   h1, p1,   total\n"
# print card_list_string
with open("card_list2.csv", "w") as f:
    f.write(card_list_string)

# load a sample card to get the size
photo1 = PhotoImage(file=image_dir+"C2.gif")

# make canvas width = (NUMBER_OF_CARD + 2) * width of card
width1 = (NUMBER_OF_CARDS + 2) * photo1.width() + 400

#height1 = 2 * photo1.height() + 40
height1 = 2 * photo1.height() + 40

canvas1 = Canvas(width=width1, height=height1)
canvas1.pack()

# now load all card images into a dictionary
image_dict = create_images()

canvas1.bind('<Button-1>', show_next_hand)
canvas1.bind('<Button-3>', show_best_hand)
canvas1.bind('<Button-2>', reset_hand)
root.mainloop()