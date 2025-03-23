# File: ml_training_plan.py
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model

# Load dataset
npz = np.load("asymmetric_mode_dataset.npz")
X = npz["X"]
y_force = npz["y_force"]
y_freq = npz["y_freq"]
y_asym = npz["y_asym"]

# Model architecture
inputs = tf.keras.Input(shape=(7,), name="features")
x = layers.Dense(128, activation='relu')(inputs)
x = layers.Dense(64, activation='relu')(x)

freq_out = layers.Dense(1, name="frequency")(x)
force_out = layers.Dense(1, name="force")(x)
asym_out = layers.Dense(1, activation="sigmoid", name="asymmetry")(x)

model = Model(inputs=inputs, outputs=[freq_out, force_out, asym_out])
model.compile(
    optimizer="adam",
    loss={
        "frequency": "mse",
        "force": "mse",
        "asymmetry": "binary_crossentropy"
    },
    metrics={
        "frequency": "mae",
        "force": "mae",
        "asymmetry": "accuracy"
    }
)

# Train model
model.fit(
    X, {"frequency": y_freq, "force": y_force, "asymmetry": y_asym},
    epochs=50, batch_size=32, validation_split=0.2
)

# Save trained model
model.save("asymmetric_mode_predictor.h5")
