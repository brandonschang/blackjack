import random
import math

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():																		#card object

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.value = values[rank]

	def __str__(self):
		return f'{self.rank} of {self.suit}'

class Deck():																		#deck object, which contains a list of all cards

	def __init__(self):
		self.deck = []

		for rank in ranks:															#embedded for loop that creates every card in the deck
			for suit in suits:
				self.deck.append(Card(rank,suit))

	def __str__(self):
		deck_comp = ''
		for card in self.deck:
			deck_comp += '\n ' + card.__str__()
		return 'The deck has: ' + deck_comp

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		return self.deck.pop()

class Hand():																		#hand object, which contains a list of cards

	def __init__(self):
		self.cards = []
		self.value = 0
		self.aces = 0

	def add_card(self, card):
		self.cards.append(card)
		self.value += card.value
		if card.rank == 'Ace':
			self.aces += 1

	def adjust_for_ace(self):
		while (self.value > 21 and self.aces > 0):
			self.value -= 10
			self.aces -= 1

	def remove_card(self):
		return self.cards.pop()

class Chips():																		#chips object, which represents the player's balance in chips

	def __init__(self, total):
		self.total = total
		self.bet = 0
		self.winnings = 0

	def win_bet(self):
		self.total += self.bet
		self.winnings += self.bet

	def lose_bet(self):
		self.total -= self.bet
		self.winnings -= self.bet

	def win_blackjack(self):
		self.total = self.total + int(math.ceil(1.5*self.bet)) 
		self.winnings = self.winnings + int(math.ceil(1.5*self.bet))

	def win_double_down(self):
		self.total += 2*self.bet
		self.winnings += 2*self.bet

	def lose_double_down(self):
		self.total -= 2*self.bet 
		self.winnings -= 2*self.bet

def add_funds(chips):																#function that adds more money to a player's chips 

	while True:
		try:
			more_chips  = int(input('How much money are you cashing in for chips? '))
		except:
			print('Invalid response. Please input an integer value. ')
		else:
			if (more_chips < 0):
				print('Invalid response. Please input a value greater than zero. ')
			elif (more_chips == 0):
				print('Invalid response. You cannot cash in $0. ')
			else:
				chips.total += more_chips
				break

def take_bet(chips):																#function that takes a player's bet for a new hand

	global broke
	broke = False

	while True:
		try:
			chips.bet = int(input('How much would you like to bet? '))
		except:
			print('Invalid bet. Please input an integer (chip) value. ')
		else:
			if (chips.bet < 0):
				print('Invalid response. Please input a bet greater than zero. ')
			elif (chips.bet == 0):
				print('Invalid response. Bet cannot be $0. ')
			elif (chips.bet > chips.total):
				more_chips = input(f'You currently have ${chips.total} in chips, which is not enough to place this bet. \
Would you like to cash in for more chips? ').lower()
				if more_chips[0] == 'y':
					add_funds(player_chips)
					print(f'Funds added. You now have ${chips.total} in chips. You will need to restate your bet. ')
				elif more_chips[0] == 'n':
					repeat_bet = input('Would you like to place a lower bet? ')
					if repeat_bet[0] == 'y':
						continue
					else:
						broke = True
						break
				else:
					print('I don\'t know what your response means. Please place your bet again. ')
			else:
				break

def hit(deck, hand):																#hit function

	hand.add_card(deck.deal())
	hand.adjust_for_ace()

def double_down(deck, hand):														#double down function
	hand.add_card(deck.deal())
	hand.adjust_for_ace()

