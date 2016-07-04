import numpy as np
from game import *
from cards import *

####################################################################################################

INITIAL_DISTRIBUTION_CAPACITY = 32

class EndingPrediction:
  def __init__(self):
    '''
    Represents a prediction of when and how a given player will reach >= 15 points, assuming all
    players play optimally from the given board/player states at the end of a round. Optimal play
    here means optimizing the following objective functions in order:

    1. win the game
    2. minimize round # at which reach >= 15
    3. maximize # points
    4. minimize # cards

    The prediction takes the form of a probability distribution over (R, P, C) triples, where

    R = the round # at which player will reach >= 15 points
    P = # of points player will end with
    C = # of cards player will have when game ends

    If desired, a triple can contain NaN for some of its values, in which case it represents the
    associated marginal distribution.
    '''
    self.distribution = np.zeros((INITIAL_DISTRIBUTION_CAPACITY, 4))  # (w,R,P,C) rows

  def normalize(self):
    self.distribution[:,0] /= np.sum(self.distribution, axis=0)[0]

####################################################################################################

class AbstractPlayer:
  def get_action(self): pass
  def get_noble_claim(self, noble_candidates): pass
  def get_discard(self): pass
  def get_name(self): pass
  def init(self, index, player_state, board_state, public_player_states): pass
  def handle_card_deal_broadcast(self, card): pass
  def handle_take_coins_action_broadcast(self, action, player_index): pass
  def handle_reserve_card_action_broadcast(self, action, player_index): pass
  def handle_buy_public_card_action_broadcast(self, action, player_index): pass
  def handle_buy_reserved_card_action_broadcast(self, action, player_index): pass
  def handle_handle_discard_action_broadcast(self, action, player_index): pass


####################################################################################################

class SimpleHeadsUpAI:
  def __init__(self, name):
    self.name = name
    self.index = None
    self.my_state = None
    self.board_state = None
    self.public_player_states = None
    self.remaining_cards = None
    self.opponent_reserved_cards = []
  
  def handle_card_deal_broadcast(self, card):
     level_cards = self.remaining_cards[card.levels-1]
     self.remaining_cards[card.levels-1] = [c for c in level_cards if c.ID != card.ID]
  
  def handle_take_coins_action_broadcast(self, action, player_index): pass
  
  def handle_reserve_card_action_broadcast(self, action, player_index):
    if player_index == self.index: return
    if action.card is None:
      raise Exception('ERROR: SimpleHeadsUpAI cannot handle unknown-card reserves')
    self.opponent_reserved_cards.append(action.card)
  
  def handle_buy_public_card_action_broadcast(self, action, player_index): pass
  
  def handle_buy_reserved_card_action_broadcast(self, action, player_index):
    if player_index == self.index: return
    self.opponent_reserved_cards = [card for card in self.opponent_reserved_cards if card.ID != action.card.ID]
  
  def handle_handle_discard_action_broadcast(self, action, player_index): pass

  def _generate_candidate_actions(self):
    '''
    Simplification:
    
    * don't ever do something that causes you to discard coins or cards.
    * don't ever reserve a card that you could buy instead.
    * when buying any given card, don't spend gold coins when you can spend non-gold coins instead
    * don't reserve unknown cards
    '''
    actions = []
    
    public_state = self.state.public_player_state
    legal_take_actions = self.board_state.generate_legal_take_coin_actions()
    for take in legal_take_actions:
      if sum(take.coins) + sum(public_state.coins) <= PER_PLAYER_COIN_LIMIT:
        actions.append(take)

    can_reserve = public_state.num_reserved_cards < RESERVED_CARD_LIMIT
    for level in range(NUM_LEVELS):
      level_cards = self.board_state.cards[level]
      for (card_index, card) in enumerate(level_cards):
        # determine if can buy
        slack = public_state.coins[:NUM_COLORS] - card.cost
        shortfall = -np.sum(np.min(0, slack))
        if shortfall <= public_player_state.coins[COLORS.J]:
          buy = BuyPublicCardAction(level, card_index)
          buy.coins[:NUM_COLORS] = np.minimum(public_state.coins[:NUM_COLORS], card.cost)
          buy.coins[COLORS.J] = shortfall
          actions.append(buy)
        elif can_reserve:
          reserve = ReserveCardAction(level, card_index)
          actions.append(reserve)
    return actions

  def _estimate_win_probability(self, action):

    pass

  def get_action(self):
    candidate_actions = self._generate_candidate_actions()
    probs = [(self._estimate_win_probability(action), index) for (index, action) in enumerate(candidate_actions)]
    probs.sort()
    return candidate_actions[probs[-1][1]]

  def get_noble_claim(self, noble_candidates):
    # for now, just claim the first noble
    if len(noble_candidates)>1:
      print 'TODO: SimpleHeadsUpAI noble claim logic'
    return ClaimNobleAction(0)

  def get_discard(self):
    raise Exception('SimpleHeadsUpAI should never discard')

  def get_name(self):
    return name
  
  def init(self, index, player_state, board_state, public_player_states):
    self.index = index
    self.my_state = player_state
    self.board_state = board_state
    self.public_player_states = public_player_states
    
    init_card_ids = [set() for i in range(NUM_LEVELS)]
    for lvl in range(NUM_LEVELS):
      assert len(board_state.cards[lvl]) == NUM_CARDS_PER_LEVEL
      for card in board_state.cards[lvl]:
        init_card_ids[card.levels-1].add(card.ID)
    
    self.remaining_cards = [[] for i in range(NUM_LEVELS)]
    for card in Card.MASTER_LIST:
      if card.ID not in init_card_ids[card.levels-1]:
        self.remaining_cards[card.levels-1].append(card)

      
####################################################################################################

class SimpleSolitaireAI:
  def __init__(self):
    self.prediction = EndingPrediction()

  def get_name(self):
    return 'SimpleSolitaire'

  def get_action(self, board_state, public_player_states):
    pass

  def get_noble_claim(self, board_state, public_player_states, noble_choices):
    pass

  def get_discard(self, board_state, public_player_states):
    pass

  def receive_assignment(self, index, state):
    self.index = index
    self.state = state

