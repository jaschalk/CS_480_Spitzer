# sample code brought in from https://www.tensorflow.org/tutorials/quickstart/beginner

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

mnist = tf.keras.datasets.mnist
tf.keras.backend.set_floatx('float64')
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
print(x_test)

#Create the model with the properties provided by the arguments:

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)), #the input layer is a vectorized 28x28 matrix
  tf.keras.layers.Dense(16, activation='relu'), #the next layer is 128 elements, Densely connected to the previous layer, and using relu activation
  tf.keras.layers.Dropout(0.025), #% chance of each neuron being 0, this is to prevent overfitting
  tf.keras.layers.Dense(16, activation='relu'),
  tf.keras.layers.Dropout(0.025),
  tf.keras.layers.Dense(10) #the final layer is 10 elements and densely connected
])

predictions = model(x_train[:1]).numpy()

tf.nn.softmax(predictions).numpy()

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

loss_fn(y_train[:1], predictions).numpy()

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test,  y_test, verbose=2)

probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

probability_model(x_test[:5])