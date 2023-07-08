from sklearn.preprocessing import normalize
import ot
import numpy as np


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
