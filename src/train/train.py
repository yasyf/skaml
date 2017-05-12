import sys
import glob
import constants as c
import functions as f

from keras.models import Sequential, Model
from keras.layers import SimpleRNN
from keras.layers import Activation, Dropout, Flatten, Dense, Concatenate, Masking
from keras.layers import Input
from keras.optimizers import Nadam, SGD
from keras.callbacks import Callback
from keras import backend as K


def train_mimic(username):
  print "Creating Model..."
  forward_input = Input(shape = (c.WINDOW_SIZE, c.ALPHABET_SIZE))
  forward_mask = Masking()(forward_input)
  forward_rnn = SimpleRNN(c.VECTOR_SIZE)(forward_mask)
  reverse_input = Input(shape = (c.WINDOW_SIZE, c.ALPHABET_SIZE))
  reverse_mask = Masking()(reverse_input)
  reverse_rnn = SimpleRNN(c.VECTOR_SIZE)(reverse_mask)
  x = Concatenate()([forward_rnn, reverse_rnn])
  output = Dense(50)(x)
  output = Dense(1)(output)

  model = Model(inputs=[forward_input, reverse_input], outputs=output)

  print "Compiling Model..."
  # optimizer = SGD(lr=0.05, momentum=0.0, decay=5e-4, nesterov=False)
  # optimizer = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
  model.compile(loss='mean_absolute_error', optimizer='sgd')

  input_files = glob.glob('Data/' + username + '/*.npz')
  out = f.filelist_to_data(input_files)
  model.fit(x=out[:2], y=out[2], epochs=c.EPOCHS)

  print "Saving result..."
  model.save('models/' + username + '-mimic.h5')

def train_distinguish(username):
  print "Creating Model..."
  forward_input = Input(shape = (c.WINDOW_SIZE, c.ALPHABET_SIZE))
  forward_mask = Masking()(forward_input)
  forward_rnn = SimpleRNN(c.VECTOR_SIZE)(forward_mask)
  reverse_input = Input(shape = (c.WINDOW_SIZE, c.ALPHABET_SIZE))
  reverse_mask = Masking()(reverse_input)
  reverse_rnn = SimpleRNN(c.VECTOR_SIZE)(reverse_mask)
  x = Concatenate()([forward_rnn, reverse_rnn])
  output = Dense(50)(x)
  output = Dense(1)(output)

  model = Model(inputs=[forward_input, reverse_input], outputs=output)

  print "Compiling Model..."
  # optimizer = SGD(lr=0.05, momentum=0.0, decay=5e-4, nesterov=False)
  # optimizer = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
  model.compile(loss='mean_absolute_error', optimizer='sgd')

  input_files = glob.glob('Data/' + username + '/*.npz')
  out = f.filelist_to_data(input_files)
  model.fit(x=out[:2], y=out[2], epochs=c.EPOCHS)

  print "Saving result..."
  model.save('models/' + username + '-mimic.h5')

def main(mode, username):
  if mode == 'mimic':
    train_mimic(username)
  if mode == 'distinguish':
    train_distinguish(username)

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])
