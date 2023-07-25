import os
from enum import Enum

from crossover.random_path import RandomPath
from mutations.drop_path import DropPath
from mutations.drop_segment import DropSegment
from mutations.needle import Needle


class Fitness(Enum):
    OPT_TRANSPORT = 1
    IMAGE_DIFF = 2


# folder for tmp pictures
TMP_FOLDER = "tmp"

# debgging flg
DEBUG = True

# path to init pnf Image
PNG_PATH = os.path.join("data", "AgapeDesign.png")

# count individuals in generation
INDIVIDUAL_COUNT = 10

# percent of elite
ELITE_PERCENT = 0.2

# step of evol
STEP_EVOL = 500

# fitness type
FITNESS_TYPE = Fitness.IMAGE_DIFF

# mutations
MUTATION_TYPE = [Needle(0.3), DropSegment(0.05), DropPath(0.005)]

# crossovers
CROSSOVER = []
