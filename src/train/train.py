import glob
import random
import numpy as np
import constants as c
from StringIO import StringIO

from PIL import Image
from keras.models import Sequential, Model
from keras.layers import SimpleRNN
from keras.layers import Activation, Dropout, Flatten, Dense, Concatenate, Masking
from keras.layers import Input
from keras.optimizers import Nadam, SGD
from keras.callbacks import Callback
from keras import backend as K


# ALL_IMAGES = glob.glob('./Data/CleanGenerated/*.jpeg')

# INPUT_BATCHSIZE = 500

def string_to_matrix(string):
	output = np.empty([len(string), len(c.CHARACTERS)])
	for i in range(len(string)):
		output[i] = np.array([int(string[i] == letter) for letter in c.CHARACTERS])
	output = output[-c.WINDOW_SIZE:]

	return np.concatenate([np.tile(np.zeros(len(c.CHARACTERS)), (c.WINDOW_SIZE - output.shape[0], 1)), output])

def password_to_data(password, times):


# def input_generator():
#     while True:
#         for i in range(0, len(ALL_IMAGES), INPUT_BATCHSIZE):
#             files = ALL_IMAGES[i:i + INPUT_BATCHSIZE]
#             input_x = np.array([np.array(Image.open(filename)) for filename in files])
#             input_y = np.array([identifier_to_onehot(filename[-13:-5]) for filename in files])
#             input_y = np.transpose(input_y, (1, 0, 2))
#             yield input_x, [input_y[0], input_y[1], input_y[2], input_y[3]]

# def validation_generator():
#     while True:
#         identifier = g.getRandomIdentifier()
#         f = StringIO()
#         g.getCaptcha(identifier, noise=True, variation=True).save(f, format = "jpeg", quality = c.JPEG_QUALITY)
#         identifier_string = "".join(map(g.strMapper, identifier))
#         vec = identifier_to_onehot(identifier_string)
#         yield np.array([np.array(Image.open(f))]), [np.array([vec[0]]), np.array([vec[1]]), np.array([vec[2]]), np.array([vec[3]])]

def main():	
    print "Creating Model..."
    forward_input = Input(shape = (c.WINDOW_SIZE, len(c.CHARACTERS)))
    forward_rnn = Masking()(forward_input)
    forward_rnn = SimpleRNN(c.VECTOR_SIZE)(forward_rnn)
    reverse_input = Input(shape = (c.WINDOW_SIZE, len(c.CHARACTERS)))
	reverse_rnn = Masking()(reverse_input)
    reverse_rnn = SimpleRNN(c.VECTOR_SIZE)(reverse_input)
    x = Concatenate()([forward_rnn, reverse_rnn])
    output = Dense(50)(x)
    output = Dense(1)

    model = Model(input=[forward_input, reverse_input], output=output)

    print "Compiling Model..."
    # optimizer = SGD(lr=0.05, momentum=0.0, decay=5e-4, nesterov=False)
    optimizer = SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
    model.compile(loss='categorical_crossentropy',
                optimizer=optimizer,
                metrics=['accuracy'])

    model.fit_generator(
        input_generator(),
        samples_per_epoch=len(ALL_IMAGES),
        nb_epoch=50,
        validation_data=validation_generator(),
        nb_val_samples=1000)

    print "Saving result..."
    model.save('models/my_model.h5')

if __name__ == '__main__':
    main()
