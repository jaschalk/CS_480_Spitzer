# sample code brought in from https://www.tensorflow.org/tutorials/quickstart/beginner

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

mnist = tf.keras.datasets.mnist
tf.keras.backend.set_floatx('float64')
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

#Create the model with the properties provided by the arguments:

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)), #the input layer is a vectorized 28x28 matrix
  tf.keras.layers.Dense(16, activation='relu'), #the next layer is 128 elements, Densely connected to the previous layer, and using relu activation
  tf.keras.layers.Dropout(0.025), #% chance of each neuron being 0, this is to prevent overfitting
  tf.keras.layers.Dense(16, activation='relu'),
  tf.keras.layers.Dropout(0.025),
  tf.keras.layers.Dense(10) #the final layer is 10 elements and densely connected
])

main_input = tf.keras.Input(shape=(28,28))

inputA = tf.keras.Input(shape=(28,28))
testA = tf.keras.layers.Flatten()(inputA)
x = tf.keras.layers.Dense(32, activation="selu")(testA)
x = tf.keras.layers.Dropout(0.1)(x)
x = tf.keras.layers.Dense(16, activation="selu")(x)
x = tf.keras.Model(inputs=inputA, outputs=x)

inputB = tf.keras.Input(shape=(28,28))
testB = tf.keras.layers.Flatten()(inputB)
y = tf.keras.layers.GaussianNoise(stddev=0.5)(testB)
y = tf.keras.layers.Dense(16, activation="selu")(y)
y = tf.keras.layers.Dense(16, activation="selu")(y)
y = tf.keras.Model(inputs=inputB, outputs=y)

multi = tf.keras.layers.multiply([x.output, y.output])

z = tf.keras.layers.Dense(16, activation="selu")(multi)
z = tf.keras.layers.Dense(10, activation="selu")(z)

test_model = tf.keras.Model(inputs=[x.input, y.input], outputs=z)

if True:
  model = test_model

  predictions = model([x_train[:1], x_train[:1] ]).numpy()

  tf.nn.softmax(predictions).numpy()

  loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

  loss_fn(y_train[:1], predictions).numpy()

  model.compile(optimizer='adam',
                loss=loss_fn,
                metrics=['accuracy'])

  model.fit([x_train, x_train], y_train, epochs=5)
  model.evaluate([x_test, x_test], y_test, verbose=2)
else:
  predictions = model(x_train[:1]).numpy()

  tf.nn.softmax(predictions).numpy()

  loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

  loss_fn(y_train[:1], predictions).numpy()

  model.compile(optimizer='adam',
                loss=loss_fn,
                metrics=['accuracy'])

  model.fit(x_train, y_train, epochs=5)
  model.evaluate(x_test, y_test, verbose=2)

#probability_model = tf.keras.Sequential([
#  model,
#  tf.keras.layers.Softmax()
#])

#probability_model([x_test[:5], x_test[:5]])