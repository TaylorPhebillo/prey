import random
from cat_mouse import simulate_cat_mouse
from behavior import Behavior
from visualizers import CatMouseVisualizer

class HillClimber:
    def __init__(self, start, neighbor_func, fitness_func):
        self.start = start
        self.neighbor_func = neighbor_func
        self.fitness_func = fitness_func

    def optimize(self, iterations=10):
        position = self.start
        best_fit = self.fitness_func(position)
        for _ in range(iterations):
            print(f"Position: {position}, best_fit: {best_fit}")
            candidate_position = self.neighbor_func(position)
            fit = self.fitness_func(candidate_position)
            if fit > best_fit:
                position = candidate_position
                best_fit = fit

        return position, best_fit

def gauss():
    return random.gauss(0,1)

def main():
    vis = CatMouseVisualizer(suffix="opt")
    h = HillClimber([gauss() for _ in range(10)],
            lambda x:  [x[i] + gauss() for i in range(10)],
            lambda x:  simulate_cat_mouse(3, 50, Behavior(x), vis.visualize_locations, vis.complete))
    print(h.optimize())

if __name__ == "__main__":
    main()
