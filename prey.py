import random
from PIL import Image, ImageDraw
import math

def normalize(direction, length):
    if all(x == 0 for x in direction):
        return direction
    current_len = math.sqrt(sum([x**2 for x in direction]))
    return [x * length / current_len for x in direction]


class Position:
    # Cut velocity by 30% each step, leave other derivatives of position unchanged
    # TODO: elasticity = 1.0
    def __init__(
        self,
        position=None,
        boundaries=1,
        acceleration_limit=0.01,
        nearness_threshold=0.1,
        drag=[
            1.0,
            0.7,
            1.0]):
        self.drag = drag
        self.boundaries = boundaries
        self.acceleration_limit = acceleration_limit
        self.nearness_threshold = nearness_threshold
        # Position and velocity
        # TODO: Setup within boundaries?
        self.position = position
        if not position:
            # 2Dx3d- 2d for coordinates/direction, 3d means we use the third derivative
            # to target motion by default
            self.position = [
                [random.random()
                 if deriv_level == 0 else 0 for _ in range(2)]
                for deriv_level in range(3)]

    def __repr__(self):
        return f"{self.position[0]}"

    def accelerate_in_direction(self, acceleration):
        self.position[-1] = normalize(acceleration, self.acceleration_limit)
        for derivative_level in range(len(self.position) - 2, -1, -1):
            for dim in range(len(self.position[0])):
                self.position[derivative_level][dim] += self.position[derivative_level + 1][dim]
                self.position[derivative_level][dim] *= 1.0 if derivative_level >= len(
                    self.drag) else self.drag[derivative_level]
        self.bounce()

    
    # If position exceeds the boundaries of the 'map', reflect the position & velocity back into the map
    # Note that in principle, one time step could bounce from one wall to another many times, hence the
    # while loop

    def bounce(self):
        while self._single_bounce():
            pass
        assert(
            all([self.position[0][x] >= 0 for x in range(len(self.position[0]) - 1)]))

    def _single_bounce(self):
        for i in range(len(self.position[0])):
            if self.position[0][i] < 0:
                self._reflect(i, True)
                return True
            if self.position[0][i] > self.boundaries:
                self._reflect(i, False)
                return True
        return False

    def _reflect(self, dim, low):
        if low:
            self.position[0][dim] = -1 * self.position[0][dim]
        else:
            self.position[0][dim] -= 2 * \
                (self.position[0][dim] - self.boundaries)
        for i in range(1, len(self.position) - 1):
            self.position[i][dim] *= -1

    def is_near(self, other_positions):
        return min([dist(self.position[0], p.position[0])
                   for p in other_positions]) < self.nearness_threshold


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


def dist(point_a, point_b):
    return math.sqrt(sum([(point_a[i] - point_b[i])**2 for i in range(len(point_a))]))


def dot_2d(measured_vector, response):
    assert len(measured_vector) == 2
    assert len(response) == 4
    return [measured_vector[0] * response[0] +
            measured_vector[1] * response[1],
            measured_vector[0] * response[2] +
            measured_vector[1] * response[3]]


def col_sum(*input_components):
    #print(input_components)
    result = [0] * len(input_components[0])
    for component in input_components:
        assert len(component) == len(result)
        for dim in range(len(result)):
            result[dim] += component[dim]
    return result

class Behavior:
    num_responses = 2

    def __init__(self, response=[random.gauss(0,1) for _ in range(10)]):
        self.programmed_response = response
        # Each component of a 2d response needs to respond to both the x and y
        # component of what it's responding to, so responding to one thing
        # uses 4 numbers (given the naive implementation)
        # The final 2 response components are the +C component- the default drift
        assert len(self.programmed_response) == Behavior.num_responses * 4 + 2

    def react(self, cats, position):
        # Interpret the first two values of the vector as the default drift behavior
        return col_sum(
          self.programmed_response[0:2],
          dot_2d(cats, self.programmed_response[2:6]),
          dot_2d(position, self.programmed_response[6:10]))

