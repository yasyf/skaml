import numpy as np
import constants as c

def resize_matrix(matrix):
  output = np.zeros([c.WINDOW_SIZE, c.ALPHABET_SIZE])
  for i in range(min(c.WINDOW_SIZE, matrix.shape[0])):
    output[-(i + 1)] = matrix[-(i + 1)]
  return output

def wordmatrix_to_input(wordmatrix):
  forward_word = np.array(wordmatrix)
  reverse_word = forward_word[::-1]
  word_length = len(forward_word)
  outx_1 = []
  outx_2 = []
  for j in range(len(forward_word) - 1):
    outx_1.append(resize_matrix(forward_word[:j + 2]))
    outx_2.append(resize_matrix(reverse_word[:word_length - j]))
  return [np.array(outx_1), np.array(outx_2)]

def password_to_mimic_data(filename):
  X = np.load(filename)['X']
  Y = np.load(filename)['Y']
  outx_1 = []
  outx_2 = []
  outy = []
  for i in range(len(X)):
    if len(Y[i]) == 0:
      continue
    forward_word = X[i]
    reverse_word = forward_word[::-1]
    word_length = len(X[i])
    timing = Y[i]
    for j in range(len(forward_word) - 1):
      outx_1.append(resize_matrix(forward_word[:j + 2]))
      outx_2.append(resize_matrix(reverse_word[:word_length - j]))
      outy.append(min(timing[j], max(np.random.normal(loc=150,scale=10), 0)))
  return [np.array(outx_1), np.array(outx_2), np.array(outy)]

def filelist_to_mimic_data(filelist):
  x_1 = np.zeros((0, c.WINDOW_SIZE, c.ALPHABET_SIZE))
  x_2 = np.zeros((0, c.WINDOW_SIZE, c.ALPHABET_SIZE))
  y = np.zeros(0)
  for file in filelist:
    out = password_to_mimic_data(file)
    x_1 = np.append(x_1, out[0], axis = 0)
    x_2 = np.append(x_2, out[1], axis = 0)
    y = np.append(y, out[2])
  return [x_1, x_2, y]

def password_to_distinguish_data(filename):
  X = np.load(filename)['X']
  Y = np.load(filename)['Y']
  Z = np.load(filename)['Z']

  output = []
  for i in range(len(X)):
    if len(X[i]) == 0:
      continue
    a = np.zeros((c.MAX_WORD_SIZE, c.ALPHABET_SIZE + 2))
    a[c.MAX_WORD_SIZE - len(X[i])] = np.append(X[i][0], [Z[i][0], 0])
    for j in range(len(Y[i])):
      a[c.MAX_WORD_SIZE - len(X[i]) + j + 1] = np.append(X[i][j + 1], [Z[i][j + 1]*0.01, Y[i][j]*0.01])
    output.append(a)
  return output

def filelist_to_distinguish_data(filelist):
  x = np.zeros((0, c.MAX_WORD_SIZE, c.ALPHABET_SIZE + 2))
  for file in filelist:
    out = password_to_distinguish_data(file)
    x = np.append(x, out, axis = 0)
  return x
