import random
from cat_mouse import simulate_cat_mouse
from behavior import Behavior
from visualizers import CatMouseVisualizer

class HillClimber:
    def __init__(self, start_func, neighbor_func, fitness_func):
        self.start = start_func
        self.neighbor_func = neighbor_func
        self.fitness_func = fitness_func

    def optimize(self, iterations=10):
        position = self.start()
        best_fit = self.fitness_func(position)
        for _ in range(iterations):
            print(f"Position: {position}, best_fit: {best_fit}")
            candidate_position = self.neighbor_func(position)
            fit = self.fitness_func(candidate_position)
            if fit > best_fit:
                position = candidate_position
                best_fit = fit

        return position, best_fit

    def optimize_with_restarts(self, iterations=100, restarts=10):
        position = None
        best_fit = -float('inf')
        for _ in range(restarts):
            candidate_position, fit = self.optimize(iterations)
            if fit > best_fit:
                position = candidate_position
                best_fit = fit

        return position, best_fit

def cat_mouse_opt_adaptor_no_vis(behavior_pos):
    iters = [
        simulate_cat_mouse(
            3,
            50,
            Behavior(behavior_pos),
            ) for _ in range(100)]
    return sum(iters)

def cat_mouse_opt_adaptor(behavior_pos):
    noop = lambda *args: None
    vis = CatMouseVisualizer(suffix=f"{behavior_pos}")
    iters = [
        simulate_cat_mouse(
            3,
            50,
            Behavior(behavior_pos),
            vis.visualize_locations if sample == 0 else noop,
            vis.complete if sample == 0 else noop) for sample in range(100)]
    return sum(iters)

def gauss():
    return random.gauss(0, 1)

def main():
    climber = HillClimber(lambda: [gauss() for _ in range(10)],
                          lambda x: [x[i] + (gauss() / 30) for i in range(10)],
                          cat_mouse_opt_adaptor_no_vis)
    result = climber.optimize_with_restarts(2, 2)
    cat_mouse_opt_adaptor(result[0])
    print(result)

if __name__ == "__main__":
    main()
