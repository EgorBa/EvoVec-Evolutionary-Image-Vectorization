from sklearn.preprocessing import normalize
import ot
import numpy as np
from PIL import Image

import cache
import config


def opt_transport_loss(png_cnt, cur_cnt):
    # works only for one contour
    png_cnt = png_cnt[0].reshape(-1, 2)
    png_cnt = normalize(png_cnt, norm='l2')
    cur_cnt = cur_cnt[0].reshape(-1, 2)
    cur_cnt = normalize(cur_cnt, norm='l2')

    M = ot.dist(png_cnt, cur_cnt)  # using the Euclidean distance between samples as the cost

    # Compute the transportation plan with EMD
    T = ot.emd([], [], M)  # using empty marginals since we don't have the same number of samples
    # emd_distance = T[0]
    T = T[1]
    # Compute the transportation loss
    transportation_loss = np.sum(T * M)
    return transportation_loss


def image_diff(png_first, png_second) -> float:
    image_first, image_second = read_images(png_first, png_second)
    return float(abs(np.sum(image_second - image_first)))


def image_diff_exp(png_first, png_second) -> float:
    image_first, image_second = read_images(png_first, png_second)
    return float(np.sum(np.exp((abs(image_second - image_first) / 255) * 50 + 1)))


def image_diff_mse(png_first, png_second) -> float:
    image_first, image_second = read_images(png_first, png_second)
    return float(np.sum(np.power((abs(image_second - image_first) / 255), 2)))


def read_images(png_first, png_second):
    if png_first == config.PNG_PATH:
        update_cache_if_need()
        image_first = cache.PNG_IMAGE
    else:
        image_first = np.array(Image.open(png_first).convert('RGB'), dtype=int)
    if png_second == config.PNG_PATH:
        update_cache_if_need()
        image_second = cache.PNG_IMAGE
    else:
        image_second = np.array(Image.open(png_second).convert('RGB'), dtype=int)
    return image_first, image_second


def update_cache_if_need():
    if cache.PNG_IMAGE is None:
        cache.PNG_IMAGE = np.array(Image.open(config.PNG_PATH).convert('RGB'), dtype=int)
