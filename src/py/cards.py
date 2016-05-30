import sys
import traceback

W = 0
U = 1
G = 2
R = 3
B = 4
J = 5

def color_dict_to_tuple(color_dict):
  w = color_dict.get(W, 0)
  u = color_dict.get(U, 0)
  g = color_dict.get(G, 0)
  r = color_dict.get(R, 0)
  b = color_dict.get(B, 0)
  return (w, u, g, r, b)

def color_to_str(color):
  return 'WUGRBJ'[color]

def color_tuple_to_str(t):
  tokens = []
  for (color,count) in enumerate(t):
    if count:
      tokens.append('%s%s' % (color_to_str(color), count))
  return ','.join(tokens)

class Card:
  next_id = -1
  MASTER_LIST = []
  __slots__ = ['ID', 'levels', 'points', 'color', 'cost']

  @staticmethod
  def get_next_id():
    Card.next_id += 1
    return Card.next_id

  @staticmethod
  def _add_card(levels, points, color, color_dict):
    Card.MASTER_LIST.append(Card(levels, points, color, color_dict))

  def __init__(self, levels, points, color, color_dict):
    self.ID = Card.get_next_id()
    self.levels = levels
    self.points = points
    self.color = color
    self.cost = color_dict_to_tuple(color_dict)

    # for convenience
    self._color_tuple = tuple([(1 if color==i else 0) for i in range(5)])

  def color_tuple(self):
    return self._color_tuple

  def __str__(self):
    return '%s:%s%s%s(%s)' % (self.ID, self.levels, color_to_str(self.color), self.points, color_tuple_to_str(self.cost))

Card._add_card(1, 0, W, {R:2, B:1})
Card._add_card(1, 0, U, {W:1, B:2})
Card._add_card(1, 0, G, {W:2, U:1})
Card._add_card(1, 0, R, {U:2, G:1})
Card._add_card(1, 0, B, {G:2, R:1})

Card._add_card(1, 0, W, {U:3})
Card._add_card(1, 0, U, {B:3})
Card._add_card(1, 0, G, {R:3})
Card._add_card(1, 0, R, {W:3})
Card._add_card(1, 0, B, {G:3})

Card._add_card(1, 0, W, {U:1, G:1, R:1, B:1})
Card._add_card(1, 0, U, {W:1, G:1, R:1, B:1})
Card._add_card(1, 0, G, {W:1, U:1, R:1, B:1})
Card._add_card(1, 0, R, {W:1, U:1, G:1, B:1})
Card._add_card(1, 0, B, {W:1, U:1, G:1, R:1})

Card._add_card(1, 0, W, {U:1, G:2, R:1, B:1})
Card._add_card(1, 0, U, {W:1, G:1, R:2, B:1})
Card._add_card(1, 0, G, {W:1, U:1, R:1, B:2})
Card._add_card(1, 0, R, {W:2, U:1, G:1, B:1})
Card._add_card(1, 0, B, {W:1, U:2, G:1, R:1})

Card._add_card(1, 0, W, {U:2, B:2})
Card._add_card(1, 0, U, {G:2, B:2})
Card._add_card(1, 0, G, {U:2, R:2})
Card._add_card(1, 0, R, {W:2, R:2})
Card._add_card(1, 0, B, {W:2, G:2})

Card._add_card(1, 0, W, {W:3, U:1, B:1})
Card._add_card(1, 0, U, {U:1, G:3, R:1})
Card._add_card(1, 0, G, {W:1, U:3, G:1})
Card._add_card(1, 0, R, {W:1, R:1, B:3})
Card._add_card(1, 0, B, {G:1, R:3, B:1})

Card._add_card(1, 0, W, {U:2, G:2, B:1})
Card._add_card(1, 0, U, {W:1, G:2, R:2})
Card._add_card(1, 0, G, {U:1, R:2, B:2})
Card._add_card(1, 0, R, {W:2, G:1, B:2})
Card._add_card(1, 0, B, {W:2, U:2, R:1})

Card._add_card(1, 1, W, {G:4})
Card._add_card(1, 1, U, {R:4})
Card._add_card(1, 1, G, {B:4})
Card._add_card(1, 1, R, {W:4})
Card._add_card(1, 1, B, {U:4})

Card._add_card(2, 1, W, {W:2, U:3, R:3})
Card._add_card(2, 1, U, {U:2, G:3, B:3})
Card._add_card(2, 1, G, {W:3, G:2, R:3})
Card._add_card(2, 1, R, {U:3, R:2, B:3})
Card._add_card(2, 1, B, {W:3, G:3, B:2})

