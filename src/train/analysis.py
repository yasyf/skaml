import sys
import glob
import numpy as np
import operator

FIRST_CODE = 48
LAST_CODE = 90
ONE_HOT_SIZE = LAST_CODE - FIRST_CODE + 1
TIME_DIFF_THRESHOLD = 300
HOLD_THRESHOLD = 150

type_dict = {}
type_dict['a'] = 1
type_dict['b'] = 4
type_dict['c'] = 3
type_dict['d'] = 3
type_dict['e'] = 3
type_dict['f'] = 4
type_dict['g'] = 4
type_dict['h'] = 5
type_dict['i'] = 6
type_dict['j'] = 5
type_dict['k'] = 6
type_dict['l'] = 7
type_dict['m'] = 6
type_dict['n'] = 5
type_dict['o'] = 7
type_dict['p'] = 8
type_dict['q'] = 1
type_dict['r'] = 4
type_dict['s'] = 2
type_dict['t'] = 4
type_dict['u'] = 5
type_dict['v'] = 4
type_dict['w'] = 2
type_dict['x'] = 2
type_dict['y'] = 5
type_dict['z'] = 1


def idxs_to_str(idxs):
  return ''.join(map(lambda i: chr(i + FIRST_CODE).lower(), idxs))

def idx_to_char(idx):
  return chr(idx + FIRST_CODE).lower()

def one_hot_to_ind(x):
  return np.flatnonzero(x)[0]


def mean_delays(X, Y):
  means = np.zeros((ONE_HOT_SIZE, ONE_HOT_SIZE))
  counts = np.zeros((ONE_HOT_SIZE, ONE_HOT_SIZE))

  for i, word in enumerate(X):
    for j, char in enumerate(word):
      if j == 0:
        continue
      c1 = one_hot_to_ind(word[j - 1])
      c2 = one_hot_to_ind(char)
      means[c1][c2] += Y[i][j - 1]
      counts[c1][c2] += 1

  counts[np.where(counts == 0)] = 1
  means /= counts
  mean = means.ravel()[np.flatnonzero(means)].mean()
  means[np.where(means == 0)] = mean
  return means

def user_mean_delays(username):
  input_files = glob.glob('Data/' + username + '/*.npz')

  means = np.zeros((ONE_HOT_SIZE, ONE_HOT_SIZE))
  counts = np.zeros((ONE_HOT_SIZE, ONE_HOT_SIZE))

  for filename in input_files:
    X = np.load(filename)['X']
    Y = np.load(filename)['Y']
    for i, word in enumerate(X):
      for j, char in enumerate(word):
        if j == 0:
          continue
        c1 = one_hot_to_ind(word[j - 1])
        c2 = one_hot_to_ind(char)
        means[c1][c2] += Y[i][j - 1]
        counts[c1][c2] += 1

  counts[np.where(counts == 0)] = 1
  means /= counts
  mean = means.ravel()[np.flatnonzero(means)].mean()
  # means[np.where(means == 0)] = mean
  return means, counts

def sort_timings(username):
  means, counts = user_mean_delays(username)
  m_dict = {}
  c_dict = {}
  for i in range(ONE_HOT_SIZE):
    for j in range(ONE_HOT_SIZE):
      if counts[i, j] > 0:
        m_dict[(idx_to_char(i), idx_to_char(j))] = means[i, j]
        c_dict[(idx_to_char(i), idx_to_char(j))] = counts[i, j]
  sorted_m = sorted(m_dict.items(), key=operator.itemgetter(1))
  for x in sorted_m:
    if c_dict[x[0]] > 10:
      print x, c_dict[x[0]], type_dict[x[0][0]] == type_dict[x[0][1]]
  return m_dict

def main(args):
  sort_timings(args[0])


if __name__ == '__main__':
  main(sys.argv[1:])