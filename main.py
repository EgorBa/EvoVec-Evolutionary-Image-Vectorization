import os
from typing import List
import random
import numpy as np

import config
from dto.svg_path import SvgPath
from dto.svg_picture import SvgPicture
from utils.stat_creator import create_gif, create_graf
from vectorize_by_algo import get_initial_svg


def clear_tmp_dir():
    for filename in os.listdir(config.TMP_FOLDER):
        os.remove(os.path.join(config.TMP_FOLDER, filename))


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
    return cur_population[:count]


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


def mutation(cur_population: List[SvgPicture], gen_number: int) -> List[SvgPicture]:
    for individual in cur_population:
        if random.random() < 0.3:
            random_path = individual.paths[random.randint(0, len(individual.paths) - 1)]
            random_index = random.randint(0, len(random_path.path_arr) - 1)
            before = random_path.path_arr[random_index]
            sign = 1
            if random.random() < 0.5:
                sign = -1
            new_value = (before + sign * (0.1 - 0.001 * gen_number)) % 1
            random_path.path_arr[random_index] = new_value
    if config.DEBUG:
        print(f'mutation applied, size = {len(cur_population)}')
    return cur_population


def main():
    generation = init_first_generation()

    clear_tmp_dir()
    best_fitness_value = []

    for i in range(config.STEP_EVOL):
        if config.DEBUG:
            print(f'generation : {i}, size = {len(generation)}')
        elite = get_most_fittest(generation, int(config.ELITE_PERCENT * config.INDIVIDUAL_COUNT))
        children = create_children(elite)
        mutated_generation = mutation(children, i)
        new_generation = elite + mutated_generation
        generation = get_most_fittest(new_generation, config.INDIVIDUAL_COUNT)
        if config.DEBUG:
            best = generation[0]
            path_svg = os.path.join(config.TMP_FOLDER, f'gen_{i}.svg')
            best.save_as_svg(path_svg)
            best_fitness_value.append((i, best.fitness))
            print(f'fitness of best individual = {best.fitness}')
            print("===============================")

    if config.DEBUG:
        create_gif(os.path.join(config.TMP_FOLDER, f'gif_animation.gif'))
        create_graf(best_fitness_value, os.path.join(config.TMP_FOLDER,'graf_of_fitness.png'))


if __name__ == "__main__":
    main()
