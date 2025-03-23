import tensorflow as tf
from tensorflow.keras import layers, Model

inputs = tf.keras.Input(shape=(7,))
x = layers.Dense(128, activation='relu')(inputs)
x = layers.Dense(64, activation='relu')(x)

# Frequency prediction
freq_out = layers.Dense(1, name="frequency")(x)

# Force prediction
force_out = layers.Dense(1, name="force")(x)

# Asymmetry classification
asym_out = layers.Dense(1, activation="sigmoid", name="asymmetry")(x)

model = Model(inputs=inputs, outputs=[freq_out, force_out, asym_out])
model.compile(
    loss={"frequency": "mse", "force": "mse", "asymmetry": "binary_crossentropy"},
    optimizer="adam",
    metrics={"frequency": "mae", "force": "mae", "asymmetry": "accuracy"}
)
