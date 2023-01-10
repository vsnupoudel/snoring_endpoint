import tensorflow as tf
import os

model_path = os.path.join( os.path.dirname(__file__)  , 'snoring_or_not')
model = tf.saved_model.load(model_path)
