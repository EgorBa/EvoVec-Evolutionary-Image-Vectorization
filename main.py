import os
from typing import List
import random
import numpy as np

import config
from dto.svg_path import SvgPath
from dto.svg_picture import SvgPicture
from vectorize_by_algo import get_initial_svg


def init_first_generation() -> List[SvgPicture]:
    generation = []
    individual = get_initial_svg(config.PNG_PATH)
    for i in range(config.INDIVIDUAL_COUNT):
        generation.append(individual.__copy__())
    if config.DEBUG:
        print("first generation created")
    return generation


def get_most_fittest(cur_population: List[SvgPicture], count: int) -> List[SvgPicture]:
    for individual in cur_population:
        individual.culc_fitness_function()
    cur_population.sort(key=lambda x: x.fitness)
    return cur_population[-count:]


def create_children(cur_population: List[SvgPicture]) -> List[SvgPicture]:
    children = []
    for i in range(config.INDIVIDUAL_COUNT):
        first_parent = cur_population[random.randint(0, len(cur_population) - 1)]
        second_parent = cur_population[random.randint(0, len(cur_population) - 1)]
        paths = []
        for path in first_parent.paths:
            paths.append(SvgPath(path.width, path.height, np.array(path.path_arr)))
        child = SvgPicture(paths, config.PNG_PATH)
        children.append(child)
    if config.DEBUG:
        print(f'children created, size = {len(children)}')
    return children


# def crossover(cur_population: List[SvgPicture]) -> List[SvgPicture]:


def mutation(cur_population: List[SvgPicture]) -> List[SvgPicture]:
    for individual in cur_population:
        if random.random() < 0.3:
            random_path = individual.paths[random.randint(0, len(individual.paths) - 1)]
            random_index = random.randint(0, len(random_path.path_arr) - 1)
            before = random_path.path_arr[random_index]
            if random.random() < 0.5:
                random_path.path_arr[random_index] = (before + 0.1) % 1
            else:
                random_path.path_arr[random_index] = (before - 0.1) % 1
    if config.DEBUG:
        print(f'mutation applied, size = {len(cur_population)}')
    return cur_population


def main():
    generation = init_first_generation()

    for i in range(500):
        if config.DEBUG:
            print(f'generation : {i}, size = {len(generation)}')
        elite = get_most_fittest(generation, int(config.ELITE_PERCENT * config.INDIVIDUAL_COUNT))
        children = create_children(elite)
        new_generation = elite + children
        mutated_generation = mutation(new_generation)
        generation = get_most_fittest(mutated_generation, config.INDIVIDUAL_COUNT)
        if config.DEBUG:
            best = generation[-1]
            best.save_as_svg(os.path.join("tmp", f'gen_{i}.svg'))
            print(f'fitness of best individual = {best.fitness}')
            print(best.fitness)


if __name__ == "__main__":
    main()
