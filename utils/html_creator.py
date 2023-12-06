import os
from typing import List

import pdfkit

import config

import base64


class HTMLFile:
    path_to_graf_of_fitness: str
    gen_file_paths: List[str]
    gen_file_indexes: List[int]
    times: List[float]
    path_pdf: str
    start_count_paths: int
    start_count_segments: int
    end_count_paths: int
    end_count_segments: int

    def __init__(self, path_to_graf_of_fitness: str, times: List[float], gen_file_paths: List[str],
                 gen_file_indexes: List[int], path_pdf: str, start_count_paths: int, start_count_segments: int,
                 end_count_paths: int, end_count_segments: int):
        self.path_to_graf_of_fitness = path_to_graf_of_fitness
        self.gen_file_paths = gen_file_paths
        self.gen_file_indexes = gen_file_indexes
        self.path_pdf = path_pdf
        self.times = times
        self.start_count_paths = start_count_paths
        self.start_count_segments = start_count_segments
        self.end_count_paths = end_count_paths
        self.end_count_segments = end_count_segments

    def save_as_pdf(self):
        begin = '<!DOCTYPE html>\n<html lang=\"en\">\n\t<head>\n\t\t<meta charset=\"UTF-8\">\n\t\t<title>Vectorize algo report</title>\n\t</head>\n\t<body>\n'
        title = '\t\t<h2>Vectorize algo report.</h2>\n'
        count_of_individuals_in_generation = f'\t\t<p>Count of individuals in population = {config.INDIVIDUAL_COUNT}</p>\n'
        count_steps_evol = f'\t\t<p>Count of steps in evaluation algorithm = {config.STEP_EVOL}</p>\n'
        params_mutation = self.create_used_params(config.MUTATION_TYPE)
        params_crossover = self.create_used_params(config.CROSSOVER)
        avg_time = f'\t\t<p>Time of work of algorithm = {self.get_time(sum(self.times))}</p>\n'
        sum_time = f'\t\t<p>Avg time of work of 1 iteration = {self.get_time(sum(self.times) / len(self.times))}</p>\n'
        count_of_paths = f'\t\t<p>Init paths count : {self.start_count_paths}, evolution paths count : {self.end_count_paths}</p>\n'
        count_of_segments = f'\t\t<p>Init count of segments : {self.start_count_segments}, evolution count of segments {self.end_count_segments}</p>\n'
        table = self.create_table_with_selected_gen(self.gen_file_paths, self.gen_file_indexes)
        image = f'\t\t<figure>\n\t\t\t<img src=\"data:image/png;base64,{self.image_file_path_to_base64_string(self.path_to_graf_of_fitness)}\" alt=\"Graf of fitness\" width=\"400px\">\n\t\t\t<figcaption>Graf of fitness</figcaption>\n\t\t</figure>\n'
        end = '\t</body>\n</html>'

        html_text = begin + title + count_of_individuals_in_generation + count_steps_evol + count_of_paths + count_of_segments + avg_time + sum_time + params_mutation + params_crossover + table + image + end

        f = open("sample.html", "w")
        f.write(html_text)
        f.close()

        pdfkit.from_file('sample.html', self.path_pdf)
        os.remove('sample.html')

    def create_used_params(self, array) -> str:
        data = []
        key_word = "unknown operation"
        if array == config.MUTATION_TYPE:
            key_word = 'mutations'
        elif array == config.CROSSOVER:
            key_word = 'crossovers'
        if len(array) > 0:
            for m in array:
                data.append(m.__str__())
            return f'\t\t<p>Used {key_word} = {data.__str__()}</p>\n'
        else:
            return f'\t\t<p>No used {key_word}</p>\n'

    def image_file_path_to_base64_string(self, filepath: str) -> str:
        with open(filepath, 'rb') as f:
            return base64.b64encode(f.read()).decode()

    def create_table_with_selected_gen(self, gen_files: List[str], gen_index: List[int]) -> str:
        begin_table = '\t\t<table>\n\t\t\t<caption>Some results of evaluation</caption>\n\t\t\t<tr>\n'
        first_line = ''
        second_line = ''
        first_line += f'\t\t\t\t<th><img src=\"data:image/png;base64,{self.image_file_path_to_base64_string(config.PNG_PATH)}\" alt=\"Source file\" width=\"200px\"></th>\n'
        second_line += f'\t\t\t\t<th>Source Image</th>\n'
        for idx, gen in zip(gen_index, gen_files):
            first_line += f'\t\t\t\t<th><img src=\"data:image/png;base64,{self.image_file_path_to_base64_string(gen)}\" alt=\"Gen {idx}\" width=\"200px\"></th>\n'
            second_line += f'\t\t\t\t<th>Generation : {idx}</th>\n'
        first_line_end = '\t\t\t</tr>\n\t\t\t<tr>\n'
        end = f'\t\t\t</tr>\n\t\t</table>\n'
        return begin_table + first_line + first_line_end + second_line + end

    def get_time(self, time: float) -> str:
        if time < 60:
            return f'{round(time, 3)} secs.'
        elif time < 60 * 60:
            return f'{round(time / 60, 3)} mins.'
        else:
            return f'{round(time / (60 * 60), 3)} hours.'
