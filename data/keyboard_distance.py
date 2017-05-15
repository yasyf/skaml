import numpy as np

keyboard_cartesian = {'q': {'x':0, 'y':0}, 'w': {'x':1, 'y':0}, 'e': {'x':2, 'y':0}, 'r': {'x':3, 'y':0}, 't': {'x':4, 'y':0}, 'y': {'x':5, 'y':0}, 'u': {'x':6, 'y':0}, 'i': {'x':7, 'y':0}, 'o': {'x':8, 'y':0}, 'p': {'x':9, 'y':0}, 'a': {'x':0, 'y':1},'z': {'x':0, 'y':2},'s': {'x':1, 'y':1},'x': {'x':1, 'y':2},'d': {'x':2, 'y':1},'c': {'x':2, 'y':2}, 'f': {'x':3, 'y':1}, 'b': {'x':4, 'y':2}, 'm': {'x':5, 'y':2}, 'j': {'x':6, 'y':1}, 'g': {'x':4, 'y':1}, 'h': {'x':5, 'y':1}, 'j': {'x':6, 'y':1}, 'k': {'x':7, 'y':1}, 'l': {'x':8, 'y':1}, 'v': {'x':3, 'y':2}, 'n': {'x':5, 'y':2}, }

def keyboard_distance(a, b):
    X = keyboard_cartesian[a]['x'] - keyboard_cartesian[b]['x']
    Y = keyboard_cartesian[a]['y'] - keyboard_cartesian[b]['y']
    return np.sqrt(np.power(X, 2) + np.power(Y, 2))

