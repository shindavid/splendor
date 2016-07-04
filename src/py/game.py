import random
from cards import *
import numpy as np

class BoardState:
  def __init__(self):
    self.round_number = 0
    self.cards = [[] for i in range(NUM_LEVELS)]  # cards[i] consists of <=4 Card's whose levels==i+1
    self.remaining_card_counts = np.array([0 for i in range(NUM_LEVELS)])
    self.coins = np.array([0 for i in range(NUM_COLORS_INCLUDING_JOKER)])  # coins[color] is how many coins are left of that color
    self.nobles = []  # <=3 Noble's

  def deal(self, card):
    self.cards[card.levels-1].append(card)

  def remove(self, card):
    self.cards[card.levels-1].remove(card)

  def generate_legal_take_coin_actions(self):
    actions = []
    for C1 in range(NUM_COLORS):
      if not self.coins[C1]: continue
      if self.coins[C1] >= REQUIRED_STACK_SIZE_TO_TAKE_2_OF:
        take = TakeCoinsAction()
        take.coins[C1] = 2
        actions.append(take)
      
      for C2 in range(C1):
        if not self.coins[C2]: continue
        for C3 in range(C2):
          if not self.coins[C3]: continue
          
          take = TakeCoinsAction()
          take.coins[C1] = 1
          take.coins[C2] = 1
          take.coins[C3] = 1
          actions.append(take)

    return actions

class PublicPlayerState:
  def __init__(self):
    self.purchased_cards = []
    self.awarded_nobles = []
    self.coins = np.array([0 for i in range(NUM_COLORS_INCLUDING_JOKER)])
    self.num_reserved_cards = 0

    # derived fields
    self.discounts = np.array([0 for i in range(NUM_COLORS)])
    self.points = 0

  def add_purchased_card(self, card):
    self.purchased_cards.append(card)
    self.discounts += card.color_np_array()
    self.points += card.points
    self.validate()

  def add_claimed_noble(self, noble):
    self.awarded_nobles.append(noble)
    self.points += noble.points

  def validate(self):
    assert self.points == sum([card.points for card in self.purchased_cards]) + sum([noble.points for noble in self.awarded_nobles])
    assert self.discounts == np.sum(np.vstack([card.color_np_array() for card in self.purchased_cards]), axis=0)
    assert self.num_reserved_cards <= 3
    assert np.sum(self.coins) <= 10

class PlayerState:
  def __init__(self):
    self.public_player_state = PublicPlayerState()
    self.reserved_cards = []

class PlayerAction:
  pass

class TakeCoinsAction(PlayerAction):
  def __init__(self):
    self.coins = np.array([0 for i in range(NUM_COLORS)])

  def __str__(self):
    tokens = ['+']
    tokens.extend([color_to_str(c) * n for (c,n) in enumerate(self.coins)])
    return ''.join(tokens)

class ReserveCardAction(PlayerAction):
  def __init__(self, levels, index):
    self.levels = levels
    self.index = index  # -1 means reserve from top of deck
    self.card = None  # will be set by GameManager

  def __str__(self):
    return 'reserve'

class BuyPublicCardAction(PlayerAction):
  def __init__(self, levels, index):
    self.levels = levels
    self.index = index
    self.coins = np.array([0 for i in range(NUM_COLORS_INCLUDING_JOKER)])

  def __str__(self):
    tokens = ['buy-']
    tokens.extend([color_to_str(c) * n for (c,n) in enumerate(self.coins)])
    return ''.join(tokens)

class BuyReservedCardAction(PlayerAction):
  def __init__(self, reserved_index):
    self.reserved_index = reserved_index
    self.coins = np.array([0 for i in range(NUM_COLORS_INCLUDING_JOKER)])
    self.card = None  # will be set by GameManager

  def __str__(self):
    return 'reserve unk'

class TriggeredAction:
  pass

class DiscardCoinAction(TriggeredAction):
  def __init__(self):
    self.coins = np.array([0 for i in range(NUM_COLORS_INCLUDING_JOKER)])

  def __str__(self):
    tokens = ['discard-']
    tokens.extend([color_to_str(c) * n for (c,n) in enumerate(self.coins)])
    return ''.join(tokens)

class ClaimNobleAction(TriggeredAction):
  def __init__(self, noble_index):
    self.noble_index = noble_index

  def __str__(self):
    return 'noble'

