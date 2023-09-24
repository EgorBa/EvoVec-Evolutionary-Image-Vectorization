import os
from enum import Enum

from mutations.concat_path import ConcatPath
from mutations.drop_path import DropPath
from mutations.drop_segment import DropSegment
from mutations.needle import Needle


class Fitness(Enum):
    OPT_TRANSPORT = 1
    IMAGE_DIFF = 2
    IMAGE_DIFF_EXP = 3


# folder for tmp pictures
TMP_FOLDER = "tmp"

# debgging flg
DEBUG = True

# path to init pnf Image
PNG_PATH = os.path.join("data", "hippo.png")

# count individuals in generation
INDIVIDUAL_COUNT = 10

# percent of elite
ELITE_PERCENT = 0.2

# step of evol
STEP_EVOL = 30

# fitness type
FITNESS_TYPE = Fitness.IMAGE_DIFF

# mutations
# MUTATION_TYPE = [Needle(0.3), DropPath(0.005)]
MUTATION_TYPE = [ConcatPath(1)]

# crossovers
CROSSOVER = []
