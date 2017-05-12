import numpy as np

FIRST_CODE = 48
LAST_CODE = 90
ONE_HOT_SIZE = LAST_CODE - FIRST_CODE + 1

def encode(chars):
  return [list(one_hot(c)) for c in chars if is_valid_char(c)]

def filter_valid(obj):
  return [[c for c in w['characters'] if is_valid_char(c)] for w in obj['words'] if w['characters']]

def one_hot(char):
  one_hot = np.zeros(ONE_HOT_SIZE)
  one_hot[char['keyCode'] - FIRST_CODE] = 1
  return one_hot

def is_valid_char(char):
  return FIRST_CODE <= char['keyCode'] <= LAST_CODE

def release_time_diff(c1, c2):
  return c2['timeReleased'] - c1['timeReleased']

def transform(obj):
  words = filter_valid(obj)
  X = np.empty(len(words), dtype=np.object)
  Y = np.empty(len(words), dtype=np.object)
  for i, word in enumerate(words):
    chars = [(j, x) for j, x in enumerate(word) if is_valid_char(x)]
    if not chars:
      X[i] = np.empty(0)
      Y[i] = np.empty(0)
      continue
    x = np.empty((len(chars), ONE_HOT_SIZE), dtype=np.float)
    y = np.empty((len(chars) - 1,), dtype=np.float)
    for k, (j, char) in enumerate(chars):
      x[k,:] = one_hot(char)
      if k == 0:
        continue
      y[k-1] = release_time_diff(word[j-1], char)
    X[i] = x
    Y[i] = y
  return X, Y
