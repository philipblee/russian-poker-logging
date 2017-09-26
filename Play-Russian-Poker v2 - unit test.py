#DONE 09-18-2017 TODO-pl let user set up his cards to compare with program
#DONE 09-22-2017 TODO-pl make cards snap into grid
#DONE 09-19-2017 TODO-pl add space to left of cards
#DONE 09-19-2017 TODO-pl create rectangle objects below cards to help identify where cards are arranged to
#DONE 09-19-2017 TODO-pl fix rank_suit_sort by suit.index[a] * 14+ rank.index{a] in deck
#DONE 09-23-2017 TODO-pl figure out player's hand and score player's hand
#TODO-pl show deck of cards, then allows player to pick hand to play
# split out determine_best_hand from show_best_hand

import Tkinter
from deck import *
top = Tkinter.Tk()

def create_images():
    """create all card images as a card_name:image_object dictionary"""
    #global image_dict
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
    X_GAP = 90
    Y_GAP = 140
    mx = event.x // X_GAP * X_GAP + 5
    my = event.y // Y_GAP * Y_GAP + 20
    # if my > 160:
    #     my = 160
    # mx, my - tells image where to snap into place 90 is X_GAP, 140 is Y_GAP
    rectangle_x, rectangle_y = w.coords("current")[0], w.coords("current")[1]
    delta_x = mx - rectangle_x + 5
    delta_y = my - rectangle_y - 11
    w.move("current", delta_x, delta_y)

def set_up_hand(*args):
    """ This function reads what is on the canvas and let's ? know"""
    # evaluate what is on white rectangles
    # set_up_card_list = determine_player_cards()
    w.delete("token")
    show_deck_of_cards()
    return

def play_setup_hand(*args):
    card_list = determine_setup_hand()
    w.delete("token")
    show_next_hand(card_list)

def determine_setup_hand(*args):
    full_deck = sorted(Deck().deal(1)[0], cmp=suit_rank_sort, reverse=True)
    print full_deck
    card_listx = []
    for card in full_deck:
        card_x, card_y = w.coords(card)
        print "in determine_setup_hand", card, card_x, card_y
        if card_y <= 200:
             card_listx.append(card)
    print card_listx
    return (card_listx)

def show_deck_of_cards(*args):
    """show deck of cards that can be moved to playing area"""
    card_list = list(Deck().deal(1))[0]
    card_list = sorted(card_list, cmp=suit_rank_sort)
    X_OFFSET = 190
    Y_OFFSET = 300 - 11
    CARD_GAP = 90
    y = 10 + 30 + 20
    x = X_OFFSET
    number =1
    for card in card_list:
        print card, x, Y_OFFSET, image_dict[card]
        w.create_image(x, Y_OFFSET, image=image_dict[card], anchor=NW, tags=("token", card, number))
        x += CARD_GAP
        number += 1
        if x > 1320:
             x = 190
             Y_OFFSET += 110

