import random
from creature import Creature, dist
import math


def argmin(args, func):
    min_v = float('inf')
    min_arg = None
    min_i = 0
    for i, arg in enumerate(args):
        res = func(arg)
        if res < min_v:
            min_v = res
            min_arg = arg
            min_i = i
    return (min_arg, min_v, min_i)


class CatMouseSimulator:
    def __init__(
            self,
            cat_locations,
            mice_locations,
            cat_behavior,
            plotter,
            plotter_complete=None):
        self.cats = cat_locations
        self.mice = mice_locations
        self.cat_behavior = cat_behavior
        self.plotter = plotter
        self.plotter_complete = plotter_complete
        self.killed = []

    def iterate(self):
        """
        Move the cats and mice each one step. Update the plotter, if any
        Return true if the simulation should continue (i.e. mice are alive)
        """
        closest_mice = [argmin(self.mice, lambda mouse: dist(
            mouse, cat)) for cat in self.cats]
        closest_cats = [argmin(self.cats, lambda cat: dist(
            mouse, cat)) for mouse in self.mice]
        direction_to_mice = [
            [closest_mice[i][0][d] - cat[d]
             for d in range(len(cat))] for i,
            cat in enumerate(self.cats)]
        mice_moves = [self.cat_behavior.react(
            closest_cats[i][0],
            self.mice[i])
            for i in range(len(self.mice))]
        # Move
        for i, cat in enumerate(self.cats):
            cat.accelerate_in_direction(direction_to_mice[i])
        for i, mouse in enumerate(self.mice):
            mouse.accelerate_in_direction(mice_moves[i])
        # Kill
        kill_indices = [self.mice[i].is_near(
            self.cats) for i in range(len(self.mice))]
        self.killed.extend([self.mice[i]
                           for i in range(len(self.mice)) if kill_indices[i]])
        self.mice = [self.mice[i]
                     for i in range(len(self.mice)) if not kill_indices[i]]
        # Optionally, plot
        if self.plotter:
            self.plotter(self.cats, self.mice, self.killed)
        if len(self.mice) != 0:
            return True
        if self.plotter_complete:
            self.plotter_complete()
        return False


def simulate_cat_mouse(
        num_cats,
        num_mice,
        cat_behavior,
        plotter=None,
        plotter_complete=None,
        seed=0):
    if seed:
        random.seed(seed)
    cats = [Creature() for _ in range(num_cats)]
    mice = [Creature() for _ in range(num_mice)]
    iterations = 0
    s = CatMouseSimulator(cats, mice, cat_behavior, plotter, plotter_complete)
    while s.iterate():
        iterations += 1
    return iterations
