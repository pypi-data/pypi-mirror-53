import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from typing import Optional
from .utils import plot_df_images


def save_model_json(model_arch_path, model):
    with open(model_arch_path, "w") as f:
        f.write(model.to_json())


def load_model_json(model_arch_path, model_weights_path):
    with open(model_arch_path, "r") as f:
        model = keras.models.model_from_json(f.read())
    model.load_weights(model_weights_path)
    return model

# Visualize activations and filters
def deprocess_image(x):
    x -= x.mean()
    x /= (x.std() + 1e-5)
    x *= 0.1

    x += 255
    x = np.clip(x, 0, 1)

    x *= 255
    x = np.clip(x, 0, 255).astype('uint8')
    return x


def visualize_one_filter(model, layer_name: str, filter_index: int, size=150):
    """
    Builds a loss function that maximizes the activation of the nth filter of the specified layer.
    To plot filter image use plt.imshow(visualise_one_filter(model, layer_name, filter_index, size=150))
    :param model: trained model.
    :param layer_name: layer you want to visualise.
    :param filter_index: filter index.
    :param size: size of filter
    :return:
    """
    layer_output = model.get_layer(layer_name).output
    loss = tf.reduce_mean(layer_output[:, :, :, filter_index])

    grads = tf.gradients(loss, model.input)[0]
    grads /= (tf.sqrt(tf.reduce_mean(tf.square(grads))) + 1e-5)

    iterate = tf.function([model.input], [loss, grads])

    input_img_data = np.random.random((1, size, size, 3)) * 20 + 128

    step = 1
    for i in range(40):
        loss_value, grads_value = iterate([input_img_data])
        input_img_data += grads_value * step

    img = input_img_data[0]
    return deprocess_image(img)


def visualize_filters(model, layer_name, size=64, margin=5):
    results = np.zeros((8 * size + 7 * margin, 8 * size + 7 * margin, 3))
    for i in range(8):
        for j in range(8):
            filter_img = visualize_one_filter(model, layer_name, i + (j * 8), size=size)

            horizontal_start = i * size + i * margin
            horizontal_end = horizontal_start + size
            vertical_start = j * size + j * margin
            vertical_end = vertical_start + size
            results[horizontal_start: horizontal_end, vertical_start: vertical_end, :] = filter_img

    plt.figure(figsize=(20, 20))
    plt.imshow(results)


def visualize_activations(
        model,
        img_path: str,
        layers_to: int,
        layers_from: Optional[bool]=False,
        target_size: Optional[tuple]=(224, 224),
        cmap: Optional[str]='viridis'
    ) -> None:
    """
    used to visualize modedl activations
    :param model: Model which activations you want to visualize.
    :param img_path: Image which activations you want to see.
    :param layers_to: Up to which layer you want to plot activations
    :param layers_from: From which layer you want to start plotting. Default = 0.
    :param target_size: Size of image you want to process. The size of image used for model training.
    :param cmap: Cmap for image plotting
    :return: None
    """
    layer_outputs = [layer.output for layer in
                     model.layers[layers_from:layers_to]]  # Extracts the outputs of the top 12 layers
    activation_model = keras.models.Model(inputs=model.input,
                                          outputs=layer_outputs)  # Creates a model that will return these outputs, given the model input

    layer_names = []
    for layer in model.layers[layers_from:layers_to]:
        layer_names.append(layer.name)  # Names of the layers, so you can have them as part of your plot

    img = keras.preprocessing.image.load_img(img_path, target_size=target_size)
    img_tensor = keras.preprocessing.image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    print(img_tensor.shape)
    plt.imshow(img_tensor[0])
    plt.show()

    activations = activation_model.predict(img_tensor)

    images_per_row = 16

    for layer_name, layer_activation in zip(layer_names, activations):  # Displays the feature maps
        n_features = layer_activation.shape[-1]  # Number of features in the feature map
        size = layer_activation.shape[1]  # The feature map has shape (1, size, size, n_features).
        n_cols = n_features // images_per_row  # Tiles the activation channels in this matrix
        display_grid = np.zeros((size * n_cols, images_per_row * size))
        for col in range(n_cols):  # Tiles each filter into a big horizontal grid
            for row in range(images_per_row):
                channel_image = layer_activation[0,
                                :, :,
                                col * images_per_row + row]
                channel_image -= channel_image.mean()  # Post-processes the feature to make it visually palatable
                channel_image /= channel_image.std()
                channel_image *= 64
                channel_image += 128
                channel_image = np.clip(channel_image, 0, 255).astype('uint8')
                display_grid[col * size: (col + 1) * size,  # Displays the grid
                row * size: (row + 1) * size] = channel_image
        scale = 1. / size
        if display_grid.shape[0] > 0:
            h = display_grid.shape[0]
        else:
            continue

        plt.figure(figsize=(scale * display_grid.shape[1],
                            scale * display_grid.shape[0]))
        plt.title(layer_name)
        plt.grid(False)
        plt.imshow(display_grid, aspect='auto', cmap=cmap)


# Plotting confused and etc
def get_most_confused(
        df: pd.DataFrame,
        path_column: str,
        predictions: np.array,
        labels: np.array,
        image_count: int,
        difference_rate: Optional[float]=None,
        plot: Optional[bool]=True,
        random_plot: Optional[bool]=True,
    ) -> pd.DataFrame:
    """
    Plots given number of images from DataFrame, which predicted values differs from real values
    by specified difference_rate.
    :param df: DataFrame you use for predictions.
    :param path_column: Column where image paths are specified
    :param predictions: Predictions tensor.
    :param labels: Label tensor.
    :param image_count: number of images you want to plot
    :param difference_rate: percentage of difference between predicted and real values (0-1)
    :param plot: If True images are plotted, otherwise returns pd.DataFrame. Default True
    :param random_plot: If True selects images randomly. Default True
    :return: pd.DataFrame
    """
    max_predictions = predictions.argmax(axis=1)
    data = {
        'pred_label / label / df_label': [],
        'image': []
    }
    for i, (a, b, c) in enumerate(zip(max_predictions, labels, df['AdoptionSpeed'].tolist())):
        if not difference_rate:
            if a != b:
                data['pred_label / label / df_label'].append(f'{a} / {b} / {c}')
                data['image'].append(df.iloc[i].image)
        else:
            y_hat = int(a)
            y = int(b)
            if predictions[i][y_hat] - predictions[i][y] >= difference_rate:
                predicted = str(round(predictions[i][y_hat], 4))
                real_class = str(round(predictions[i][y], 4))
                data['pred_label / label / df_label'].append(f'{y_hat}: {predicted} / {y}: {real_class} / {c}')
                data['image'].append(df.iloc[i].image)

    confused_df = pd.DataFrame(data)

    if not plot:
        return confused_df

    print(
        f'From {len(df)} images of tested dataframe {len(confused_df)} images were predicted incorrectly with the difference_rate = {difference_rate}.\n')
    plot_df_images(confused_df, 'image', image_count, 'pred_label / label / df_label', random_plot=random_plot)



# TODO create class with predictions: do evaluate, predict, test_labels, plot_most_confused??
# TODO check fast.ai API to cleanup dataset

if __name__ == '__main__':
    layer_name = 'block1_conv1'
    filter_index = 0
    # plt.imshow(visualise_one_filter(model, layer_name, filter_index, size=150))