def show_next_hand(card_list, *args):
    """ Create the card list use Deck().deal(4) and display them"""
    NUMBER_OF_CARDS = 13
    logging.info ("\n=========== New Hand ===============\n")
    if card_list == []:
        a = Deck().deal(4)
        card_list = a[0][0:NUMBER_OF_CARDS]
        card_list = sorted(card_list, cmp=rank_sort, reverse=True)
    # PlayHand(root).pack()
    top.title("Choose the hand that Peter Yee would play")
    # clear out last hand
    # w.delete("all")

    # create white rectangles
    X_GAP = 90  # distance between cards and rectangles
    Y_OFFSET = 90 + 60  # add 60 to account for buttons on top
    X_OFFSET = 180  # where cards and rectangles begin
    x = X_OFFSET
    tag_number = 1
    for i in range(13):
        # print x-10, Y_OFFSET -10, x + CARD_GAP -10, Y_OFFSET + 105
        w.create_rectangle((x, Y_OFFSET - 10, x + X_GAP, Y_OFFSET + 105), fill="white", tags=tag_number)
        x += X_GAP
        tag_number += 1

    # blue top and bottom lines for play_area first X_OFFSET
    w.create_line(X_OFFSET, 138, X_OFFSET + 1170, 138, fill="blue", width=3)
    w.create_line(X_OFFSET, 257, X_OFFSET + X_OFFSET + 11 * X_GAP, 257, fill="blue", width=3)

    # 12 vertical lines for 13 cards - width=3 lines to separate hands
    #TODO-pl use X_OFFSET, X_GAP and Y_GAP
    w.create_line(X_OFFSET, 138, X_OFFSET, 258, fill="blue", width=3)
    w.create_line(X_OFFSET + X_GAP, 138, X_OFFSET + X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 2 * X_GAP, 138, X_OFFSET + 2 * X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 3 * X_GAP, 138, X_OFFSET + 3 * X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 4 * X_GAP, 138, X_OFFSET + 4 * X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 5 * X_GAP, 138, X_OFFSET + 5 * X_GAP, 258, fill="blue", width=3)
    w.create_line(X_OFFSET + 6 * X_GAP, 138, X_OFFSET + 6 * X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 7 * X_GAP, 138, X_OFFSET + 7 * X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 8 * X_GAP, 138, 900, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 9 * X_GAP, 138, X_OFFSET + 9 * X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 10 * X_GAP, 138, X_OFFSET + 10 * X_GAP, 258, fill="blue", width=3)
    w.create_line(X_OFFSET + 11 * X_GAP, 138, X_OFFSET + 11 * X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 12* X_GAP, 138, X_OFFSET + 12* X_GAP, 258, fill="blue", width=1)
    w.create_line(X_OFFSET + 13* X_GAP, 138, X_OFFSET + 13* X_GAP, 258, fill="blue", width=3)

    Y_OFFSET = 10
    y = 10 + 30 + 20
    x = X_OFFSET + 5   # adds 5 to move card to center of white rectangle
    for card in card_list:
        w.create_image(x, Y_OFFSET, image=image_dict[card], anchor=NW, tags=("token", card))
        x += X_GAP

    total_score_label = Label(text="total score = 0" + 28 * " ", fg="blue", bg="white")
    total_score_label.place(x=x, y=y)
    hand3_score_label = Label(text="hand3 = 0" + 35 * " ", fg="blue", bg="white")
    hand3_score_label.place(x=x, y=y + 25)
    hand2_score_label = Label(text="hand2 = 0" + 35 * " ", fg="blue", bg="white")
    hand2_score_label.place(x=x, y=y + 50)
    hand1_score_label = Label(text="hand1 = 0" + 35 * " ", fg="blue", bg="white")
    hand1_score_label.place(x=x, y=y + 75)

def find_best_hand(*args):
    """ Given card_list, find the best hand and show scoring"""
    global card_list
    global message_left_click_label
    message_left_click_label = Label(text="")
    if card_list == []:
        message_left_click_label = Label(text="Start new hand by left-clicking mouse")
        message_left_click_label.pack()
        return
    message_left_click_label.pack_forget()

    # TODO-pl calculate score of played hand -TBD

    card_list2 = list(card_list[0:NUMBER_OF_CARDS])  # deal NUMBER_OF_CARDS
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
    return (best_wild_card, best_card_list1, best_hand_score)

def show_best_hand(*args):
    """ Given card_list, find the best hand and show scoring"""
    global image_dict
    global message_left_click_label

    wild_card, best_card_list1, best_hand_score = find_best_hand(card_list)
    score3, score2, score1, score4 = best_hand_score[0], best_hand_score[1], best_hand_score[2], best_hand_score[3]
    print "best_card_list1", best_card_list1
    # placing card images on canvas
    top.title("Best Hand Below and Best Scores on Right")
    CARD_GAP = 90
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
        hand3_score_label.place(x=x, y=y+25)
        hand2_score_label = Label(text="hand2 = " + str(score2), fg="blue", bg="white")
        hand2_score_label.place(x=x, y=y+50)
        hand1_score_label = Label(text="hand1 = " + str(score1), fg="blue", bg="white")
        hand1_score_label.place(x=x, y=y+75)
        player_total_score = round(show_player_score(),2)
        score4 = round(score4,2)
        global wins
        global ties
        global losses
        if player_total_score > score4:
             wins += 1
        elif score4 > player_total_score:
             losses +=1
        elif score4 == player_total_score:
             ties +=1
        print "wins", wins, "losses", losses, "ties", ties

