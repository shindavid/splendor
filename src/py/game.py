import random
from cards import *

class BoardState:
  def __init__(self):
    self.cards = [[], [], []]  # cards[i] consists of <=4 Card's whose levels==i+1
    self.coins = [0 for i in range(6)]  # coins[color] is how many coins are left of that color
    self.nobles = []  # <=3 Noble's

  def deal(self, card):
    self.cards[card.levels-1].append(card)

  def remove(self, card):
    self.cards[card.levels-1].remove(card)

class PublicPlayerState:
  def __init__(self):
    self.purchased_cards = []
    self.awarded_nobles = []
    self.coins = [0 for i in range(6)]

    # derived fields
    self.discounts = [0 for i in range(5)]
    self.points = 0

  def validate(self):
    assert self.points == sum([card.points for card in self.purchased_cards]) + sum([noble.points for noble in self.awarded_nobles])
    assert self.discounts == [sum(x) for x in zip(*[card.color_tuple() for card in self.purchased_cards])]
    assert len(self.reserved_cards) <= 3
    assert sum(self.coins) <= 10

class PlayerState:
  def __init__(self):
    self.public_player_state = PublicPlayerState()
    self.reserved_cards = []

class GameState:
  num_coins_to_use = {2:4, 3:5, 4:7}
  num_nobles_to_use = {2:3, 3:4, 4:5}

  def __init__(self, seed, players):
    num_players = len(players)

    random.seed(seed)
    shuffled_cards = [card for card in Card.MASTER_LIST]
    shuffled_nobles = [noble for noble in Noble.MASTER_LIST]
    shuffled_players = [p for in players]
    random.shuffle(shuffled_cards)
    random.shuffle(shuffled_nobles)
    random.shuffle(players)
    
    self.board_state = BoardState()
    self.all_cards = [[], [], []]  # all_cards[i] consists of all Card ID's whose levels==i+1
    self.card_indices = [0, 0, 0]  # card_indices[i] represents next card to be dealt with levels==i+1
    for card in shuffled_cards:
      self.all_cards[card.levels-1].append(card)
    
    for levels in (1,2,3):
      for i in range(4):
        self.deal_card(levels)

    for color in range(5):
      self.board_state.coins[color] = GameState.num_coins_to_use[num_players]
    self.board_state.coins[J] = 5

    self.board_state.nobles.extend(shuffled_nobles[:GameState.num_nobles_to_use[num_players]])

    self.players = players
    self.player_states = [PlayerState() for p in players]
    self.current_player_index = 0

  def deal_card(self, levels):
    L = levels-1
    N = self.card_indices[L]
    if N >= len(self.all_cards[L]): return

    self.board_state.cards[L].append(self.all_cards[L][N])
    self.card_indices[L] += 1

