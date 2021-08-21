import unittest
import prey
from prey import Creature


def is_position_equal(pos, expected):
    try:
        # Not clear if we got coordinates or a position object, so try to
        # extract coordinates
        return is_position_equal(pos.position, expected)
    except AttributeError:
        pass
    if not expected:
        return True
    try:
        return all([is_position_equal(pos[i], expected[i])
                   for i in range(len(expected))])
    except TypeError:
        return pos == expected
    raise ("Mismatch")


class TestSimulation(unittest.TestCase):
    def test_behavior_length_except(self):
        with self.assertRaises(AssertionError):
            p = prey.Behavior([])

    def test_simulator_stops(self):
        # With no mice, simulation should stop immediately
        s = prey.CatMouseSimulator([], [], prey.Behavior(), None)
        self.assertFalse(s.iterate())

    def build_position_checker(self):
        pass

    def test_cat_acceleration(self):
        """
        Simulate one step, moving by velocity (2nd derivative, so position matrix is len 2)-
        cat should accelerate one step to the mouse
        """
        def test_cat_from(init_position, plot_validator, should_mice_remain):
            s = prey.CatMouseSimulator(
                [Creature([init_position, [0, 0]])],
                [Creature([[0, 0], [0, 0]])],
                prey.Behavior(),
                plot_validator)
            self.assertEqual(s.iterate(), should_mice_remain)
        test_cat_from([0, 0], None, False)


class TestCreature(unittest.TestCase):
    def test_move(self):
        # Move with no momentum- each movement just updates velocity
        p = Creature([[0, 0], [0, 0]], 1, 0.1)
        p.accelerate_in_direction([1, 0])
        self.assertTrue(is_position_equal(p, [[0.1, 0], [0.1, 0]]))
        p.accelerate_in_direction([1, 0])
        self.assertTrue(is_position_equal(p, [[0.2, 0], [0.1, 0]]))
        p.accelerate_in_direction([0, 1])
        self.assertTrue(is_position_equal(p, [[0.2, 0.1], [0, 0.1]]))

    def test_bounce_velocity(self):
        p = Creature([[0, 0], [0, 0]], 1, 0.1)
        p.accelerate_in_direction([-1, 0])
        self.assertTrue(is_position_equal(p, [[0.1, 0], [-0.1, 0]]))

    def test_bounce_accel(self):
        p = Creature([[0, 0], [0, 0], [0, 0]], 1, 0.1, 0, [1.0, 1.0, 1.0])
        p.accelerate_in_direction([-1, 0])
        self.assertTrue(is_position_equal(p, [[0.1, 0], [0.1, 0], [-0.1, 0]]))


if __name__ == '__main__':
    unittest.main()
