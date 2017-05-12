import sys
import numpy as np
import constants as c
import functions as f

from keras.models import load_model

def main(username, word):
	model = load_model('models/' + username + '-mimic.h5')
	print model.predict(f.wordmatrix_to_input(c.matrix_dict[word])).flatten().tolist()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])