Card._add_card(2, 1, W, {G:3, R:2, B:2})
Card._add_card(2, 1, U, {U:2, G:2, R:3})
Card._add_card(2, 1, G, {W:2, U:3, B:2})
Card._add_card(2, 1, R, {W:2, R:2, B:3})
Card._add_card(2, 1, B, {W:3, U:2, G:2})

Card._add_card(2, 2, W, {G:1, R:4, B:2})
Card._add_card(2, 2, U, {W:2, R:1, B:4})
Card._add_card(2, 2, G, {W:4, U:2, B:1})
Card._add_card(2, 2, R, {W:1, U:4, G:2})
Card._add_card(2, 2, B, {U:1, G:4, R:2})

Card._add_card(2, 2, W, {R:5, B:3})
Card._add_card(2, 2, U, {W:5, U:3})
Card._add_card(2, 2, G, {U:5, G:3})
Card._add_card(2, 2, R, {W:3, B:5})
Card._add_card(2, 2, B, {G:5, R:3})

Card._add_card(2, 2, W, {R:5})
Card._add_card(2, 2, U, {U:5})
Card._add_card(2, 2, G, {G:5})
Card._add_card(2, 2, R, {B:5})
Card._add_card(2, 2, B, {W:5})

Card._add_card(2, 3, W, {W:6})
Card._add_card(2, 3, U, {U:6})
Card._add_card(2, 3, G, {G:6})
Card._add_card(2, 3, R, {R:6})
Card._add_card(2, 3, B, {B:6})

Card._add_card(3, 3, W, {U:3, G:3, R:5, B:3})
Card._add_card(3, 3, U, {W:3, G:3, R:3, B:5})
Card._add_card(3, 3, G, {W:5, U:3, R:3, B:3})
Card._add_card(3, 3, R, {W:3, U:5, G:3, B:3})
Card._add_card(3, 3, B, {W:3, U:3, G:5, R:3})

Card._add_card(3, 4, W, {W:3, R:3, B:6})
Card._add_card(3, 4, U, {W:6, U:3, B:3})
Card._add_card(3, 4, G, {W:3, U:6, G:3})
Card._add_card(3, 4, R, {U:3, G:6, R:3})
Card._add_card(3, 4, B, {G:3, R:6, B:3})

Card._add_card(3, 5, W, {W:3, B:7})
Card._add_card(3, 5, U, {W:7, U:3})
Card._add_card(3, 5, G, {U:7, G:3})
Card._add_card(3, 5, R, {G:7, R:3})
Card._add_card(3, 5, B, {R:7, B:3})

Card._add_card(3, 4, W, {B:7})
Card._add_card(3, 4, U, {W:7})
Card._add_card(3, 4, G, {U:7})
Card._add_card(3, 4, R, {G:7})
Card._add_card(3, 4, B, {R:7})

def _validate_symmetry(block):
  assert len(set([card.levels for card in block])) == 1
  assert len(set([card.points for card in block])) == 1
  assert set([card.color for card in block]) == set([B,U,G,R,W])
  assert len(set([tuple(sorted(card.cost)) for card in block])) == 1

  total_costs = [0,0,0,0,0] 
  for card in block:
    for (k,v) in enumerate(card.cost):
      total_costs[k] += v

  assert len(set(total_costs)) == 1

def _validate_cards():
  assert len(Card.MASTER_LIST) % 5 == 0
  start = 0
  while True:
    block = Card.MASTER_LIST[start:start+5]
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

class Noble:
  next_id = -1
  MASTER_LIST = []
  __slots__ = ['ID', 'points', 'requirement']
  
  @staticmethod
  def get_next_id():
    Noble.next_id += 1
    return Noble.next_id

  @staticmethod
  def _add_noble(points, color_dict):
    Noble.MASTER_LIST.append(Noble(points, color_dict))

  def __init__(self, points, requirement):
    self.ID = Noble.get_next_id()
    self.points = points
    self.requirement = color_dict_to_tuple(requirement)

  def __str__(self):
    return '%s(%s)' % (self.points, color_tuple_to_str(self.requirement))

Noble._add_noble(3, {G:3, U:3, W:3})
Noble._add_noble(3, {G:3, U:3, R:3})
Noble._add_noble(3, {B:3, R:3, W:3})
Noble._add_noble(3, {B:3, R:3, G:3})
Noble._add_noble(3, {B:3, U:3, W:3})

Noble._add_noble(3, {B:4, W:4})
Noble._add_noble(3, {U:4, W:4})
Noble._add_noble(3, {R:4, G:4})
Noble._add_noble(3, {B:4, R:4})
Noble._add_noble(3, {U:4, G:4})

