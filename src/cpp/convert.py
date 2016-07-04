filename = '../py/cards.py'
f = open(filename)

color_map = {
    'W' : 'eWhite',
    'U' : 'eBlue',
    'G' : 'eGreen',
    'R' : 'eRed',
    'B' : 'eBlack',
    'J' : 'eGold',
    }

color_index_map = {
    'W' : 0,
    'U' : 1,
    'G' : 2,
    'R' : 3,
    'B' : 4
    }

def convert(cost_str):
  cost_array = [0,0,0,0,0]
  tokens = [x.strip() for x in cost_str.split(',')]
  for token in tokens:
    subtokens = token.split(':')
    color_index = color_index_map[subtokens[0]]
    count = int(subtokens[1])
    cost_array[color_index] = count

  return ', '.join([str(x) for x in cost_array])

ID = 0
first = True
for line in f:
  if line.count('_add_card'):
    if first:
      first = False
      continue
    lp = line.find('(')
    rp = line.find(')')
    lb = line.find('{')
    rb = line.find('}')
    cost_str = line[lb+1:rb]
    tokens = line[lp+1:rp].split(',')
    level = int(tokens[0].strip()) - 1
    points = int(tokens[1].strip())
    color = color_map[tokens[2].strip()]
    
    print '    {%2d, {%s}, %s, %s, %s},' % (ID, convert(cost_str), points, level, color)
    ID += 1

ID = 0
f = open(filename)
first = True
for line in f:
  if line.count('_add_noble'):
    if first:
      first = False
      continue
    lp = line.find('(')
    rp = line.find(')')
    lb = line.find('{')
    rb = line.find('}')
    cost_str = line[lb+1:rb]
    
    print '    {%s, 3, {%s}},' % (ID, convert(cost_str))
    ID += 1
