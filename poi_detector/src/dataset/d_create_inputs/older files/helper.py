import matplotlib.pyplot as plt
import librosa.display
import numpy as np
from PIL import Image
import skimage.io


def create_and_save_transform_image(wav_path, transform):
    plt.interactive(False)

    ax = librosa.display.specshow(transform)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    # plt.savefig(wav_path, bbox_inches='tight', pad_inches=0, format='png')
    plt.show()
    raise Exception()


def create_and_save_transform_image2(wav_path, transform):
    img = Image.fromarray(transform, 'RGB')
    img.show()

    raise Exception()


def create_and_save_transform_image3(spec_path, transform):
    transform = np.transpose(transform)
    skimage.io.imsave(spec_path, transform)


def load_transform(spec_path):
    return skimage.io.imread(spec_path)
