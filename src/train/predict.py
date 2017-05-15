import sys, os
import constants as c
import functions as f
import numpy as np
from keras.models import load_model

MODEL_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models')

def predict_mimic(username, word):
  model = load_model('models/' + username + '-mimic.h5')
  return model.predict(f.wordmatrix_to_input(c.matrix_dict[word])).flatten().tolist()

def predict_distinguish(username, word, timings, press_length):
  model = os.path.join(MODEL_DIR, '{}-distinguish.h5'.format(username))
  if not os.path.exists(model):
    return np.array([0., 1.])
  data = f.xyz_to_distinguish_data(word, timings, press_length)
  model = load_model(model)
  return model.predict(data).flatten()

def main(args):
  if args[0] == 'mimic':
    print predict_mimic(args[1], args[2])
  if args[0] == 'distinguish':
    print predict_distinguish(args[1], args[2], args[3], args[4])

if __name__ == '__main__':
  main(sys.argv[1:])
