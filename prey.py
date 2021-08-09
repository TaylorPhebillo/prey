import random
import math

def normalize(direction, length):
    if all([x == 0 for x in direction]):
        return direction
    current_len = math.sqrt(sum([x**2 for x in direction]))
    return [x * length / current_len for x in direction]

class Position:
    boundaries = 1
    acceleration_limit = 0.1
    nearness_threshold = 0.1
    # TODO: elasticity = 1.0
    def __init__(self):
        # Position and velocity
        # TODO: Setup within boundaries?

        self.position = [[random.random() for _ in range(2)] for _ in range(3)]

    def __repr__(self):
        return f"{self.position[0]}"

    def accelerate_in_direction(self, acceleration):
        self.position[-1] = normalize(acceleration, Position.acceleration_limit)
        for derivative_level in range(len(self.position) - 2, -1, -1):
            for dim in range(len(self.position[0])):
                self.position[derivative_level][dim] += self.position[derivative_level + 1][dim]
        self.bounce()

    """
    If position exceeds the boundaries of the 'map', reflect the position & velocity back into the map
    Note that in principle, one time step could bounce from one wall to another many times, hence the
    while loop
    """
    def bounce(self):
        while self._single_bounce():
            pass
    def _single_bounce(self):
        for i in range(len(self.position[0])):
            if self.position[0][i] < 0:
                self._reflect(i, True)
                return True
            if self.position[0][i] > Position.boundaries:
                self._reflect(i, False)
                return True
        return False

    def _reflect(self, dim, low):
        for i in range(len(self.position)):
            if low:
                self.position[i][dim] *= -1
            else:
                self.position[i][dim] -= Position.boundaries

    def is_near(self, other_positions):
        return min([dist(self.position[0], p.position[0]) for p in other_positions]) < Position.nearness_threshold

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

def dist(a, b):
    return math.sqrt(sum([(a[i] - b[i])**2 for i in range(len(a))]))

class Behavior:
    required_dims = 4
    def __init__(self, response):
        self.response = response
        assert(len(response) == Behavior.required_dims)

    def react(self, cats, position):
        return [0 for _ in range(len(position))]

def print_locations(cats, mice, killed):
    print(f"cats:{cats}\nmice:{mice}\nkilled{killed}")

def simulate(num_cats, num_mice, cat_behavior, plotter = None):

    cats = [Position() for _ in range(num_cats)]
    mice = [Position() for _ in range(num_mice)]
    killed = []
    iterations = 0
    while(mice):
        iterations += 1
        closest_mice = [argmin(mice, lambda mouse: dist(mouse.position[0], cat.position[0])) for cat in cats]
        direction_to_mice = [[closest_mice[i][0].position[0][d] - cat.position[0][d] for d in range(len(cat.position[0]))] for i, cat in enumerate(cats)]
        mice_moves = [cat_behavior.react(cats, mice[i].position[0]) for i in range(len(mice))]
        # Move
        for i, cat in enumerate(cats):
            cat.accelerate_in_direction(direction_to_mice[i])
        for i, p in enumerate(mice):
            p.accelerate_in_direction(mice_moves[i])
        # Kill
        kill_indices = [mice[i].is_near(cats) for i in range(len(mice))]
        killed.extend([(mice[i], iterations) for i in range(len(mice)) if kill_indices[i]])
        mice = [mice[i] for i in range(len(mice)) if not kill_indices[i]]
        # Optionally, plot
        if plotter:
            plotter(cats, mice, killed)
        print()
        print()
    return iterations


def main():
    iters = simulate(1, 3, Behavior([0]*4), print_locations)
    print(f"Lived for {iters}")
    
if __name__ == "__main__":
  main()
