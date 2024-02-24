import os
from typing import List
import random
import time
import threading

import config
from dto.svg_picture import SvgPicture
from utils.color import fix_init_colors
from utils.html_creator import HTMLFile
from utils.resizer import create_resized_image
from utils.stat_creator import create_gif, create_graf, get_gen_file_paths_by_numbers
from vectorize_by_algo import get_initial_svg


def clear_tmp_dir():
    for filename in os.listdir(config.TMP_FOLDER):
        os.remove(os.path.join(config.TMP_FOLDER, filename))


def init_first_generation() -> List[SvgPicture]:
    generation = []
    tmp_path = create_resized_image(config.PNG_PATH, max_w=config.MAX_W, max_h=config.MAX_H)
    individual = get_initial_svg(tmp_path)
    individual.culc_fitness_function()
    fix_init_colors(individual)
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
        parent = cur_population[random.randint(0, len(cur_population) - 1)]
        children.append(parent.__copy__())
    if config.DEBUG:
        print(f'children created, size = {len(children)}')
    return children


def crossover(cur_population: List[SvgPicture]) -> List[SvgPicture]:
    new_population = cur_population
    for cur_crossover in config.CROSSOVER:
        new_population = cur_crossover.crossover(new_population)
    return new_population


def mutation(cur_population: List[SvgPicture], gen_number: int) -> List[SvgPicture]:
    for cur_mutation in config.MUTATION_TYPE:
        threads = []
        for individual in cur_population:
            t = threading.Thread(target=cur_mutation.mutate, args=(individual, gen_number,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    if config.DEBUG:
        print(f'mutation applied, size = {len(cur_population)}')
    return cur_population


def main():
    clear_tmp_dir()

    generation = init_first_generation()

    best_fitness_value = []
    times = []
    start_time = 0
    start_count_paths = generation[0].paths_count
    start_count_segments = generation[0].segments_count
    end_count_paths = generation[0].paths_count
    end_count_segments = generation[0].segments_count

    for i in range(config.STEP_EVOL):
        if config.DEBUG:
            print(f'generation : {i}, size = {len(generation)}')
            start_time = time.time()
        elite = get_most_fittest(generation, int(config.ELITE_PERCENT * config.INDIVIDUAL_COUNT))
        children = create_children(elite)
        mutated_generation = mutation(children, i)
        crossover_generation = crossover(mutated_generation)
        new_generation = elite + crossover_generation
        generation = get_most_fittest(new_generation, config.INDIVIDUAL_COUNT)
        if config.DEBUG:
            best = generation[0]
            path_svg = os.path.join(config.TMP_FOLDER, f'gen_{i}.svg')
            best.save_as_svg(path_svg)
            best_fitness_value.append((i, best.fitness))
            t = round(time.time() - start_time, 3)
            print(f'fitness of best individual = {best.fitness}, '
                  f'time for gen = {t} sec.')
            print("===============================")
            times.append(t)
            end_count_paths = best.paths_count
            end_count_segments = best.segments_count

    if config.DEBUG:
        create_gif(os.path.join(config.TMP_FOLDER, f'gif_animation.gif'))
        path_to_graf = os.path.join(config.TMP_FOLDER, 'graf_of_fitness.png')
        create_graf(best_fitness_value, path_to_graf)
        gen_numbers = [0, int(config.STEP_EVOL / 4), int(config.STEP_EVOL / 2), int(3 * config.STEP_EVOL / 4),
                       config.STEP_EVOL - 1]
        HTMLFile(
            path_to_graf_of_fitness=path_to_graf,
            times=times,
            gen_file_paths=get_gen_file_paths_by_numbers(gen_numbers),
            gen_file_indexes=gen_numbers,
            path_pdf=os.path.join(config.TMP_FOLDER, 'results.pdf'),
            start_count_paths=start_count_paths,
            start_count_segments=start_count_segments,
            end_count_paths=end_count_paths,
            end_count_segments=end_count_segments
        ).save_as_pdf()


if __name__ == "__main__":
    main()
