import sys, os
import constants as c
import functions as f
import numpy as np
import keras.models

MODEL_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models')
MODEL_CACHE = {}

def distinquish_model(username):
  return os.path.join(MODEL_DIR, '{}-distinguish.h5'.format(username))

def load_distinquish_model(username):
  if username not in MODEL_CACHE:
    MODEL_CACHE[username] = keras.models.load_model(distinquish_model(username))
  return MODEL_CACHE[username]

def predict_mimic(username, word):
  model = keras.models.load_model('models/' + username + '-mimic.h5')
  return model.predict(f.wordmatrix_to_input(c.matrix_dict[word])).flatten().tolist()

def predict_distinguish(username, word, timings, press_length):
  if not os.path.exists(distinquish_model(username)):
    return np.array([0., 1.])
  data = f.xyz_to_distinguish_data(word, timings, press_length)
  return load_distinquish_model(username).predict(data).flatten()

def main(args):
  if args[0] == 'mimic':
    print predict_mimic(args[1], args[2])
  if args[0] == 'distinguish':
    print predict_distinguish(args[1], args[2], args[3], args[4])

if __name__ == '__main__':
  main(sys.argv[1:])
