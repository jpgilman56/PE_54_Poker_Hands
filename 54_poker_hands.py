import re #regex import
from enum import Enum

#GLOBAL CONSTANTS
CARDS_IN_HAND = 5
NUM_OF_GAMES = 1000
PLAYERS = 2


TEST_HAND = [['2C', '4C', '4S', '5C', '6C'], ['7D', '2S', '5D', '3S', 'AC']]


class Suit(Enum):
	HEARTS = "H"
	DIAMONDS = "D"
	CLUBS = "C"
	SPADES = "S"

class CardValue(Enum):
	TWO = "2"
	THREE = "3"
	FOUR = "4"
	FIVE = "5"
	SIX = "6"
	SEVEN = "7"
	EIGHT = "8"
	NINE = "9"
	TEN = "T"
	JACK = "J"
	QUEEN = "Q"
	KING = "K"
	ACE = "A"

	def __lt__(self, other_card_value):
		return CARD_RANK[self] < CARD_RANK[other_card_value]

	def __gt__(self, other_card_value):
		return CARD_RANK[self] > CARD_RANK[other_card_value]
	


CARD_RANK = {
	CardValue.TWO: 2,
	CardValue.THREE: 3,
	CardValue.FOUR: 4,
	CardValue.FIVE: 5,
	CardValue.SIX: 6,
	CardValue.SEVEN: 7,
	CardValue.EIGHT: 8,
	CardValue.NINE: 9,
	CardValue.TEN: 10,
	CardValue.JACK: 11,
	CardValue.QUEEN: 12,
	CardValue.KING: 13,
	CardValue.ACE: 14
}


class HandType(Enum):
	HIGH_CARD = 1
	ONE_PAIR = 2
	TWO_PAIR = 3
	THREE_KIND = 4
	STRAIGHT = 5
	FLUSH = 6
	FULL_HOUSE = 7
	FOUR_KIND = 8
	STRAIGHT_FLUSH = 9
	ROYAL_FLUSH = 10


class Card:

	def __init__(self, card_string):
		self.card_value = CardValue(card_string[0])
		self.suit: Suit = Suit(card_string[1])

	def __repr__(self):
		return(f"Card: {self.card_value.value}{self.suit.value}")

	def __lt__(self, other_card):
		'''Allows less than comparison between cards, based on value'''
		return CARD_RANK[self.card_value] < CARD_RANK[other_card.card_value]

	def __gt__(self, other_card):
		'''Allows greater than comparison between cards, based on value'''
		return CARD_RANK[self.card_value] > CARD_RANK[other_card.card_value]


