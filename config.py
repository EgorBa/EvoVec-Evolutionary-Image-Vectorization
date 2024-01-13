import os
from enum import Enum

from mutations.concat_path import ConcatPath
from mutations.drop_path import DropPath
from mutations.drop_segment import DropSegment
from mutations.needle import Needle
from mutations.needle_type.constant_type import ConstantType


class Fitness(Enum):
    OPT_TRANSPORT = 1
    IMAGE_DIFF = 2
    IMAGE_DIFF_EXP = 3
    IMAGE_DIFF_MSE = 4


# folder for tmp pictures
TMP_FOLDER = "tmp"

# debugging flg
DEBUG = True

# path to init pnf Image
PNG_PATH = os.path.join("data", "img_7.png")

# count individuals in generation
INDIVIDUAL_COUNT = 30

# percent of elite
ELITE_PERCENT = 0.2

# step of evol
STEP_EVOL = 100

# fitness type
FITNESS_TYPE = Fitness.IMAGE_DIFF_MSE

# mutations
# MUTATION_TYPE = [Needle(0.2, ConstantType(0.001)), DropPath(0.2, 0.0001)]
MUTATION_TYPE = [ConcatPath(0.5, 20), Needle(0.2, ConstantType(10)), DropPath(1, 0.001)]

# crossovers
CROSSOVER = []

# read init image (need to cache image)
PNG_IMAGE = None

# color diff
COLOR_DIFF = 500
