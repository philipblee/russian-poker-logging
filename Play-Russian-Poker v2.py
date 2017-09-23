#DONE 09-18-2017 TODO-pl let user set up his cards to compare with program
#DONE 09-22-2017 TODO-pl make cards snap into grid
#DONE 09-19-2017 TODO-pl add space to left of cards
#DONE 09-19-2017 TODO-pl create rectangle objects below cards to help identify where cards are arranged to
#DONE 09-19-2017 TODO-pl fix rank_suit_sort by suit.index[a] * 14+ rank.index{a] in deck
#TODO-pl figure out player's hand and score player's hand

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

def onMotion(event):
    x, y = w.click
    dx = event.x - x
    dy = event.y - y
    w.move('current', dx, dy)
    w.click = event.x, event.y

def onRelease(event):
    mx = event.x // 90 * 90 + 5
    my = event.y // 140 * 140 + 20
    if my > 160:
         my = 160
    # mx, my - tells image where to snap into place
    rectangle_x, rectangle_y = w.coords("current")[0], w.coords("current")[1]
    delta_x = mx - rectangle_x + 5
    delta_y = my - rectangle_y - 11
    # print "rectangle coordinates", rectangle_x, rectangle_y, "delta", delta_x, delta_y
    # print "where to snap in place", mx, my, "mouse coordinates", event.x, event.y
    # print "how much to move x,y", event.x - mx, event.y - my
    w.move("current", delta_x, delta_y)

def show_next_hand(*args):
    """ Create the card list use Deck().deal(4) and display them"""
    global card_list
    NUMBER_OF_CARDS = 13
    a = Deck().deal(4)
    logging.info ("\n=========== New Hand ===============\n")
    card_list = a[0][0:NUMBER_OF_CARDS]
    card_list = sorted(card_list, cmp=suit_rank_sort, reverse=True)

    # PlayHand(root).pack()
    top.title("New Hand")
    # clear out last hand
    w.delete("all")

    # create white rectangles
    CARD_GAP = 90  # distance between cards and rectangles
    Y_OFFSET = 90 + 60  # add 60 to account for buttons on top
    X_OFFSET = 178
    x = X_OFFSET
    tag_number = 1
    for card in card_list:
        # print x-10, Y_OFFSET -10, x + CARD_GAP -10, Y_OFFSET + 105
        w.create_rectangle((x, Y_OFFSET - 10, x + CARD_GAP, Y_OFFSET + 105), fill="white", tags=tag_number)
        x += CARD_GAP
        tag_number += 1

    Y_OFFSET = 10
    y = 10 + 30 + 20
    CARD_GAP = 90
    x_place = 210
    x = x_place - 20
    x = X_OFFSET + 5
    for card in card_list:
        # print "snap", x, Y_OFFSET, card, image_dict[card]
        w.create_image(x, Y_OFFSET, image=image_dict[card], anchor=NW, tags=("token", card))
        x += CARD_GAP
    total_score_label = Label(text="total score = 0" + 28 * " ", fg="blue", bg="white")
    total_score_label.place(x=x, y=y)
    hand3_score_label = Label(text="hand3 = 0" + 35 * " ", fg="blue", bg="white")
    hand3_score_label.place(x=x, y=y + 75)
    hand2_score_label = Label(text="hand2 = 0" + 35 * " ", fg="blue", bg="white")
    hand2_score_label.place(x=x, y=y + 50)
    hand1_score_label = Label(text="hand1 = 0" + 35 * " ", fg="blue", bg="white")
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
    x = 10 + 70
    y = 10 + 90
    CARD_GAP = 90
    x_place = 954 + 70
    #top.delete("all")
    top.title("Solved")

    j = 0
    for i in range(1):
        x = 10 + 90 + 70 + 15
        y = 10 * (j + 1)
        j += 1
        for card in best_card_list1[0:5]:  # hand3
            w.create_image(x, y, image=image_dict[card], anchor=NW)
            x += CARD_GAP

        for card in best_card_list1[5:10]:  # hand2
            w.create_image(x, y, image=image_dict[card], anchor=NW)
            x += CARD_GAP

        for card in best_card_list1[10:13]:  # hand1
            w.create_image(x, y, image=image_dict[card], anchor=NW)
            x += CARD_GAP
        x += 18 - 18

        y = 10 + 30 + 20
        total_score_label = Label(text="total score = "+str(score4), fg="blue", bg="white")
        total_score_label.place(x=x,y=y)
        hand3_score_label = Label(text="hand3 = " + str(score3), fg="blue", bg="white")
        hand3_score_label.place(x=x, y=y+75)
        hand2_score_label = Label(text="hand2 = " + str(score2), fg="blue", bg="white")
        hand2_score_label.place(x=x, y=y+50)
        hand1_score_label = Label(text="hand1 = " + str(score1), fg="blue", bg="white")
        hand1_score_label.place(x=x, y=y+25)

def show_player_score(*args):
    pass

w = Tkinter.Canvas(top, bg="pink", height=300, width = 1528)

NUMBER_OF_CARDS = 13
image_dir = "Cards_gif/"
image_dict = create_images()
show_next_hand()

show_next_hand_button = Button(top, text="Show Next Hand", command=show_next_hand)
show_best_hand_button = Button(top, text="Show Best Hand", command=show_best_hand)
show_player_score_button = Button(top, text="Show Player Hand Score",
                                    command=show_player_score)
show_next_hand_button.pack()
show_best_hand_button.pack()
show_player_score_button.pack(side=RIGHT)
w.pack()

w.tag_bind("token", "<Button-1>", onClick)
w.tag_bind("token", "<B1-Motion>", onMotion)
w.tag_bind("token", "<ButtonRelease-1>", onRelease)

top.mainloop()