class Hand:

	def __init__(self, card_string_array: [str]):
		self.card__string_array = card_string_array
		self.card_array = []
		
		for card_string in card_string_array:
			self.card_array.append(Card(card_string))

		#Sort hand by ascending value of card
		self.card_array.sort(key= lambda card_array: CARD_RANK[card_array.card_value])

		self.hand_type: HandType = None
		self.hand_value_rank: [CardValue] = None

		self.find_hand()

	def __repr__(self):
		return f"Hand of type {self.hand_type} with value ranks {self.hand_value_rank}"

	def __eq__(self, other_hand):
		''' Allows equality test of two hands'''
		return HandType(self.hand_type).value == HandType(other_hand.hand_type).value and self.hand_value_rank == other_hand.hand_value_rank

	def __lt__(self, other_hand):
		'''Allows comparability of whether a hand is worse than another'''
		if HandType(self.hand_type).value < HandType(other_hand.hand_type).value:
			return True
		elif HandType(self.hand_type).value == HandType(other_hand.hand_type).value:
			return self.hand_value_rank < other_hand.hand_value_rank
		else:
			return False

	def __gt__(self, other_hand):
		'''Allows comparability of whether a hand is better than another'''
		if HandType(self.hand_type).value > HandType(other_hand.hand_type).value:
			return True
		elif HandType(self.hand_type).value == HandType(other_hand.hand_type).value:
			return self.hand_value_rank > other_hand.hand_value_rank
		else:
			return False



	def get_card_values(self) -> [CardValue]:
		return_array = []
		for card in self.card_array:
			return_array.append(card.card_value)
		return(return_array)

	def get_suits(self):
		return_array = []
		for card in self.card_array:
			return_array.append(card.suit)
		return(return_array)

	def value_counts(self):
		card_values = self.get_card_values()
		card_value_counts = []
		card_value_count_dict = dict()
		for card_value in card_values:
			card_value_count = card_values.count(card_value)
			card_value_counts.append(card_value_count)
			card_value_count_dict[card_value] = card_value_count

		value_rank = self.sort_value_rank_list(card_value_count_dict)

		return card_value_counts, value_rank

	def sort_value_rank_list(self, card_value_count_dict):

		'''
		Returns sorted CardValues from a dictionary of CardValues and their frequency, whereby they are sorted first by descending frequency and then in descending rank.
		'''

		value_rank_list = list(card_value_count_dict)
		value_rank_list.sort(reverse=True, key= lambda card_value: (card_value_count_dict[card_value], CARD_RANK[card_value]))
		
		return value_rank_list

	def find_hand(self):
		'''Sets HandType Enum '''
		value_counts, self.hand_value_rank = self.value_counts()

		sum_counts = sum(value_counts)

		hand_type: HandType = None

		##test of straight, flush, straight flush and royal flush first

		check_flush = self.check_flush()
		check_straight = self.check_straight()

		if check_straight and check_flush:
			if self.card_array[0].card_value == CardValue.TEN:
				self.hand_type = HandType.ROYAL_FLUSH
			else:
				self.hand_type = HandType.STRAIGHT_FLUSH
		elif check_flush:
			self.hand_type = HandType.FLUSH
		elif check_straight:
			self.hand_type = HandType.STRAIGHT
		else:
			if sum_counts == 5:
				self.hand_type = HandType.HIGH_CARD
			elif sum_counts == 7:
				self.hand_type = HandType.ONE_PAIR
			elif sum_counts == 9:
				self.hand_type = HandType.TWO_PAIR
			elif sum_counts == 11:
				self.hand_type = HandType.THREE_KIND
			elif sum_counts == 13:
				self.hand_type = HandType.FULL_HOUSE
			elif sum_counts == 17:
				self.hand_type = HandType.FOUR_KIND

	def check_straight(self) -> bool:
		straight_array = [CARD_RANK[self.get_card_values()[0]] + i for i in range(0,CARDS_IN_HAND)]
		test_array = [CARD_RANK[i] for i in self.get_card_values()]
		return straight_array == test_array 

	def check_flush(self) -> bool:
		suits = self.get_suits()
		return(suits.count(suits[0]) == CARDS_IN_HAND)

def hand_reader(file: str) -> [[[str], [str]]]:
	'''Reads hand strings from file and returns an array of games, each game having an array of hands'''

	games_array: [[[str], [str]]] = []
	
	try:
		f = open(file, "r")
		print("File opened succesfully")
	except:
		print("Error opening file")
	else:
		for i in range(NUM_OF_GAMES):
			line = f.readline()
			line_array = re.split("\s", line)

			games_array.append([line_array[0:CARDS_IN_HAND], line_array[CARDS_IN_HAND:CARDS_IN_HAND+CARDS_IN_HAND]])
		
		f.close()

		return games_array
		
		

def hand_generator(file):
	'''Generates Hand types from a file'''

	games_array = hand_reader(file)

	player1_array = [Hand(hand_string_array) for hand_string_array in player1_hands_string_array]
	player2_array = [Hand(hand_string_array) for hand_string_array in player1_hands_string_array]

	return player1_array, player2_array

def hand_comparison(file):

	player_wins = [0 for i in range(PLAYERS)]

	games_array = hand_reader(file)

	for game in games_array:
		hands: [Hand] = []
		for hand in game:
			hands.append(Hand(hand))

		winning_hand = max(hands)
		winner = hands.index(winning_hand)
		player_wins[winner] += 1

		print(f"Winner: Player {winner + 1} with a {winning_hand.hand_type}")

	print(player_wins)




print(hand_comparison("0054_poker.txt"))







