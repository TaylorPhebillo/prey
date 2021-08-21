# Cats chasing Mice
This project simulates dumb cats chasing configurable mice around a 2d box.

Cats will always chase the nearest mouse. Mice behaviors are configurable at the start of the simulation, and can respond to their individual position and the position of the nearest cat. The simulation returns the lifetime of the longest lived mouse, and can optionally log or plot the simulated results.
## Why?
This simulation is a fun opportunity for optimization. The mice behaviors are configured by a floating point vector, which can be optimized by any gradiant-free method. The behavior vectors are small and simple enough that optimization should be easy without being trivial, and the simulation is complex enough for interesting emergent behaviors. For example, see the mice (red) completely ignore the cats (white), in order to run the cats in circles and survive for a long time.

![Circles](circle.gif)

## Use
Run `python3 multi_sim.py` to simulate 1000 random behaviors with random inputs, saving the visualiations in the current directory. 

`python3 special_results.py` will simulate and visualize a couple of hard-coded behaviors that should be a little more interesting than pure random.

Physical simulation parameters, and the number of cats and mice, are not currently configurable.