# A special case of behavior that's programmed to ignore the cats, and move in circles
# dx = y - 0.5 (since x and y range from 0. to 1.)
# dy = 0.5 - x
circle_behavior = Behavior([
-0.5, # dx drift
0.5, # dy drift
0, 0, 0, 0, # 4 entries for responding to nearby cats
0, # dx response to x
1.0, # dx response to y
-1.0, # dy response to x
0  # dy response to y
])

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

    """
    Move the cats and mice each one step. Update the plotter, if any
    Return true if the simulation should continue (i.e. mice are alive)
    """

    def iterate(self):
        closest_mice = [argmin(self.mice, lambda mouse: dist(
            mouse.position[0], cat.position[0])) for cat in self.cats]
        closest_cats = [argmin(self.cats, lambda cat: dist(
            mouse.position[0], cat.position[0])) for mouse in self.mice]
        direction_to_mice = [
            [closest_mice[i][0].position[0][d] - cat.position[0][d]
             for d in range(len(cat.position[0]))] for i,
            cat in enumerate(self.cats)]
        mice_moves = [
            self.cat_behavior.react(closest_cats[i][0].position[0], self.mice[i].position[0])
            for i in range(len(self.mice))]
        # Move
        for i, cat in enumerate(self.cats):
            cat.accelerate_in_direction(direction_to_mice[i])
        for i, p in enumerate(self.mice):
            p.accelerate_in_direction(mice_moves[i])
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
        seed = 0):
    if seed:
        random.seed(seed)
    cats = [Position() for _ in range(num_cats)]
    mice = [Position() for _ in range(num_mice)]
    killed = []
    iterations = 0
    s = CatMouseSimulator(cats, mice, cat_behavior, plotter, plotter_complete)
    while s.iterate():
        iterations += 1
    return iterations


def print_locations(cats, mice, killed):
    print(f"cats:{cats}\nmice:{mice}\nkilled{killed}")


class CatMouseVisualizer:
    def __init__(self, size=256, target="/Users/taylor/prey/test", suffix = "", filetype=".gif", limit=None):
        self.limit = limit
        self.target = target + suffix + filetype
        self.img_size = size
        self.imgs = []

    def visualize_locations(self, cats, mice, killed):
        self.imgs.append(
            Image.new('RGB', (self.img_size, self.img_size), "black"))
        draw = ImageDraw.Draw(self.imgs[-1])
        dot_size = self.img_size * Position().nearness_threshold / 2

        def draw_at(pos, color):
            draw.ellipse(
                (pos[0] *
                 self.img_size -
                 dot_size,
                 pos[1] *
                    self.img_size -
                    dot_size,
                    pos[0] *
                    self.img_size +
                    dot_size,
                    pos[1] *
                    self.img_size +
                    dot_size),
                fill=color)

        for dead in killed:
            draw_at(dead.position[0], "blue")
        for mouse in mice:
            draw_at(mouse.position[0], "white")
        for cat in cats:
            draw_at(cat.position[0], "red")
        if self.limit and self.limit == len(self.imgs):
           self.complete()

    def complete(self):
        print(f"Saving {len(self.imgs)} images into a gif")
        Image.new(
            'RGB', (self.img_size, self.img_size),
            "black").save(
            fp=self.target, format='GIF', append_images=self.imgs,
            save_all=True, duration=20, loop=0)

def fun_result():
    vis = CatMouseVisualizer(suffix="manual", limit=1000)
    iters = simulate_cat_mouse(3, 50, 
        Behavior(
            [1.2932335026451751, -0.6136395570170698, 0.2855665089845411, -1.437305314105581, -0.5155442512710706, 0.6109865232330572, -1.2412022889309902, 0.17199899428165452, 1.8130341188020964, -0.4954604336391439]
        ), vis.visualize_locations, vis.complete, seed =74280061 )

def main():
    vecs_to_try = [ [[random.gauss(0, 1) for _ in range(10)] , random.randrange(100000000)] for _ in range(1000)]
    print("\n".join(str(x) for x in vecs_to_try))
    response_times = []
    for i in range(len(vecs_to_try)):
        print(f"Trying {vecs_to_try[i]}")
        vis = CatMouseVisualizer(suffix=str(i))
        iters = simulate_cat_mouse(3, 50, 
            Behavior(vecs_to_try[i][0]), vis.visualize_locations, vis.complete, seed = vecs_to_try[i][1])
        print(f"Lived for {iters}")
        response_times.append(iters)
    print(response_times)


if __name__ == "__main__":
    main()
