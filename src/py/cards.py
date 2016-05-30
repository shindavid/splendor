
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
ALL_CARDS.append(Card(1, 0, G, {W:2, U:1}))
