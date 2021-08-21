from behavior import Behavior
from cat_mouse import simulate_cat_mouse
from visualizers import CatMouseVisualizer
# A couple of interesting results we can use to make sure things work


def fun_result():
    """Simulate a saved behavior that seemed fun"""
    vis = CatMouseVisualizer(suffix="manual", limit=1000)
    simulate_cat_mouse(
        3, 50,
        Behavior(
            [1.2932335026451751, -0.6136395570170698, 0.2855665089845411, -
             1.437305314105581, -0.5155442512710706, 0.6109865232330572, -
             1.2412022889309902, 0.17199899428165452, 1.8130341188020964, -
             0.4954604336391439]),
        vis.visualize_locations, vis.complete, seed=74280061)


# A special case of behavior that's programmed to ignore the cats, and move in circles
# dx = y - 0.5 (since x and y range from 0. to 1.)
# dy = 0.5 - x
circle_behavior = Behavior([
    -0.5,  # dx drift
    0.5,  # dy drift
    0, 0, 0, 0,  # 4 entries for responding to nearby cats
    0,  # dx response to x
    1.0,  # dx response to y
    -1.0,  # dy response to x
    0  # dy response to y
])


def circle_result():
    """Simulate a preplanned behavior that works_ok"""
    vis = CatMouseVisualizer(suffix="circle", limit=1000)
    simulate_cat_mouse(
        3, 50, circle_behavior,
        vis.visualize_locations, vis.complete, seed=74280061)


if __name__ == "__main__":
    circle_result()
    fun_result()
