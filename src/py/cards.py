import sys
import traceback

W = 0
U = 1
G = 2
R = 3
B = 4

def cost_dict_to_tuple(cost_dict):
  w = cost_dict.get(W, 0)
  u = cost_dict.get(U, 0)
  g = cost_dict.get(G, 0)
  r = cost_dict.get(R, 0)
  b = cost_dict.get(B, 0)
  return (w, u, g, r, b)

def color_to_str(color):
  return 'WUGRB'[color]

def color_tuple_to_str(t):
  tokens = []
  for (color,count) in enumerate(t):
    if count:
      tokens.append('%s%s' % (color_to_str(color), count))
  return ','.join(tokens)

class Card:
  __slots__ = ['dots', 'points', 'color', 'cost']
  def __init__(self, dots, points, color, cost_dict):
    self.dots = dots
    self.points = points
    self.color = color
    self.cost = cost_dict_to_tuple(cost_dict)

  def __str__(self):
    return '%s%s%s(%s)' % (self.dots, color_to_str(self.color), self.points, color_tuple_to_str(self.cost))

ALL_CARDS = []

def _add_card(dots, points, color, cost_dict):
  ALL_CARDS.append(Card(dots, points, color, cost_dict))

_add_card(1, 0, W, {R:2, B:1})
_add_card(1, 0, U, {W:1, B:2})
_add_card(1, 0, G, {W:2, U:1})
_add_card(1, 0, R, {U:2, G:1})
_add_card(1, 0, B, {G:2, R:1})

_add_card(1, 0, W, {U:3})
_add_card(1, 0, U, {B:3})
_add_card(1, 0, G, {R:3})
_add_card(1, 0, R, {W:3})
_add_card(1, 0, B, {G:3})

_add_card(1, 0, W, {U:1, G:1, R:1, B:1})
_add_card(1, 0, U, {W:1, G:1, R:1, B:1})
_add_card(1, 0, G, {W:1, U:1, R:1, B:1})
_add_card(1, 0, R, {W:1, U:1, G:1, B:1})
_add_card(1, 0, B, {W:1, U:1, G:1, R:1})

_add_card(1, 0, W, {U:1, G:2, R:1, B:1})
_add_card(1, 0, U, {W:1, G:1, R:2, B:1})
_add_card(1, 0, G, {W:1, U:1, R:1, B:2})
_add_card(1, 0, R, {W:2, U:1, G:1, B:1})
_add_card(1, 0, B, {W:1, U:2, G:1, R:1})

_add_card(1, 0, W, {U:2, B:2})
_add_card(1, 0, U, {G:2, B:2})
_add_card(1, 0, G, {U:2, R:2})
_add_card(1, 0, R, {W:2, R:2})
_add_card(1, 0, B, {W:2, G:2})

_add_card(1, 0, W, {W:3, U:1, B:1})
_add_card(1, 0, U, {U:1, G:3, R:1})
_add_card(1, 0, G, {W:1, U:3, G:1})
_add_card(1, 0, R, {W:1, R:1, B:3})
_add_card(1, 0, B, {G:1, R:3, B:1})

_add_card(1, 0, W, {U:2, G:2, B:1})
_add_card(1, 0, U, {W:1, G:2, R:2})
_add_card(1, 0, G, {U:1, R:2, B:2})
_add_card(1, 0, R, {W:2, G:1, B:2})
_add_card(1, 0, B, {W:2, U:2, R:1})

_add_card(1, 1, W, {G:4})
_add_card(1, 1, U, {R:4})
_add_card(1, 1, G, {B:4})
_add_card(1, 1, R, {W:4})
_add_card(1, 1, B, {U:4})

_add_card(2, 1, W, {W:2, U:3, R:3})
_add_card(2, 1, U, {U:2, G:3, B:3})
_add_card(2, 1, G, {W:3, G:2, R:3})
_add_card(2, 1, R, {U:3, R:2, B:3})
_add_card(2, 1, B, {W:3, G:3, B:2})

_add_card(2, 1, W, {G:3, R:2, B:2})
_add_card(2, 1, U, {U:2, G:2, R:3})
_add_card(2, 1, G, {W:2, U:3, B:2})
_add_card(2, 1, R, {W:2, R:2, B:3})
_add_card(2, 1, B, {W:3, U:2, G:2})

_add_card(2, 2, W, {G:1, R:4, B:2})
_add_card(2, 2, U, {W:2, R:1, B:4})
_add_card(2, 2, G, {W:4, U:2, B:1})
_add_card(2, 2, R, {W:1, U:4, G:2})
_add_card(2, 2, B, {U:1, G:4, R:2})

_add_card(2, 2, W, {R:5, B:3})
_add_card(2, 2, U, {W:5, U:3})
_add_card(2, 2, G, {U:5, G:3})
_add_card(2, 2, R, {W:3, B:5})
_add_card(2, 2, B, {G:5, R:3})

_add_card(2, 2, W, {R:5})
_add_card(2, 2, U, {U:5})
_add_card(2, 2, G, {G:5})
_add_card(2, 2, R, {B:5})
_add_card(2, 2, B, {W:5})

_add_card(2, 3, W, {W:6})
_add_card(2, 3, U, {U:6})
_add_card(2, 3, G, {G:6})
_add_card(2, 3, R, {R:6})
_add_card(2, 3, B, {B:6})

_add_card(3, 3, W, {U:3, G:3, R:5, B:3})
_add_card(3, 3, U, {W:3, G:3, R:3, B:5})
_add_card(3, 3, G, {W:5, U:3, R:3, B:3})
_add_card(3, 3, R, {W:3, U:5, G:3, B:3})
_add_card(3, 3, B, {W:3, U:3, G:5, R:3})

_add_card(3, 4, W, {W:3, R:3, B:6})
_add_card(3, 4, U, {W:6, U:3, B:3})
_add_card(3, 4, G, {W:3, U:6, G:3})
_add_card(3, 4, R, {U:3, G:6, R:3})
_add_card(3, 4, B, {G:3, R:6, B:3})

_add_card(3, 5, W, {W:3, B:7})
_add_card(3, 5, U, {W:7, U:3})
_add_card(3, 5, G, {U:7, G:3})
_add_card(3, 5, R, {G:7, R:3})
_add_card(3, 5, B, {R:7, B:3})

_add_card(3, 4, W, {B:7})
_add_card(3, 4, U, {W:7})
_add_card(3, 4, G, {U:7})
_add_card(3, 4, R, {G:7})
_add_card(3, 4, B, {R:7})

def _validate_symmetry(block):
  assert len(set([card.dots for card in block])) == 1
  assert len(set([card.points for card in block])) == 1
  assert set([card.color for card in block]) == set([B,U,G,R,W])
  assert len(set([tuple(sorted(card.cost)) for card in block])) == 1

  total_costs = [0,0,0,0,0] 
  for card in block:
    for (k,v) in enumerate(card.cost):
      total_costs[k] += v

  assert len(set(total_costs)) == 1

def _validate_cards():
  assert len(ALL_CARDS) % 5 == 0
  start = 0
  while True:
    block = ALL_CARDS[start:start+5]
    if not block: break
    try:
      _validate_symmetry(block)
    except:
      print 'Validation failed for:'
      for card in block:
        print str(card)

      traceback.print_exc()
      sys.exit(1)

    start += 5

_validate_cards()

