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
  forward_rnn = SimpleRNN(c.S_VECTOR_SIZE)(forward_mask)
  forward_rnn = LeakyReLU()(forward_rnn)
  reverse_input = Input(shape = (c.WINDOW_SIZE, c.ALPHABET_SIZE))
  reverse_mask = Masking()(reverse_input)
  reverse_rnn = SimpleRNN(c.S_VECTOR_SIZE)(reverse_mask)
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

  z = np.c_[out[0].reshape(len(out[0]), -1), out[1].reshape(len(out[1]), -1), out[2].reshape(len(out[2]), -1)]
  np.random.shuffle(z)
  x1 = z[:, :out[0].size//len(out[0])].reshape(out[0].shape)
  x2 = z[:, out[0].size//len(out[0]):out[0].size//len(out[0]) + out[1].size//len(out[1])].reshape(out[1].shape)
  y = z[:, out[0].size//len(out[0]) + out[1].size//len(out[1]):].reshape(out[2].shape)
  model.fit(x=[x1, x2], y=y, epochs=c.EPOCHS, validation_split=0.1)

  print "Saving result..."
  model.save('models/' + username + '-mimic.h5')

def train_distinguish(username):
  print "Creating Model..."
  rnn_input = Input(shape = (c.MAX_WORD_SIZE, c.ALPHABET_SIZE + 2))
  rnn_mask = Masking()(rnn_input)
  rnn = SimpleRNN(c.D_VECTOR_SIZE, activation='relu')(rnn_mask)
  # rnn = LeakyReLU()(rnn)
  output = Dense(50, activation='relu')(rnn)
  # output = LeakyReLU()(output)
  output = Dropout(0.5)(output)
  output = Dense(50, activation='relu')(rnn)
  # output = LeakyReLU()(output)
  output = Dense(20, activation='relu')(rnn)
  # output = LeakyReLU()(output)
  output = Dense(2, activation='softmax')(output)

  model = Model(inputs=rnn_input, outputs=output)

  print "Compiling Model..."
  # optimizer = SGD(lr=0.05, momentum=0.0, decay=5e-4, nesterov=False)
  # optimizer = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
  model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

  names = next(os.walk('./Data/'))[1]
  x = np.zeros((0, c.MAX_WORD_SIZE, c.ALPHABET_SIZE + 2))
  y = np.zeros((0, 2))
  for name in names:
    input_files = glob.glob('Data/' + name + '/*.npz')
    x_data = f.filelist_to_distinguish_data(input_files)
    if name == username:
      y_data = np.repeat(np.array([[1, 0]]), len(x_data), axis=0)
    else:
      y_data = np.repeat(np.array([[0, 1]]), len(x_data), axis=0)
    x = np.append(x, x_data, axis = 0)
    y = np.append(y, y_data, axis = 0)
  print np.mean(y, axis = 0)
  z = np.c_[x.reshape(len(x), -1), y.reshape(len(y), -1)]
  np.random.shuffle(z)
  x2 = z[:, :x.size//len(x)].reshape(x.shape)
  y2 = z[:, x.size//len(x):].reshape(y.shape)
  model.fit(x=x2, y=y2, epochs=c.EPOCHS, validation_split=0.1)

  print "Saving result..."
  model.save('models/' + username + '-distinguish.h5')

def main(mode, username):
  if mode == 'mimic':
    train_mimic(username)
  if mode == 'distinguish':
    train_distinguish(username)

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])
