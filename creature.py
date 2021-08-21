import math
import random


def dist(point_a, point_b):
    return math.sqrt(
        sum([(point_a[i] - point_b[i])**2 for i in range(len(point_a))]))


class Creature:
    def __init__(
        self,
        position=None,
        boundaries=1,
        acceleration_limit=0.01,
        nearness_threshold=0.1,
        drag=[  # Cut velocity by 30% each step, leave other derivatives of position unchanged
            1.0,
            0.7,
            1.0]):
        self.drag = drag
        self.boundaries = boundaries
        self.acceleration_limit = acceleration_limit
        self.nearness_threshold = nearness_threshold
        # Creature and velocity
        self._position = position
        if not position:
            # 2Dx3d- 2d for coordinates/direction, 3d means we use the third derivative
            # to target motion by default
            self._position = [
                [random.uniform(0, boundaries)
                 if deriv_level == 0 else 0 for _ in range(2)]
                for deriv_level in range(3)]

    def __setitem__(self, key, value):
        """indexing into a creature means requesting the X or Y coordinate"""
        assert key == 0 or key == 1
        self._position[0][key] = value

    def __getitem__(self, key):
        """indexing into a creature means requesting the X or Y coordinate"""
        assert key == 0 or key == 1
        return self._position[0][key]

    def __len__(self):
        return 2

    def __repr__(self):
        return f"{self._position[0]}"

    def accelerate_in_direction(self, acceleration):
        # treat "acceleration" as the highest supported derivative,
        # then update lower derivatives accordingly until the raw coordinates
        # are updated
        def normalize(direction, length):
            if all(x == 0 for x in direction):
                return direction
            current_len = math.sqrt(sum([x**2 for x in direction]))
            return [x * length / current_len for x in direction]

        self._position[-1] = normalize(acceleration, self.acceleration_limit)
        for derivative_level in range(len(self._position) - 2, -1, -1):
            for dim in range(len(self._position[0])):
                self._position[derivative_level][dim] += self._position[derivative_level + 1][dim]
                # To keep things stable, cut down some derivative components
                # (usually velocity)
                self._position[derivative_level][dim] *= 1.0 if derivative_level >= len(
                    self.drag) else self.drag[derivative_level]
        self.bounce()

    def bounce(self):
        """If position exceeds the boundaries of the 'map', reflect the position & velocity back into the map"""
        # Note that in principle, one time step could bounce from one wall to another many times, hence the
        # while loop
        while self._single_bounce():
            pass
        # Check that everything is in bounds after enough bounces
        assert self[0] >= 0 and self[1] >= 0 and self[0] <= self.boundaries and self[1] <= self.boundaries

    def _single_bounce(self):
        for i in range(len(self._position[0])):
            if self[i] < 0:
                self._reflect(i, True)
                return True
            if self[i] > self.boundaries:
                self._reflect(i, False)
                return True
        return False

    def _reflect(self, dim, too_low):
        """ Bounce in the X or Y direction """
        if too_low:
            # Bounce off the bottom/left wall
            self[dim] = -1 * self[dim]
        else:
            # Bounce off the high/right wall
            self[dim] -= 2 * \
                (self[dim] - self.boundaries)
        # No matter what we bounced off, reflect all higher derivatives
        for i in range(1, len(self._position) - 1):
            self._position[i][dim] *= -1

    def is_near(self, other_positions):
        return min([dist(self, p)
                   for p in other_positions]) < self.nearness_threshold
