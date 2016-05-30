
B = 1
U = 2
G = 3
R = 4
W = 5

def cost_dict_to_tuple(cost_dict):
  b = cost_dict.get(B, 0)
  u = cost_dict.get(U, 0)
  g = cost_dict.get(G, 0)
  r = cost_dict.get(R, 0)
  w = cost_dict.get(W, 0)
  return (b,u,g,r,w)

class Card:
  __slots__ = ['dots', 'points', 'color', 'cost']
  def __init__(self, dots, points, color, cost_dict):
    self.dots = dots
    self.points = points
    self.color = color
    self.cost = cost_dict_to_tuple(cost_dict)

ALL_CARDS = []

def _add(dots, points, color, cost_dict):
  ALL_CARDS.append(Card(dots, points, color, cost_dict))

_add(1, 0, B, {G:2, R:1})
_add(1, 0, U, {W:1, B:2})
_add(1, 0, G, {W:2, U:1})
_add(1, 0, R, {U:2, G:1})
_add(1, 0, W, {R:2, B:1})

_add(1, 0, B, {G:3})
_add(1, 0, U, {B:3})
_add(1, 0, G, {R:3})
_add(1, 0, R, {W:3})
_add(1, 0, W, {U:3})

_add(1, 0, B, {U:1, G:1, R:1, W:1})
_add(1, 0, U, {B:1, G:1, R:1, W:1})
_add(1, 0, G, {B:1, U:1, R:1, W:1})
_add(1, 0, R, {B:1, U:1, R:1, W:1})
_add(1, 0, W, {B:1, U:1, G:1, R:1})

_add(1, 0, B, {U:2, G:1, R:1, W:1})
_add(1, 0, U, {B:1, G:1, R:2, W:1})
_add(1, 0, G, {B:2, U:1, R:1, W:1})
_add(1, 0, R, {B:1, U:1, R:1, W:2})
_add(1, 0, W, {B:1, U:1, G:2, R:1})

_add(1, 0, B, {G:2, W:2})
_add(1, 0, U, {G:2, B:2})
_add(1, 0, G, {U:2, R:2})
_add(1, 0, R, {W:2, R:2})
_add(1, 0, W, {U:2, B:2})

_add(1, 0, B, {G:1, R:3, B:1})
_add(1, 0, U, {U:1, G:3, R:1})
_add(1, 0, G, {W:1, U:3, G:1})
_add(1, 0, R, {W:1, R:1, B:3})
_add(1, 0, W, {W:3, U:1, B:1})

_add(1, 0, B, {W:2, U:2, R:1})
_add(1, 0, U, {W:1, G:2, R:2})
_add(1, 0, G, {U:1, R:2, B:2})
_add(1, 0, R, {W:2, G:1, B:2})
_add(1, 0, W, {U:2, G:2, B:1})

_add(1, 1, B, {U:4})
_add(1, 1, U, {R:4})
_add(1, 1, G, {G:4})
_add(1, 1, R, {W:4})
_add(1, 1, W, {G:4})

_add(2, 1, B, {W:3, G:3, B:2})
_add(2, 1, U, {U:2, G:3, B:3})
_add(2, 1, G, {W:3, G:2, R:3})
_add(2, 1, R, {U:3, R:2, B:3})
_add(2, 1, W, {W:2, U:3, R:3})

_add(2, 1, B, {W:3, U:2, G:2})
_add(2, 1, U, {U:2, G:2, R:3})
_add(2, 1, G, {W:2, U:3, B:2})
_add(2, 1, R, {W:2, R:2, B:3})
_add(2, 1, W, {G:3, R:2, B:2})

_add(2, 2, B, {U:1, G:4, R:2})
_add(2, 2, U, {W:2, R:1, B:4})
_add(2, 2, G, {W:4, U:2, B:1})
_add(2, 2, R, {W:1, U:4, G:2})
_add(2, 2, W, {G:1, R:4, B:2})

_add(2, 2, B, {G:5, R:3})
_add(2, 2, U, {W:5, U:3})
_add(2, 2, G, {U:5, G:3})
_add(2, 2, R, {W:3, B:5})
_add(2, 2, W, {R:5, B:3})

_add(2, 2, B, {W:5})
_add(2, 2, U, {U:5})
_add(2, 2, G, {G:5})
_add(2, 2, R, {B:5})
_add(2, 2, W, {R:5})

_add(2, 3, B, {B:6})
_add(2, 3, U, {U:6})
_add(2, 3, G, {G:6})
_add(2, 3, R, {R:6})
_add(2, 3, W, {W:6})

_add(3, 3, B, {W:3, U:3, G:5, R:3})
_add(3, 3, U, {W:3, G:3, R:3, B:5})
_add(3, 3, G, {W:5, U:3, R:3, B:3})
_add(3, 3, R, {W:3, U:5, G:3, B:3})
_add(3, 3, W, {U:3, G:3, R:5, B:3})

_add(3, 4, B, {G:3, R:6, B:3})
_add(3, 4, U, {W:6, U:3, B:3})
_add(3, 4, G, {W:3, U:6, G:3})
_add(3, 4, R, {U:3, G:6, R:3})
_add(3, 4, W, {W:3, R:3, B:6})

_add(3, 5, B, {R:7, B:3})
_add(3, 5, U, {W:7, U:3})
_add(3, 5, G, {U:7, G:3})
_add(3, 5, R, {G:7, R:3})
_add(3, 5, W, {W:3, B:7})

_add(3, 4, B, {R:7})
_add(3, 4, U, {W:7})
_add(3, 4, G, {U:7})
_add(3, 4, R, {G:7})
_add(3, 4, W, {B:7})

