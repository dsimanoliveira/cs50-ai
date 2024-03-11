# Experimentation Process

## First Trial

In my first trial, I trained the model with the same parameters provided in the Lecture Notes, adjusting only the input shape and output units. The result was not good:

```
# Create a convolutional neural network
    model = tf.keras.models.Sequential([

        # Convolutional layer
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Add an output layer with output units for all 43 categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
```

`333/333 - 3s - 9ms/step - accuracy: 0.0525 - loss: 3.4965`

## Changing the number of filters from first Convulutional Layer

I tried changing 32 filters to 128 filters from my first Convulutional Layer. This change led to a high increase in computational time, without improving the accuracy of the model. I stopped running the program before finishing because it didn't lead to any improvements in the model.

## Adding new layer after Pooling

Instead of 32 filters on first Layer. I tried 16 filters, and added a new convolutional layer of 16 just after the Pooling.

This led to a significant improvement in the model's accuracy:

`333/333 - 3s - 8ms/step - accuracy: 0.9517 - loss: 0.2092`

## Trying to decrease dropout to 0.3 instead of 0.5

That too had a positive effect, improving the accuracy of the model just a bit.

`333/333 - 2s - 6ms/step - accuracy: 0.9688 - loss: 0.1695`

## Adding new hidden layer

Instead of one hidden layer of 128 units I tried two hidden layers with 64 each.

That change didn't lead to better accuracy, and also increased the loss. 

`333/333 - 2s - 7ms/step - accuracy: 0.9574 - loss: 0.1905`

# Final Code

```
# Create a convolutional neural network
    model = tf.keras.models.Sequential([

        # Convolutional layer
        tf.keras.layers.Conv2D(
            16, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Convolutional layer
        tf.keras.layers.Conv2D(
            16, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),

        # Add an output layer with output units for all 43 categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
```