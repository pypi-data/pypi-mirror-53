import time

import matplotlib.pyplot as plt
from tqdm import tqdm

from on_image import _make_sample_image, multi_img_find

if __name__ == "__main__":
    graph_work = [*range(1, 10), *range(10, 50, 2), *range(50, 105, 5)]

    for i in range(max(graph_work)):
        _make_sample_image(i)

    time_data = []
    for n in tqdm(graph_work, desc="No Pool"):
        work = [f"./images/{i}.png" for i in range(n)]

        t1 = time.time()
        multi_img_find(work, use_mp=False)
        t2 = time.time()
        time_data.append(t2 - t1)
    plt.plot(graph_work, time_data, label="No Pool")

    time_data = []
    for n in tqdm(graph_work, desc="Auto select"):
        work = [f"./images/{i}.png" for i in range(n)]

        t1 = time.time()
        multi_img_find(work)
        t2 = time.time()
        time_data.append(t2 - t1)
    plt.plot(graph_work, time_data, label="Auto select")

    for cpu_cores in [1, 2, 4, 8, 16]:
        time_data = []

        for n in tqdm(graph_work, desc=f"{cpu_cores} core{'' if cpu_cores == 1 else 's'}"):
            work = [f"./images/{i}.png" for i in range(n)]

            t1 = time.time()
            multi_img_find(work, core_count=cpu_cores, use_mp=True)
            t2 = time.time()
            time_data.append(t2-t1)

        plt.plot(graph_work, time_data, label=f"Pool {cpu_cores} cores")

    plt.xlabel("# of images")
    plt.ylabel("seconds")
    plt.legend()
    plt.savefig(f"benchmark.png")
    plt.show()
