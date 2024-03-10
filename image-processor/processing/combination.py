import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity
from skimage.util import img_as_float


def find_difference(image1, image2):
    assert image1.shape == image2.shape, "Specify two images with the same shape."
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)
    (score, difference_image) = structural_similarity(gray_image1, gray_image2, full=True)
    print("Similarity of the images: ", score)
    normalized_difference_image = (difference_image - np.min(difference_image)) / (np.max(difference_image) - np.min(difference_image))
    return normalized_difference_image


def transfer_histogram(image1, image2):
    image1_float = img_as_float(image1)
    image2_float = img_as_float(image2)
    matched_image = match_histograms(image1_float, image2_float)
    return matched_image
