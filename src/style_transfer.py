import functools
import os
import random

from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape
    )
    return image


@functools.lru_cache(maxsize=None)
def load_image(image_url, image_size=(512, 512), preserve_aspect_ratio=True):
    """Loads and preprocesses images."""
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = plt.imread(image_url).astype(np.float32)[np.newaxis, ...]
    if img.max() > 1.0:
        img = img / 255.0
    if len(img.shape) == 3:
        img = tf.stack([img, img, img], axis=-1)
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img


def show_n(images, titles=("",)):
    n = len(images)
    image_sizes = [image.shape[1] for image in images]
    w = (image_sizes[0] * 6) // 320
    plt.figure(figsize=(w * n, w))
    gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
    for i in range(n):
        plt.subplot(gs[i])
        plt.imshow(images[i][0], aspect="equal")
        plt.axis("off")
        plt.title(titles[i] if len(titles) > i else "")
    plt.show()


def transfer_style(content_image_url, style_image_url, output_image_size=512):
    content_img_size = (output_image_size, output_image_size)
    style_img_size = (256, 256)
    content_image = load_image(content_image_url, content_img_size)
    style_image = load_image(style_image_url, style_img_size)
    style_image = tf.nn.avg_pool(
        style_image, ksize=[3, 3], strides=[1, 1], padding="SAME"
    )

    hub_handle = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    hub_module = hub.load(hub_handle)
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    return stylized_image, content_image, style_image


def transfer_style_folder(
    content_image_folder, style_image_url, result_folder, output_image_size=512
):
    hub_handle = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    hub_module = hub.load(hub_handle)
    content_img_size = (output_image_size, output_image_size)
    style_img_size = (256, 256)
    style_image = load_image(style_image_url, style_img_size)
    style_image = tf.nn.avg_pool(
        style_image, ksize=[3, 3], strides=[1, 1], padding="SAME"
    )
    for filename in os.listdir(content_image_folder):
        if (
            filename.endswith(".jpg")
            or filename.endswith(".png")
            or filename.endswith(".jpeg")
        ):
            content_image = load_image(
                content_image_folder + "/" + filename, content_img_size
            )
            outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
            stylized_image = outputs[0]
            tf.keras.preprocessing.image.save_img(
                result_folder + "/" + filename, stylized_image[0]
            )


def transfer_random_style_folder(
    content_image_folder, style_folder, result_folder, output_image_size=512
):
    hub_handle = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    hub_module = hub.load(hub_handle)
    content_img_size = (output_image_size, output_image_size)
    style_img_size = (256, 256)
    styles = [(style_folder + "/" + filename) for filename in os.listdir(style_folder)]
    styles.remove(style_folder + "/.DS_Store")
    for filename in os.listdir(content_image_folder):
        if (
            filename.endswith(".jpg")
            or filename.endswith(".JPG")
            or filename.endswith(".png")
            or filename.endswith(".jpeg")
        ):
            style_image_url = random.choice(styles)
            print(style_image_url)
            style_image = load_image(style_image_url, style_img_size)
            style_image = tf.nn.avg_pool(
                style_image, ksize=[3, 3], strides=[1, 1], padding="SAME"
            )
            content_image = load_image(
                content_image_folder + "/" + filename, content_img_size
            )
            outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
            stylized_image = outputs[0]
            tf.keras.preprocessing.image.save_img(
                result_folder + "/" + filename, stylized_image[0]
            )
