import Tkinter
from deck import *

# Code to add widgets will go here...

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


def onClick(event):
    w.click = event.x, event.y
    # print w.click

def onMotion(event):
    x, y = w.click
    dx = event.x - x
    dy = event.y - y
    w.move('current', dx, dy)
    w.click = event.x, event.y
    print w.click

def onRelease(event):
    mx = event.x // 90 * 90 + 5
    my = event.y // 90 * 90
    my = 160
    print mx, my
    # mx, my - tells image where to snap into place
    rectangle_x = w.coords("current")[0]
    rectangle_y = w.coords("current")[1]
    delta_x = mx - rectangle_x + 5
    delta_y = my - rectangle_y - 11
    #print "rectangle coordinates", rectangle_x, rectangle_y, "delta", delta_x, delta_y
    #print "where to snap in place", mx, my, "mouse coordinates", event.x, event.y
    #print "how much to move x,y", event.x - mx, event.y - my
    w.move("current", delta_x, delta_y)

def show_next_hand(*args):
    pass

def show_best_hand(*args):
    pass

def show_player_score(*args):
    pass

# PROGRAM BEGINS
# PARAMETERS

NUMBER_OF_CARDS = 13
BATCH = True
INTERACTIVE = True
first_time_deck = True
first_time_images = True
image_dir = "Cards_gif/"

root = Tkinter.Tk()
# frame = Frame(root)
# bottomframe = Frame(root)
card_list_string = "w,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,  h3,  p3,   h2, p2,   h1, p1,   total\n"
# print card_list_string
with open("card_list2.csv", "w") as f:
    f.write(card_list_string)

# load a sample card to get the size
photo1 = PhotoImage(file=image_dir+"C2.gif")

#f = Tkinter.Frame(root, bg="gray", height=300, width = 1388)
w = Tkinter.Canvas(root, bg="pink", height=300, width = 1388)
card_list = ["SA", "HA", "DA", "CA", "S2", "DT", "H5", "S7", "HQ", "D6", "H8", "HJ", "C8"]
CARD_GAP = 90
Y_OFFSET = 90 + 60
X_OFFSET = 180
x = X_OFFSET + 8
tag_number = 1
for card in card_list:
    w.create_rectangle((x - 10, Y_OFFSET - 10, x + CARD_GAP - 10, Y_OFFSET + 105), fill="white", tags=tag_number)
    x += CARD_GAP
    tag_number += 1
rectangle_width = 70
rectangle_height = 97

# make canvas width = (NUMBER_OF_CARD + 2) * width of card
width1 = (NUMBER_OF_CARDS + 2) * photo1.width() + 400

# height1 = 2 * photo1.height() + 40
#height1 = 1 * photo1.height() + 40
#canvas1 = Canvas(width=width1, height=height1)
show_next_hand_button = Button(root, text="Show Next Hand", command=show_next_hand)
show_best_hand_button = Button(root, text="Show Best Hand", command=show_best_hand)
show_player_score_button = Button(root, text="Show Player Hand Score",
                                    command=show_player_score)
show_next_hand_button.pack()
show_best_hand_button.pack()
#show_player_score_button.pack()
#frame.pack()

# now load all card images into a dictionary
image_dict = create_images()

# canvas1.bind('<Button-1>', show_next_hand)
# canvas1.bind('<Button-3>', show_best_hand)
# canvas1.bind('<Button-2>', reset_hand)
image_dir = "Cards_gif/"
# create cards and lay on top of the white rectangles
image_dict = create_images()
Y_OFFSET = 10
x = X_OFFSET + 5
for card in card_list:
    print "snap", x, Y_OFFSET, card, image_dict[card]
    #w.create_image(x, Y_OFFSET, image=image_dict[card], anchor=NW, tags=("token", card))
    x += CARD_GAP

w.pack()

w.tag_bind("token", "<Button-1>", onClick)
w.tag_bind("token", "<B1-Motion>", onMotion)
w.tag_bind("token", "<ButtonRelease-1>", onRelease)

root.mainloop()