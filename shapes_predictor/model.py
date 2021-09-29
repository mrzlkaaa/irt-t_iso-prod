import matplotlib.pyplot as plt
import numpy as np
import os
import re
import PIL
import tensorflow as tf
# from tensorflow import keras

cwd = os.getcwd()
files_list = os.listdir(cwd)
# check for .h5 file
file = [i for i in files_list if re.search(r'\.h5', i)]
if file:
        model = tf.keras.models.load_model(next(iter(file)))
        print(model.summary())
        print('model has loaded')
else:
        print('setting model up.....')
        IMG_SIZE = (180, 180)
        batch_size = 32
        circle = 'circles'

        train_ds = tf.keras.utils.image_dataset_from_directory(
                os.path.join(os.getcwd(), circle),
                labels='inferred',
                batch_size = batch_size,
                image_size = IMG_SIZE,
                seed = 123,
                subset = 'training',
                validation_split = 0.2
        )

        val_ds = tf.keras.utils.image_dataset_from_directory(
                os.path.join(os.getcwd(), circle),
                labels='inferred',
                batch_size = batch_size,
                image_size = IMG_SIZE,
                seed = 123,
                subset = 'validation',
                validation_split = 0.2
        )

        num_class = len(train_ds.class_names)
        print(num_class)
        AUTOTUNE = tf.data.AUTOTUNE

        img,lab = next(iter(train_ds))
        print(img.shape)

        data_augmentation = tf.keras.Sequential([
                tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
                tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
                tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
                tf.keras.layers.experimental.preprocessing.RandomContrast(0.3),

        ])

        # IMG_SIZE = (180, 180)
        # resize_and_rescale = tf.keras.Sequential([
        #   tf.keras.layers.experimental.preprocessing.Resizing(IMG_SIZE[0],IMG_SIZE[1]),
        #
        # ])

        model = tf.keras.Sequential([
                tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
                # resize_and_rescale,
                # data_augmentation,
                tf.keras.layers.Conv2D(16, 6, padding='valid', activation='relu'),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Conv2D(32, 4, strides=(2,2), activation='relu'),
                tf.keras.layers.MaxPool2D(),
                tf.keras.layers.Conv2D(64, 2, activation='relu'),
                tf.keras.layers.MaxPool2D(),
                # tf.keras.layers.Conv2D(256, 2, activation='relu'),
                # tf.keras.layers.MaxPool2D(),
                # tf.keras.layers.Conv2D(256, 2, activation='relu'),
                # tf.keras.layers.MaxPool2D(),
                # tf.keras.layers.Conv2D(32, 2, activation='relu'),
                # tf.keras.layers.MaxPool2D(),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(64, activation='relu'), # with 32, 64, 128 almost perfect matches for acc and val
                tf.keras.layers.Dense(num_class)
        ])

        # tf.keras.utils.plot_model(model, to_file='model.png', show_shapes=True)

        model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics='accuracy')
        model.fit(train_ds, validation_data=val_ds, epochs=15)
        model.summary()

        model.save('circle_trained_model.h5')
