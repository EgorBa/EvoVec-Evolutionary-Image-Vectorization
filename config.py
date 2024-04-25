import os

from fitness.loss_type import Fitness
from mutations.concat_path import ConcatPath
from mutations.drop_path import DropPath
from mutations.drop_segment import DropSegment
from mutations.needle import Needle
from mutations.needle_type.constant_type import ConstantType

# folder for tmp pictures
TMP_FOLDER = "tmp"

# debugging flg
DEBUG = True

# path to init pnf Image
PNG_PATH = os.path.join("full_svg_dataset", "batman.png")

# count individuals in generation
INDIVIDUAL_COUNT = 30

# percent of elite
ELITE_PERCENT = 0.1

# step of evol
STEP_EVOL = 300

# fitness type
FITNESS_TYPE = Fitness.IMAGE_DIFF_MSE

# mutations
MUTATION_TYPE = [
    ConcatPath(0.2, 50),
    DropPath(1, 0.0001),
    Needle(probability=0.1, needle_type=ConstantType(0.01))
]

# crossovers
CROSSOVER = []

# color diff
COLOR_DIFF = 200

# max width and height of input image
MAX_W = 512
MAX_H = 512

# path for resized image
RESIZED_PNG_PATH = os.path.join(TMP_FOLDER, f'resized_png.png')
