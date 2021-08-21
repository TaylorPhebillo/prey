# Cats chasing Mice
# Cats chasing Mice
This project simulates dumb cats chasing configurable mice around a 2d box.

Cats will always chase the nearest mouse. Mice behaviors are configurable at the start of the simulation, and can respond to their individual position and the position of the nearest cat. The simulation returns the lifetime of the longest lived mouse, and can optionally log or plot the simulated results.
## Why?
This simulation is a fun opportunity for optimization. The mice behaviors are configured by a floating point vector, which can be optimized by any gradiant-free method. The behavior vectors are small and simple enough that optimization should be easy without being trivial, and the simulation is complex enough for interesting emergent behaviors. For example, see the mice (red) run the cats (white) in circles 

![Circles](circle.gif)
