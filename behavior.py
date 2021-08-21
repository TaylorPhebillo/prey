import random


def dot_2d(measured_vector, response):
    assert len(measured_vector) == 2
    assert len(response) == 4
    return [measured_vector[0] * response[0] +
            measured_vector[1] * response[1],
            measured_vector[0] * response[2] +
            measured_vector[1] * response[3]]


def col_sum(*input_components):
    result = [0] * len(input_components[0])
    for component in input_components:
        assert len(component) == len(result)
        for dim in range(len(result)):
            result[dim] += component[dim]
    return result


class Behavior:
    num_responses = 2

    def __init__(self, response=[random.gauss(0, 1) for _ in range(10)]):
        self.programmed_response = response
        # Each component of a 2d response needs to respond to both the x and y
        # component of what it's responding to, so responding to one thing
        # uses 4 numbers (given the naive implementation)
        # The final 2 response components are the +C component- the default
        # drift
        assert len(self.programmed_response) == Behavior.num_responses * 4 + 2

    def react(self, cats, position):
        # Interpret the first two values of the vector as the default drift
        # behavior
        return col_sum(
            self.programmed_response[0:2],
            dot_2d(cats, self.programmed_response[2:6]),
            dot_2d(position, self.programmed_response[6:10]))
