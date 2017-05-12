import numpy as np
import constants as c

def resize_matrix(matrix):
  output = np.zeros([c.WINDOW_SIZE, c.ALPHABET_SIZE])
  for i in range(min(c.WINDOW_SIZE, matrix.shape[0])):
    output[-(i + 1)] = matrix[-(i + 1)]
  return output

def password_to_data(filename):
  X = np.load(filename)['X']
  Y = np.load(filename)['Y']
  outx_1 = []
  outx_2 = []
  outy = []
  for i in range(len(X)):
    if len(X[i]) == 0:
      continue
    forward_word = X[i]
    reverse_word = X[i][::-1]
    word_length = len(X[i])
    timing = Y[i]
    for j in range(len(forward_word) - 1):
      outx_1.append(resize_matrix(forward_word[:j + 2]))
      outx_2.append(resize_matrix(reverse_word[:word_length - j]))
      outy.append(min(timing[j], max(np.random.normal(loc=150,scale=10), 0)))
  return [np.array(outx_1), np.array(outx_2), np.array(outy)]

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

def filelist_to_data(filelist):
  x_1 = np.zeros((0, c.WINDOW_SIZE, c.ALPHABET_SIZE))
  x_2 = np.zeros((0, c.WINDOW_SIZE, c.ALPHABET_SIZE))
  y = np.zeros(0)
  for file in filelist:
    out = password_to_data(file)
    x_1 = np.append(x_1, out[0], axis = 0)
    x_2 = np.append(x_2, out[1], axis = 0)
    y = np.append(y, out[2])
  return [x_1, x_2, y]