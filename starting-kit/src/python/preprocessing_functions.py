import time

import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

import main
import sklearn
import png
import skimage

def plot_layer(img):
    plt.imshow(img)
    plt.show()


def layer_to_png(layer, output_path):
    # print()
    plt.imsave(output_path, layer)


def reduce_dimensionality(image_list):
    img_compressed = [skimage.transform.resize(i, (64, 64)) for i in image_list]

    fig, ax = plt.subplots(2)
    ax[0].imshow(image_list[0])
    ax[1].imshow(img_compressed[0])
    plt.show()

    return img_compressed


def filter_noise(layer):
    filtered_layer = layer.copy()
    filtered_layer[
        filtered_layer < np.percentile(filtered_layer, 60)
    ] = 0
    return filtered_layer


def import_volume(path):
    volume, x_vec, y_vec, z_vec = main.import_volume(path)
    img = np.abs(main.compute_mip(volume)[0])
    return img

if __name__ == '__main__':
    start_time = time.time()
    img_2d = import_volume('C:/Users/Алексей/Documents/Crypto/HackaTUM/microwave-imaging/data/raw/20221119-135950-648/20221119-135950-648_reco.img')

    img_filtered = filter_noise(img_2d)
    layer_to_png(img_filtered, 'test_files/test.png')
    print(time.time() - start_time)

    # img_2d_reduced = reduce_dimensionality(img_2d)
    # layer_to_png(img_2d_reduced, 'test_files/test_reduced.png')