def split(deck, hand, chips):														#split function
	
	global split_hand_1
	global split_hand_2
	global double_1
	global double_2
	double_1 = False
	double_2 = False

	split_hand_1 = Hand()
	split_hand_2 = Hand()

	split_hand_1.add_card(hand.remove_card())
	split_hand_2.add_card(hand.remove_card())

	add_action = ' stand(s), or double down(d)? '

	count = 0
	hand_count = 1
	split_show_some(split_hand_1, split_hand_2, dealer_hand)
	while True:
		if (split_hand_1.value > 21):
			if hand_count == 1:
				split1_bust(chips)
				hand_count += 1
				count = 0
				add_action = ' stand(s), or double down(d)? '
		elif (split_hand_2.value > 21):
			split2_bust(chips)
			split_show_some(split_hand_1, split_hand_2, dealer_hand)
			break

		if (hand_count == 1):													#1st split hand actions
			print('\nYou are now playing your 1st split hand. \n')
			move = input('Would you like to hit(h),' + add_action).lower()
			if move == '':
				print('No response entered. Please try again. ')
			elif move[0] == 'd':
				if count > 0:
					print('Invalid response. You cannot double down after your first move. ')
				elif chips.total >= chips.bet*2:
					double_down(deck, split_hand_1)
					split_show_some(split_hand_1, split_hand_2, dealer_hand)
					double_1 = True
					hand_count += 1
				else:
					print('You do not have enough chips to double down on this hand. ')
					add_action = ' or stand(s)? '
			elif move[0] == 'h':
				hit(deck, split_hand_1)
				split_show_some(split_hand_1, split_hand_2, dealer_hand)
				add_action = ' or stand(s)? '
				count += 1
			elif move[0] == 's':
				print('Player stands on 1st hand. \n')
				add_action = ' stand(s), or double down(d)? '
				hand_count += 1
				count = 0
			else:
				print('Invalid response. ')
		elif (hand_count == 2):													#2nd split hand actions
			print('\nYou are now playing your 2nd split hand. \n')
			move = input('Would you like to hit(h),' + add_action).lower()
			if move == '':
				print('No response entered. Please try again. ')
			elif move[0] == 'd':
				if count > 0:
					print('Invalid response. You cannot double down after your first move. ')
				elif chips.total >= chips.bet*2:
					double_down(deck, split_hand_2)
					split_show_some(split_hand_1, split_hand_2, dealer_hand)
					double_2 = True
					break
				else:
					print('You do not have enough chips to double down on this hand. ')
					add_action = ' or stand(s)? '
			elif move[0] == 'h':
				hit(deck, split_hand_2)
				split_show_some(split_hand_1, split_hand_2, dealer_hand)
				add_action = ' or stand(s)? '
				count += 1
			elif move[0] == 's':
				print('Player stands on 2nd hand. ')
				break
			else:
				print('Invalid response. ')

def aces_split(deck, hand):														#split function if splitting aces

	global split_hand_1
	global split_hand_2
	global double_1
	global double_2
	double_1 = False
	double_2 = False
	
	split_hand_1 = Hand()
	split_hand_2 = Hand()

	split_hand_1.add_card(hand.remove_card())
	split_hand_2.add_card(hand.remove_card())
	hit(deck, split_hand_1)
	hit(deck, split_hand_2)

def actions(deck, hand, chips):													#actions function

	global playing
	global double
	global splitted
	double = False
	splitted = False
	count = 0

	if (hand.cards[0].value == hand.cards[1].value):
		add_action = ' stand(s), double down(d), or split(x)? '
	else:
		add_action = ' stand(s), or double down(d)? '

	while True:
		
		if (hand.value > 21):
			break

		move = input('Would you like to hit(h),' + add_action).lower()
		if move == '':
			print('No response entered. Please try again. ')
		elif move[0] == 'd':
			if (count > 0): 
				print('Invalid response. You cannot double down after your first move. ')
			elif (chips.total >= chips.bet*2):
				double_down(deck, hand)
				show_some(player_hand, dealer_hand)
				double = True
				count += 1
				break
			else:
				print('You do not have enough chips to double down. ')
				add_action = ' or stand(s)? '
		elif move[0] == 'h':
			hit(deck, hand)
			show_some(player_hand, dealer_hand)
			add_action = ' or stand(s)? '
			count += 1
		elif (move[0] == 'x' or move == 'split'):
			if (count > 0):
				print('Invalid response. You cannot split after your first move. ')
			elif (hand.cards[0].value != hand.cards[1].value):
				print('Invalid response. You cannot split different value cards. ')
			elif (hand.cards[0].rank == 'Ace'):
				aces_split(deck, hand)
				splitted = True
				break
			else:
				split(deck, hand, chips)
				splitted = True
				break 
		elif move[0] == 's':
			print('Player stands. Dealer is playing. ')
			playing = False
			break
		else:
			print('Invalid response. ')

