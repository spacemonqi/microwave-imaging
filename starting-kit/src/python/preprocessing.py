import numpy as np
from matplotlib import pyplot as plt

import main
import sklearn
import png


def plot_layer(img):
    plt.imshow(img)
    plt.show()


def layer_to_png(layer, output_path):
    """

    Args:
        layer: 2d layer of 3d scan
        output_path: path to save the png

    Returns:
        None

    """
    plt.imsave(output_path, layer)



if __name__ == '__main__':
    volume, x_vec, y_vec, z_vec = main.import_volume(
        'C:/Users/Алексей/Documents/Crypto/HackaTUM/microwave-imaging/team-3/20221119-114924-969/20221119-114924-969_reco.img'
    )
    img_2d = main.get_layer(volume, 1)
    layer_to_png(img_2d, 'test_files/test.png')
