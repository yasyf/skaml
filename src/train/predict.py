import sys
import numpy as np
import constants as c
import functions as f

from keras.models import load_model



def predict_mimic(username, word):
  model = load_model('models/' + username + '-mimic.h5')
  print model.predict(f.wordmatrix_to_input(c.matrix_dict[word])).flatten().tolist()


def predict_mimic(username, word, timings, press_length):
    a = np.zeros((c.MAX_WORD_SIZE, c.ALPHABET_SIZE + 2))
    a[c.MAX_WORD_SIZE - len(word)] = np.append(word[0], [press_length[0], 0])
    for j in range(len(timings)):
      a[c.MAX_WORD_SIZE - len(word) + j + 1] = np.append(word[j + 1], [press_length[j + 1]*0.01, timings[j]*0.01])

  model = load_model('models/' + username + '-distinguish.h5')
  print model.predict(a)


def main(args):
  if args[0] == 'mimic':
    predict_mimic(args[1], args[2])
  if args[0] == 'distinguish':
    predict_distinguish(args[1], args[2], args[3], args[4])

if __name__ == '__main__':
  main(sys.argv[1:])