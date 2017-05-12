import os
import sys
import glob
import constants as c
import functions as f
import numpy as np

from keras.models import Sequential, Model
from keras.layers import SimpleRNN
from keras.layers import Activation, Dropout, Flatten, Dense, Concatenate, Masking, LeakyReLU
from keras.layers import Input
from keras.optimizers import Nadam, SGD
from keras.callbacks import Callback
from keras import backend as K


def train_mimic(username):
  print "Creating Model..."
  forward_input = Input(shape = (c.WINDOW_SIZE, c.ALPHABET_SIZE))
  forward_mask = Masking()(forward_input)
  forward_rnn = SimpleRNN(c.VECTOR_SIZE)(forward_mask)
  forward_rnn = LeakyReLU()(forward_rnn)
  reverse_input = Input(shape = (c.WINDOW_SIZE, c.ALPHABET_SIZE))
  reverse_mask = Masking()(reverse_input)
  reverse_rnn = SimpleRNN(c.VECTOR_SIZE)(reverse_mask)
  reverse_rnn = LeakyReLU()(reverse_rnn)
  x = Concatenate()([forward_rnn, reverse_rnn])
  x = Dropout(0.5)(x)
  output = Dense(50)(x)
  output = LeakyReLU()(output)
  output = Dense(1)(output)

  model = Model(inputs=[forward_input, reverse_input], outputs=output)

  print "Compiling Model..."
  # optimizer = SGD(lr=0.05, momentum=0.0, decay=5e-4, nesterov=False)
  # optimizer = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
  model.compile(loss='mean_absolute_error', optimizer='sgd')

  input_files = glob.glob('Data/' + username + '/*.npz')
  out = f.filelist_to_mimic_data(input_files)
  model.fit(x=out[:2], y=out[2], epochs=c.EPOCHS)

  print "Saving result..."
  model.save('models/' + username + '-mimic.h5')

def train_distinguish(username):
  print "Creating Model..."
  rnn_input = Input(shape = (c.MAX_WORD_SIZE, c.ALPHABET_SIZE + 1))
  rnn_mask = Masking()(rnn_input)
  rnn = SimpleRNN(c.VECTOR_SIZE)(rnn_mask)
  rnn = LeakyReLU()(rnn)
  rnn = Dropout(0.5)(rnn)
  output = Dense(50)(rnn)
  output = LeakyReLU()(output)
  output = Dense(2, activation='softmax')(output)

  model = Model(inputs=rnn_input, outputs=output)

  print "Compiling Model..."
  # optimizer = SGD(lr=0.05, momentum=0.0, decay=5e-4, nesterov=False)
  # optimizer = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
  model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

  names = next(os.walk('./Data/'))[1]
  x_data = np.zeros((0, c.MAX_WORD_SIZE, c.ALPHABET_SIZE + 1))
  y_data = np.zeros((0, 2))
  for name in names:
    input_files = glob.glob('Data/' + name + '/*.npz')
    x = f.filelist_to_distinguish_data(input_files)
    if name == username:
      y = np.repeat(np.array([[1, 0]]), len(x), axis=0)
    else:
      y = np.repeat(np.array([[0, 1]]), len(x), axis=0)
    x_data = np.append(x_data, x, axis = 0)
    y_data = np.append(y_data, y, axis = 0)
  model.fit(x=x_data, y=y_data, epochs=c.EPOCHS)

  print "Saving result..."
  model.save('models/' + username + '-distinguish.h5')

def main(mode, username):
  if mode == 'mimic':
    train_mimic(username)
  if mode == 'distinguish':
    train_distinguish(username)

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])
