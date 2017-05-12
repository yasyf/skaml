from transform import ONE_HOT_SIZE
import numpy as np

def one_hot_to_ind(x):
  return np.nonzero(x)[0]

def mean_delays(X, Y):
  delays = np.zeros((ONE_HOT_SIZE, ONE_HOT_SIZE))
  for i, word in X:
    for c in characters:
      pass
