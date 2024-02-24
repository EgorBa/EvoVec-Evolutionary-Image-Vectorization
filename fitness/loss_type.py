from enum import Enum


class Fitness(Enum):
    OPT_TRANSPORT = 1
    IMAGE_DIFF = 2
    IMAGE_DIFF_EXP = 3
    IMAGE_DIFF_MSE = 4
