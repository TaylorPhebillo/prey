import random
import math
from behavior import Behavior
from cat_mouse import simulate_cat_mouse
from visualizers import CatMouseVisualizer


def main():
    vecs_to_try = [
        [[random.gauss(0, 1) for _ in range(10)],
         random.randrange(100000000)] for _ in range(1000)]
    print("\n".join(str(x) for x in vecs_to_try))
    response_times = []
    for i, (response_vec, seed) in enumerate(vecs_to_try):
        print(f"Trying {vecs_to_try[i]}")
        vis = CatMouseVisualizer(suffix=str(i))
        iters = simulate_cat_mouse(
            3,
            50,
            Behavior(
                response_vec),
            vis.visualize_locations,
            vis.complete,
            seed=seed)
        print(f"Lived for {iters}")
        response_times.append(iters)
    print(response_times)


if __name__ == "__main__":
    main()