def show_some(player, dealer):												#function that shows player's cards and hides dealer's first card

	print('\nDealer\'s Hand: ')
	print(' <card hidden> ')
	print('',dealer.cards[1])
	print('\nPlayer\'s Hand: ', *player.cards, sep = '\n')
	print(f'Player\'s Hand = {player.value}\n')

def split_show_some(hand1, hand2, dealer):									#function that shows player's split cards and hides dealer's first card

	print('\nDealer\'s Hand: ')
	print(' <card hidden> ')
	print('',dealer.cards[1])
	print('\nPlayer\'s 1st Split Hand: ', *hand1.cards, sep = '\n')
	print(f'Player\'s 1st Split Hand = {hand1.value}')
	print('\nPlayer\'s 2nd Split Hand: ', *hand2.cards, sep = '\n')
	print(f'Player\'s 2nd Split Hand = {hand2.value}\n')


def show_all(player, dealer):												#function that shows all cards on the table

	print('\nDealer\'s Hand: ', *dealer.cards, sep = '\n')
	print(f'Dealer\'s Hand = {dealer.value}')
	print('\nPlayer\'s Hand: ', *player.cards, sep = '\n')
	print(f'Player\'s Hand = {player.value}\n')

def split_show_all(hand1, hand2, dealer):									#function that shows both player's split cards and dealer's cards

	print('\nDealer\'s Hand: ', *dealer.cards, sep = '\n')
	print(f'Dealer\'s Hand = {dealer.value}')
	print('\nPlayer\'s 1st Split Hand: ', *hand1.cards, sep = '\n')
	print(f'Player\'s 1st Split Hand = {hand1.value}')
	print('\nPlayer\'s 2nd Split Hand: ', *hand2.cards, sep = '\n')
	print(f'Player\'s 2nd Split Hand = {hand2.value}\n')	

def player_busts(chips):
	print('Player busts! \n')
	chips.lose_bet()

def player_wins(chips):
	print('Player wins! \n')
	chips.win_bet()

def dealer_busts(chips):
	print('Dealer busts! Player wins. \n')
	chips.win_bet()

def dealer_wins(chips):
	print('Dealer wins! \n')
	chips.lose_bet()

def player_blackjack(chips):
	print('BlackJack! Congrats! \n')
	chips.win_blackjack()

def dealer_blackjack(chips):
	print('Dealer got BlackJack. Better luck next time! \n')
	chips.lose_bet()

def player_wins_double_down(chips):
	print('Player wins double down bet! \n')
	chips.win_double_down()

def player_lose_double_down(chips):
	print('Player loses double down bet. \n')
	chips.lose_double_down()

def split1_bust(chips):
	print('1st split hand busts! \n')
	chips.lose_bet()

def split2_bust(chips):
	print('2nd split hand busts! \n')
	chips.lose_bet()

def split1_lose(chips):
	print('Dealer beats 1st split hand! \n')
	chips.lose_bet()

def split2_lose(chips):
	print('Dealer beats 2nd split hand! \n')
	chips.lose_bet()

def split1_doubledown_lose(chips):
	print('Dealer beats 1st split hand! Player loses double down bet. ')
	chips.lose_double_down()

def split2_doubledown_lose(chips):
	print('Dealer beats 2nd split hand! Player loses double down bet. ')
	chips.lose_double_down()

def split1_win(chips):
	print('1st split hand wins! \n')
	chips.win_bet()

def split2_win(chips):
	print('2nd split hand wins! \n')
	chips.win_bet()

def split1_doubledown_win(chips):
	print('1st split hand wins double down bet! ')
	chips.win_double_down()

def split2_doubledown_win(chips):
	print('2nd split hand wins double down bet! ')
	chips.win_double_down()

def split1_push(chips):
	print('1st split hand and dealer push! \n')

def split2_push(chips):
	print('2nd split hand and dealer push! \n')

def push():
	print('Player and Dealer tie! It\'s a push. \n')

print('Welcome to BlackJack! Get as close as you can to 21 without going over! Dealer must hit until the value of his cards is at least 17. \
An ace can count as either 1 or 11. Good luck! ')