class GameState:
  num_coins_to_use = {2:4, 3:5, 4:7}
  num_nobles_to_use = {2:3, 3:4, 4:5}

  def __init__(self, seed, players):
    self.num_players = len(players)

    random.seed(seed)

    shuffled_cards = [card for card in Card.MASTER_LIST]
    shuffled_nobles = [noble for noble in Noble.MASTER_LIST]
    shuffled_players = [p for in players]
    random.shuffle(shuffled_cards)
    random.shuffle(shuffled_nobles)
    random.shuffle(shuffled_players)
    
    self.board_state = BoardState()
    self.all_cards = [[], [], []]  # all_cards[i] consists of all Card ID's whose levels==i+1
    self.card_indices = [0, 0, 0]  # card_indices[i] represents next card to be dealt with levels==i+1
    for card in shuffled_cards:
      self.all_cards[card.levels-1].append(card)
      self.board_state.remaining_card_counts[card.levels-1] += 1

    for levels in (1,2,3):
      L = levels-1
      for i in range(NUM_CARDS_PER_LEVEL):
        card = self.deal_card(levels)
        self.board_state.cards[L].append(card)

    for color in range(NUM_COLORS):
      self.board_state.coins[color] = GameState.num_coins_to_use[self.num_players]
    self.board_state.coins[COLORS.J] = NUM_JOKERS

    self.board_state.nobles.extend(shuffled_nobles[:GameState.num_nobles_to_use[self.num_players]])

    self.players = shuffled_players
    self.player_states = [PlayerState() for p in shuffled_players]
    self.current_player_index = 0

  def deal_card(self, levels):
    L = levels-1
    N = self.card_indices[L]
    if N >= len(self.all_cards[L]): return None

    self.board_state.remaining_card_counts[L] -= 1
    self.card_indices[L] += 1
    return self.all_cards[L][N]

  def get_public_player_states(self):
    return [state.public_player_state for state in self.player_states]

  def do_turn(self, player_index):
    action = self.players[player_index].get_action()
    self.validate_action(action, player_index)
    self.handle_action(action, player_index):
    self.replenish_board_cards()
    self.force_coin_discard(player_index):
    self.award_nobles(player_index)

  def award_nobles(self, player_index):
    player_state = self.player_states[player_index]
    public_player_state = player_state.public_player_state
    candidates = [i for (i,x) in enumerate(self.nobles) if public_player_state.discounts >= x.requirement]
    if not candidates: return

    action = self.players[player_index].get_noble_claim(candidates)

    claimed_noble = candidates[action.noble_index]
    public_player_state.add_claimed_noble(claimed_noble)

  def force_coin_discard(self, player_index):
    player_state = self.player_states[player_index]
    public_player_state = player_state.public_player_state
    num_coins = sum(public_player_state.coins)
    if num_coins <= PER_PLAYER_COIN_LIMIT: return
    
    num_coins_to_discard = PER_PLAYER_COIN_LIMIT - num_coins

    action = self.players[player_index].get_discard()
    assert action.coins >= 0
    assert sum(action.coins) == num_coins_to_discard
    public_player_state.coins -= action.coins

    for (index, player) in enumerate(self.players):
      player.handle_dicard_action_broadcast(action, player_index)

  def replenish_board_cards(self):
    for (L,subcards) in enumerate(self.board_state.cards):
      for (i,card) in enumerate(subcards):
        if card is None:
          subcards[i] = self.deal_card(L+1)
          self.broadcast_card_deal(subcards[i])

      self.board_state.cards[L] = [card for in subcards if card is not None]

  def broadcast_card_deal(self, card):
    for player in self.players:
      player.handle_card_deal_broadcast(card)

  def validate_action(self, action, player_index):
    player_state = self.player_states[player_index]
    public_player_state = player_state.public_player_state
    if isinstance(action, TakeCoinsAction):
      assert action.taken >= 0
      assert self.board_state.coins >= action.taken

      num_taken = np.sum(action.taken)
      if num_taken == 1:
        # only 1 coin taken, only allowed if board only had 1 stack available. And we'll say that the
        # player has to taken 2-of if possible
        assert len(np.any(self.board_state.coins)) == 1
        assert np.max(self.board_state.coins) < REQUIRED_STACK_SIZE_TO_TAKE_2_OF
      elif num_taken == 2:
        if 2 in action.taken:
          assert self.board_state.coins[np.argmax(action.taken)] >= REQUIRED_STACK_SIZE_TO_TAKE_2_OF
        else:
          # took 2 distinct, not allowed if board had 3 different stacks available
          assert len(np.any(self.board_state.coins)) == 2
      elif num_taken == 3:
        pass
      else:
        raise Exception('Invalid action by player %s: %s' % (self.get_player_name(player_index), str(action)))
    elif isinstance(action, ReserveCardAction):
      assert public_player_state.num_reserved_cards < RESERVED_CARD_LIMIT

      if action.index == -1:
        assert self.board_state.remaining_card_counts[action.levels-1] > 0
      else:
        assert action.index in range(len(self.board_state.cards[action.levels-1]))
        # NOTE(dshin) The iOS app doesn't allow you to reserve cards that you can buy. I think that
        # is simply to provide a nicer interface. The rules technically allow this, so I will too.
    elif isinstance(action, BuyPublicCardAction):
      card = self.board_state.cards[action.levels-1][action.index]
      self.validate_card_purchase(public_player_state, card)
    elif isinstance(action, BuyReservedCardAction):
      card = player_state.reserved_cards[action.reserved_index]
      self.validate_card_purchase(public_player_state, card)
    else:
      raise Exception('Unknown action type "%s"' % type(action))

  def validate_card_purchase(self, public_player_state, card):
    slack = public_player_state.coins[:NUM_COLORS] - card.cost
    shortfall = -np.sum(np.min(0, slack))
    assert shortfall <= public_player_state.coins[COLORS.J]

  def handle_action(self, action, player_index):
    player_state = self.player_states[player_index]
    public_player_state = player_state.public_player_state
    if isinstance(action, TakeCoinsAction):
      public_player_state.coins[:NUM_COLORS] += action.coins
      for (index, player) in enumerate(self.players):
        player.handle_take_coins_action_broadcast(action, player_index)
    elif isinstance(action, ReserveCardAction):
      if self.board_state.coins[COLORS.J] > 0:
        public_player_state.coins[COLORS.J] += 1
        self.board_state.coins[COLORS.J] -= 1
      
      if action.index == -1:
        card = self.deal_card(action.levels)
        action.card = None
      else:
        card = self.board_state.cards[action.levels-1][action.index]
        self.board_state.cards[action.levels-1][action.index] = None
        action.card = card
      
      player_state.reserved_cards.append(card)
      for (index, player) in enumerate(self.players):
        player.handle_reserve_card_action_broadcast(action, player_index)
    elif isinstance(action, BuyPublicCardAction):
      public_player_state.coins -= action.coins
      self.board_state.coins += action.coins
      card = self.board_state.cards[action.levels-1][action.index]
      public_player_state.add_purchased_card(card)
      self.board_state.cards[action.levels-1][action.index] = None
      for (index, player) in enumerate(self.players):
        player.handle_buy_public_card_action_broadcast(action, player_index)
    elif isinstance(action, BuyReservedCardAction):
      public_player_state.coins -= action.coins
      self.board_state.coins += action.coins
      card = player_state.reserved_cards[action.reserved_index]
      action.card = card
      public_player_state.add_purchased_card(card)
      del player_state.reserved_cards[action.reserved_index]
      for (index, player) in enumerate(self.players):
        player.handle_buy_reserved_card_action_broadcast(action, player_index)

  def get_player_name(self, player_index):
    return self.players[player_index].get_name()

  def get_winners(self):
    score_map = collections.defaultdict(list)
    for (i,state) in enumerate(self.player_states):
      state.public_player_state.validate()
      score_key = (state.public_player_state.score, -len(state.purchased_cards))
      score_map[score_key].append(self.players[i])

    max_score_key = max(score_map)
    return score_map[max_score_key] 

class GameManager:
  def __init__(self, seed, players):
    self.game_state = GameState(seed, players)
    for (index, player) in enumerate(self.game_state.players):
      player.init(index, self.game_state.player_states[index], self.board_state,
          [player_state.public_player_state for player_state in self.game_state.player_states])

  def start(self):
    while self.game_state.get_max_score() < GAME_ENDING_SCORE:
      for player_index in range(self.game_state.num_players):
        self.game_state.do_turn(player_index)
      self.game_state.board_state.round_number += 1

    winners = self.get_winners()
    print 'Winner: %s' % (','.join([p.get_name() for p in winners]))

