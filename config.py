import os
from enum import Enum


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

# ster of evol
STEP_EVOL = 2000

# fitness type
FITNESS_TYPE = Fitness.IMAGE_DIFF
