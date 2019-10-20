from flask import Blueprint, render_template, request
import numpy as np
import tensorflow as tf
import json

mnist_bluprint = Blueprint('mnist', __name__)


# Tensorflow setup
input_size = 784
output_size = 10
hidden_layer_size = 400

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(hidden_layer_size, activation='relu'),
    tf.keras.layers.Dense(hidden_layer_size, activation='tanh'),
    tf.keras.layers.Dense(output_size, activation='softmax'),
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.load_weights('mnist_checkpoints/my_checkpoint')
# End Tensorflow setup


@mnist_bluprint.route('/')
def index():
    return render_template('mnist/index.html')


@mnist_bluprint.route('/getnumber')
def get_number():
    input_array = []
    for a in request.args.get("x"):
        input_array.append(float(a)/9.0)
    input_array = tf.reshape(input_array, [28, 28, 1])
    # (data, shape)
    # inputData = tf.tensor2d([input_array], [1, len(input_array)])
    result = model.predict([[input_array]])
    r = np.where(result == np.amax(result))
    cords = list(zip(r[0], r[1]))
    # const winner = irisClasses[result.argMax().dataSync()[0]];
    # console.log(winner);
    output_array = []
    for a in result[0]:
        output_array.append(a)
    return f'{"{"}"number": "{cords[0][1]}", "probability": {output_array}{"}"}'
