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
            path_arr = []
            for segment in path.path_arr:
                path_arr.append(segment.__copy__())
            paths.append(SvgPath(path.width, path.height, path_arr, np.array(path.color)))
        child = SvgPicture(paths, config.PNG_PATH)
        children.append(child)
    if config.DEBUG:
        print(f'children created, size = {len(children)}')
    return children


# def crossover(cur_population: List[SvgPicture]) -> List[SvgPicture]:


def mutation(cur_population: List[SvgPicture], gen_number: int) -> List[SvgPicture]:
    for cur_mutation in config.MUTATION_TYPE:
        for individual in cur_population:
            cur_mutation.mutate(individual, gen_number)
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
        create_graf(best_fitness_value, os.path.join(config.TMP_FOLDER, 'graf_of_fitness.png'))


if __name__ == "__main__":
    main()
