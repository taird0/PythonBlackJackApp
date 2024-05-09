import itertools
import random

class DeckOfCards:
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    cards = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, "Jack", "Queen", "King"]
    
    def __init__(self):
        #Creates a deck of cards for use in game
        self.deck = list(itertools.product(self.cards, self.suits))

    def __repr__(self):
        message = ""
        #Creates a list of every card in deck and returns as a string
        for card, suit in self.deck:
            message += "The %s of %s. " % (card, suit)
        return "Current cards in deck: " + message

    def shuffle_deck(self):
        #Shuffles the deck so it is in a random order
        random.shuffle(self.deck)
        print("Shuffling deck!")

    def deal_hands(self, dealer, player):
        #This starts a new round resetting the dealer and player hands and taking bet from player
        dealer.hand = []
        player.hand = []
        player.data["Chips"] -= 1
        while (len(player.hand) < 2):
            dealer.hand.append(self.hit_me())
            player.hand.append(self.hit_me())  
    
    def hit_me(self):
        #Returns last value in deck and removes it from list
        return self.deck.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.data = {"Hands Played": 0, "Hands Won": 0, "Chips" : 10}
        self.hand = []
    
    def __repr__(self):
        return self.name + ": " + "".join("{}: {} | ".format(a, b) for a, b in self.data.items())


    def get_winner(self, dealer):
        if self.get_hand_value() > 21:
            print("%s is Bust!" % self.name)
            return dealer
        elif dealer.get_hand_value() > 21:
            print("%s is Bust!" % dealer.name)
            return self
        elif self.get_hand_value() > dealer.get_hand_value():
            return self
        else:
            return dealer

    def print_hand(self):
        #Starts by adding the players name to message string
        print_string = self.name + ": "
        #loops through all cards in hand and adds them to the message string
        for cards in self.hand:
            print_string += "| %s of %s " % (cards[0], cards[1])
        #Prints the string to the user
        print(print_string) 

    def check_blackjack(self):
        if self.get_hand_value() == 21:
            return True
        return False

    def get_hand_value(self):
        score = 0
        
        for cards in self.hand:
            match cards[0]:
                case "Jack" | "Queen" | "King":
                    score += 10
                case "Ace":
                    if score + 11 > 21:
                        score += 1
                    else: 
                        score += 11
                case _: 
                    score += cards[0]
        return score 
        



#Prints ASCII Art banner from file
with open('BlackJackASCIIArt.txt') as art:
    print(''.join(line for line in art))

#Gives Rules to player
print("You start with 10 chips, bet 1 to play a hand. Bankrupt the dealer to win")
#Gets players name (default value "Player")
usr_name = input("To start enter your name! \n")

#Creates new Player with user input
if usr_name == "":
    usr_name = "Player"

player = Player(usr_name)

#Creates the Dealer object
dealer = Player("Dealer")

#Game plays as long as player and dealer have chips to play
while(player.data["Chips"] > 0 and dealer.data["Chips"] > 0):

    #Prints object information to player
    print(dealer)
    print(player)

    #Waits for user input to continue
    input("Press enter to place your bets! \n")

    #Creates a deck of cards to be used in game
    deck = DeckOfCards()
    #Shuffles the cards
    deck.shuffle_deck()
    #Deals hands
    deck.deal_hands(dealer, player)

    #Increments hands played for dealer by one
    dealer.data["Hands Played"] += 1
    #Increments hands played for player by one
    player.data["Hands Played"] += 1

    #Prints the dealers hand to player
    dealer.print_hand()

    #Prints the players hand to player
    player.print_hand()

    #Hit me, Stand etc.
    while(player.get_hand_value() < 22 and dealer.get_hand_value() < 22 and not player.check_blackjack() and not dealer.check_blackjack()):


        #Gets instructions from user
        choice = input("Stand: S | Hit Me! H \n")

        match choice:
            case "H" | "h":
                #Gives user another card from deck
                player.hand.append(deck.hit_me())
                player.print_hand()
                continue
            case "S" | "s":
                print("Stand your ground!")               
            case _:
                print("That wasn't right..")
                continue

        #Dealer will always hit below 17
        while(dealer.get_hand_value() < 17):
        #Dealers decision
            print("Dealer hits!")
            dealer.hand.append(deck.hit_me())
            dealer.print_hand()
        print("The dealer stands")
        break
        
    
        #########################################################################################################################
        #Decide Winner

        #if player bust - dealer wins
    
        #Checks if anyone got blackjack
    
    winner = player.get_winner(dealer)

    #Checks if anyone got blackjack
    if player.check_blackjack():
        print("You got blackjack!")
        player.data["Chips"] += 1 # extra chip for Blackjack
        
    elif dealer.check_blackjack():
        print("The dealer got Blackjack.. Bad luck")
        

    if winner == player:
        player.data["Hands Won"] += 1
        player.data["Chips"] += 1
        dealer.data["Chips"] -= 1
        print("%s Wins!" % player.name)
    else:
        dealer.data["Hands Won"] += 1
        print("%s Wins!" % dealer.name)

#Game Over
if player.data["Chips"] <= 0:
    print("Sorry you don't have enough chips to play.. Better luck next time!")
#You Win!
else:
    print("You Win!! Well done %s" % player.name)



#More commenting - remember people might look at this in the future