def show_player_score(*args):
    """ shows player"""
    players_13card_hand = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    # make sure every card is used
    for card in card_list:
         # print w.coords(card)
         card_placex = int((w.coords(card)[0]-100)/90) - 1  # determine where card is placed
         card_placey = int((w.coords(card)[1])) # determine if this card is on the player's board
         logging.info((card, w.coords(card)[0], card_placex, card_placey))
         # print((card, w.coords(card)[0], card_placex, card_placey))
         if card_placey >= 100:
              players_13card_hand[card_placex] = str(card)  # players_13card_hand puts cards in order played
    print players_13card_hand
    for card in players_13card_hand:
         if card == 0:
              message = "Player's Hand is incomplete.  Please play all 13 cards"
              valid_hand_label = Label(text="message", fg="blue", bg="white")
              valid_hand_label.place(x=1400, y=130)
              return
    for card in card_list:
         card_placex = int((w.coords(card)[0]-100)/90) - 1 # determine where card is placed
         logging.info((card, w.coords(card)[0], card_placex))
         players_13card_hand [card_placex] = str(card)  # players_13card_hand puts cards in order played
         which_hand = 0
         if card == "wild":   # if there is a wild_card, need to determine which hand wild_card is in
              wild_card_placex = card_placex
              if wild_card_placex >= 0 and card_placex <= 4:
                   which_hand = 3
              elif wild_card_placex >= 5 and card_placex <= 10:
                   which_hand = 2
              elif wild_card_placex >= 10 and card_placex <= 12:
                   which_hand = 1
              else:
                   logging.critical(("Error, cannot find which hand wild card is in?", which_hand))
              # now figure out what "card" player is using in place of wild_card
              best_wild_hand = [0,0]
              best_wild = ["none"]
              deck_of_cards = sorted(Deck().deal(1)[0], cmp = suit_rank_sort, reverse = True)
              deck_of_cards.remove("wild")
              # print deck_of_cards
              for wild in deck_of_cards:
                   players_13card_hand[wild_card_placex] = wild
                   # print "adding wild", players_13card_hand
                   if which_hand == 3:
                       wild_hand = score_final(players_13card_hand[0:5], "3")
                   elif which_hand == 2:
                       wild_hand = score_final(players_13card_hand[5:10], "2")
                   elif which_hand == 1:
                       wild_hand = score_final(players_13card_hand[10:13], "1")
                   else:
                       logging.critical(("Error, which_hand unknown", which_hand))
                   # print "wild card loop", wild, best_wild, wild_hand, best_wild_hand
                   if wild_hand[1] > best_wild_hand[1]:
                       best_wild_hand = wild_hand
                       best_wild = wild
              players_13card_hand[wild_card_placex] = best_wild
              print "best_wild", best_wild, players_13card_hand[wild_card_placex]
    logging.info((players_13card_hand))
    player_hand3 = score_final(players_13card_hand[0:5],"3")
    player_hand2 = score_final(players_13card_hand[5:10],"2")
    player_hand1 = score_final(players_13card_hand[10:13],"1")
    player_total = player_hand3[1] + player_hand2 [1] + player_hand1 [1]
    valid_hand = True
    if player_hand2 > player_hand3:
         valid_hand = False
    if player_hand1 > player_hand2:
         valid_hand = False
    if valid_hand == False:
         message = "Player Hand Invalid"
    else:
         message = "Player Hand Valid"
    print player_hand3
    print player_hand2
    print player_hand1
    print player_total
    x = 1200 + 170
    y = 10 + 30 + 20 + 90 + 40
    valid_hand_label = Label(text=message , fg="blue", bg="white")
    valid_hand_label.place(x=x, y=y)
    total_score_label = Label(text="total score = " + str(player_total), fg="blue", bg="white")
    total_score_label.place(x=x, y=y + 25)
    hand3_score_label = Label(text="hand3 = " + str(player_hand3), fg="blue", bg="white")
    hand3_score_label.place(x=x, y=y + 50)
    hand2_score_label = Label(text="hand2 = " + str(player_hand2), fg="blue", bg="white")
    hand2_score_label.place(x=x, y=y + 75)
    hand1_score_label = Label(text="hand1 = " + str(player_hand1), fg="blue", bg="white")
    hand1_score_label.place(x=x, y=y + 100)
    return player_total

    return

w = Tkinter.Canvas(top, height=900, width = 1528)
wins = 0
losses = 0
ties = 0
NUMBER_OF_CARDS = 13
image_dir = "Cards_gif/"
image_dict = create_images()

show_next_hand([])

show_next_hand_button = Button(top, text="Show Next Hand", command=show_next_hand)
show_best_hand_button = Button(top, text="Show Best Hand", command=show_best_hand)
show_player_score_button = Button(top, text="Player Score", command=show_player_score)
setup_hand_button = Button(top, text="Setup Hand", command=set_up_hand)
play_setup_hand_button = Button(top, text="Play Setup Hand", command=play_setup_hand)

show_next_hand_button.pack()
show_best_hand_button.pack()
show_player_score_button.pack(side=RIGHT)
setup_hand_button.pack(side=RIGHT)
play_setup_hand_button.pack(side=RIGHT)
w.pack()

w.tag_bind("token", "<Button-1>", onClick)
w.tag_bind("token", "<B1-Motion>", onMotion)
w.tag_bind("token", "<ButtonRelease-1>", onRelease)

top.mainloop()