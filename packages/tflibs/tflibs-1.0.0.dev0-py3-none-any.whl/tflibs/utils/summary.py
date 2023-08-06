""" Summary """
import tensorflow as tf


def image_summary(name, image):
    try:
        batch_size = image.shape.as_list()[0]
    except ValueError:
        batch_size = 12
    tf.summary.image(name, image, max_outputs=batch_size, family='Images')
