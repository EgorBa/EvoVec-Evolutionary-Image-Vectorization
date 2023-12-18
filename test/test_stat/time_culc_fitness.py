import time

import config
from vectorize_by_algo import get_initial_svg
import matplotlib.pyplot as plt
from tqdm import tqdm

item = get_initial_svg(config.PNG_PATH)
times = []
path_count = []
for i in tqdm(range(min(item.paths_count - 1, 1000))):
    start_time = time.time()
    item.culc_fitness_function()
    times.append(time.time() - start_time)
    path_count.append(item.paths_count)
    item.del_path(0)


plt.plot(path_count, times)
plt.xlabel("Count of path", fontsize=14)
plt.ylabel("Time, s.", fontsize=14)
plt.savefig('stat_time.png')
