# EvoVec: Evolutionary Image Vectorization with Adaptive Curve Number and Color Gradients

Primary contact: [Egor Bazhenov](tujh.bazhenov.kbn00@mail.ru)

## Examples of work

| Init image       | ![](data/test%20images/readme%20examples/init_hippo.png)    | ![](data/test%20images/readme%20examples/init_land.png)    | ![](data/test%20images/readme%20examples/init_list.png)    | ![](data/test%20images/readme%20examples/init_monkey.png)    | ![](data/test%20images/readme%20examples/init_smile.png)    |
|------------------|-------------------------------------------------------------|------------------------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------|-------------------------------------------------------------|
| Vectorized image | ![](data/test%20images/readme%20examples/my_algo_hippo.png) | ![](data/test%20images/readme%20examples/my_algo_land.png) | ![](data/test%20images/readme%20examples/my_algo_list.png) | ![](data/test%20images/readme%20examples/my_algo_monkey.png) | ![](data/test%20images/readme%20examples/my_algo_smile.png) |

We present a new method for vectorizing images using a variable number of paths based on an evolutionary algorithm.
The result of the deterministic algorithm is selected as the initial population. Further, various mutations and crossovers are iteratively applied to obtain a better vectorized image.

## Usage

1. ``git clone https://github.com/EgorBa/EvoVec-Evolutionary-Image-Vectorization``
2. ``pip install requirements.txt``
3. Configure [config file](config.py) for your task

#### Config parameters description

| Parameter name   | Description                                                         | Value type                      |
|------------------|---------------------------------------------------------------------|---------------------------------|
| DEBUG            | Need show debug info                                                | Boolean                         |
| PNG_PATH         | Path to png file for vectorization                                  | String                          |
| INDIVIDUAL_COUNT | Count individuals in one population                                 | Int                             |
| ELITE_PERCENT    | Percentage of the population that should remain                     | Float                           |
| STEP_EVOL        | Number of vectorization epochs                                      | Int                             |
| FITNESS_TYPE     | Type of selection function                                          | [Fitness](fitness/loss_type.py) |
| MUTATION_TYPE    | Array of mutations used                                             | Array<[Mutation](mutations)>    |
| CROSSOVER        | Array of crossovers used                                            | Array<[Crossover](crossover)>   |
| COLOR_DIFF       | Maximum difference in the color of pixels that need to be corrected | Int                             |
| MAX_W, MAX_H     | Maximum value of the width and height of the vectorized image       | Int                             |

4. ``python main.py``
