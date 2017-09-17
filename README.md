I am learning to program in Python and I thought I would use Russian Poker to teach me the language.

I learned to play Russian Poker with my friends as a child. Each player is dealt 13 cards and they need to set them up as three hands. The first is a 3-card hand, the second is a 5-card hand and the third is a 5-card hand with the addition provision that the third hand must be larger than the second hand and the second hand must be larger than the first hand. After setting up the cards, the players compete with the dealer's hand by comparing both first hands, then second hands and finally the third hands. Each hand follows the rules of regular poker in the following order: Straight Flush, Four of a Kind, Flush, Straight, Trips, Two Pair, One Pair and then Ace High. Most hands are worth one point, however, there are special hands that are worth more.
In the third hand, Straight Flush is worth 5 points 4 of a Kind is worth 4 points. In the second hand, those points are doubled, and Full House is worth 2 points. In the first hand, Trips are worth 3 points. To make it more interesting, I have added one wild card to the deck.

I have two different programs.

One is Interactive where you will see the thirteen cards and how the program plays it. Everytime you click the canvas, you are dealt another hand the program plays that hand optimally. This continues until you exit out of the program

The other program is Batch where the program will deal and play any number (enum) of hands optimally (as perceived by my program). This is used to generate a probability file which can be used to improve the program's playing ability.

Both programs share a module called deck_wild_v1 and require a directory of images Cards_gif.
