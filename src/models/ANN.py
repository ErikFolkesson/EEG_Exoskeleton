from tensorflow.keras import layers, models, regularizers
import tensorflow as tf

import matplotlib.pyplot as plt

class ANN:
    def __init__(self,
                 input_shape,
                 output_shape,
                 units,
                 activation_function,
                 learning_rate=0.003):
        """Initialize the ANN model."""

        self.history = None
        net = [layers.Input(shape=input_shape), layers.Flatten()]

        # Hidden layers with L2 regularization
        for num_units in units:
            net.append(
                layers.Dense(
                    num_units,
                    activation=activation_function
                )
            )

        # Output layer with L2 regularization
        net.append(
            layers.Dense(
                output_shape,
                activation='softmax' if output_shape > 1 else 'sigmoid'
            )
        )

        self.model = models.Sequential(net)

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss='binary_crossentropy',
            metrics=['accuracy', 'AUC']
        )

    def fit(self, X, y, epochs=10, batch_size=32, validation_split=0.2):
        """Fit the model to the training data."""
        self.history = self.model.fit(X, y,
                                      epochs=epochs,
                                      batch_size=batch_size,
                                      validation_split=validation_split,
                                      verbose=2)

    def plot_history(self):
        """Plot the training history."""
        if self.history is None:
            raise ValueError("Model has not been trained yet. Call fit() first.")

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(self.history.history['loss'], label='Training Loss')
        plt.plot(self.history.history['val_loss'], label='Validation Loss')
        plt.title('Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['accuracy'], label='Training Accuracy')
        plt.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.tight_layout()
        plt.show()