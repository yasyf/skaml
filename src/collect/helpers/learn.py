from transform import ONE_HOT_SIZE, transform, str_to_idxs, chars_to_idxs, one_hot_to_ind
import numpy as np
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir, 'train')))
import predict

def evaluate(username, password):
  if not password['characters']:
    return False, 0
  prob = predict.predict_distinguish(username, *transform({'words': [password]}))
  return bool(np.argmax(prob) == 0), round(prob[0], 2)

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

def idxs_delay(obj, idxs):
  X, Y, _ = transform(obj)
  means = mean_delays(X, Y)
  return [round(means[idxs[i]][idx], 2) for i, idx in enumerate(idxs[1:])]

def string_delay(obj, password):
  return idxs_delay(obj, str_to_idxs(password))

def chars_delay(obj, chars):
  return idxs_delay(obj, chars_to_idxs(chars))
