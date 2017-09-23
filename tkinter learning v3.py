import Tkinter
from deck import *
top = Tkinter.Tk()

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
    # print w.click

def onRelease(event):
    mx = event.x // 90 * 90 + 5
    my = event.y // 90 * 90
    my = 160
    # print mx, my
    # mx, my - tells image where to snap into place
    rectangle_x = w.coords("current")[0]
    rectangle_y = w.coords("current")[1]
    delta_x = mx - rectangle_x + 5
    delta_y = my - rectangle_y - 11
    # print "rectangle coordinates", rectangle_x, rectangle_y, "delta", delta_x, delta_y
    # print "where to snap in place", mx, my, "mouse coordinates", event.x, event.y
    # print "how much to move x,y", event.x - mx, event.y - my
    w.move("current", delta_x, delta_y)

w = Tkinter.Canvas(top, bg="pink", height=300, width = 1388)

card_list = ["SA", "HA", "DA", "CA", "S2", "DT", "H5", "S7", "HQ", "D6", "H8", "HJ", "C8"]
CARD_GAP = 90
Y_OFFSET = 90 + 60
X_OFFSET = 180
x = X_OFFSET + 8
tag_number = 1
NUMBER_OF_CARDS = 13

#create white rectangles
for card in card_list:
    w.create_rectangle((x - 10, Y_OFFSET - 10, x + CARD_GAP - 10, Y_OFFSET + 105), fill="white", tags=tag_number)
    x += CARD_GAP
    tag_number += 1
rectangle_width = 70
rectangle_height = 97
image_dir = "Cards_gif/"

a = Deck().deal(4)
card_list = a[0][0:NUMBER_OF_CARDS]
card_list = sorted(card_list, cmp=suit_rank_sort, reverse=True)
print "show_next_hand", card_list

# create card images and lay on top of white rectangles
image_dict = create_images()
Y_OFFSET = 10
x = X_OFFSET + 5
for card in card_list:
    #print "snap", x, Y_OFFSET, card, image_dict[card]
    w.create_image(x, Y_OFFSET, image=image_dict[card], anchor=NW, tags=("token", card))
    x += CARD_GAP

w.pack()

w.tag_bind("token", "<Button-1>", onClick)
w.tag_bind("token", "<B1-Motion>", onMotion)
w.tag_bind("token", "<ButtonRelease-1>", onRelease)

top.mainloop()