game_on = True
player_chips = Chips(0)
add_funds(player_chips)
quit = False

while game_on:																#main game logic

	deck = Deck()
	deck.shuffle()

	player_hand = Hand()
	dealer_hand = Hand()
	player_chips.winnings = 0

	player_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())

	if player_hand.value > 21:
		player_hand.adjust_for_ace()
	if dealer_hand.value > 21:
		dealer_hand.adjust_for_ace()

	if player_chips.total == 0:	
		while True:															#checks to see if player's chip balance is zero
			more_funds = input(f'You currently have $0 in chips. Would you like to cash in for more chips? ').lower()
			if more_funds[0] == 'y':
				add_funds(player_chips)
				break
			elif more_funds[0] == 'n':
				print('Thanks for playing! Better luck next time. ')
				quit = True
				break
			else:
				print('I don\'t know what that response means. ')
	if quit:
		break

	take_bet(player_chips)
	if broke:
		print('Thanks for playing! Better luck next time. ')
		break

	show_some(player_hand, dealer_hand)

	while playing:															#playing loop. exits if player busts or stands

		if (dealer_hand.value == 21):
			if (player_hand.value == 21):
				show_all(player_hand, dealer_hand)
				push()
			else:
				show_all(player_hand, dealer_hand)
				dealer_blackjack(player_chips)
			break

		if (player_hand.value == 21):
			player_blackjack(player_chips)
			break	

		actions(deck, player_hand, player_chips)

		if splitted:														#separate loop if player splits
			if (split_hand_1.value > 21 and split_hand_2.value > 21):
				break

			while (dealer_hand.value < 17):
				hit(deck, dealer_hand)
			
			split_show_all(split_hand_1, split_hand_2, dealer_hand)
			if (split_hand_1.value > 21):
				print('1st split hand busted. ')
				pass
			elif (split_hand_1.value > dealer_hand.value):
				if double_1:
					split1_doubledown_win(player_chips)
				else:
					split1_win(player_chips)	
			elif (split_hand_1.value == dealer_hand.value):
				split1_push(player_chips)
			else:
				if double_1:
					split1_doubledown_lose(player_chips)
				else:
					split1_lose(player_chips)

			if (split_hand_2.value > 21):
				print('2nd split hand busted. ')
				break
			elif (split_hand_2.value > dealer_hand.value):
				if double_2:
					split2_doubledown_win(player_chips)
				else:
					split2_win(player_chips)
			elif (split_hand_2.value == dealer_hand.value):
				split2_push(player_chips)
			else:
				if double_2:
					split2_doubledown_lose(player_chips)
				else:
					split2_lose(player_chips)

			break

		if (player_hand.value > 21):
			show_all(player_hand, dealer_hand)
			if double:
				player_lose_double_down(player_chips)
				break
			else:
				player_busts(player_chips)
				break

		show_some(player_hand, dealer_hand)

		while (dealer_hand.value < 17):
			hit(deck, dealer_hand)

		show_all(player_hand, dealer_hand)

		if (dealer_hand.value > 21):
			if double:
				print('Dealer busts! ')
				player_wins_double_down(player_chips)
			else:	
				dealer_busts(player_chips)

		elif (player_hand.value > dealer_hand.value):
			if double:
				player_wins_double_down(player_chips)
			else:
				player_wins(player_chips)

		elif (player_hand.value < dealer_hand.value):
			if double:
				player_lose_double_down(player_chips)
			else:
				dealer_wins(player_chips)

		else:
			push()

		break

	if player_chips.winnings > 0:
		print(f'\nPlayer, you won ${player_chips.winnings} that hand. ')
	elif player_chips.winnings < 0:
		player_chips.winnings *= -1
		print(f'\nPlayer, you lost ${player_chips.winnings} that hand. ')
	else:
		print('\nPlayer, you broke even that hand. ')
	print(f'You currently have ${player_chips.total} in chips. ')

	while True:
		response = input('\nWould you like to play another hand? ').lower()
		if response[0] == 'n':
			print('Thanks for playing! ')
			game_on = False
			break
		elif response[0] == 'y':
			playing = True
			break
		else:
			print('I don\'t know what that response means. Please input a YES or NO. ')
