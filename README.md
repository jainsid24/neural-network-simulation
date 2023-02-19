# Neural Network Simulation

![License: MIT](https://img.shields.io/bower/l/bootstrap?style=flat-square)
![Commit Activity](https://img.shields.io/github/last-commit/jainsid24/neural-network-simulation?style=flat-square)
![Repo Size](https://img.shields.io/github/repo-size/jainsid24/neural-network-simulation?style=flat-square)
![Python Version](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Pygame Version](https://img.shields.io/badge/Pygame-2.0.2-red?style=flat-square)
![Random Version](https://img.shields.io/badge/Random-3.9.6-orange?style=flat-square)
![Sys Version](https://img.shields.io/badge/Sys-3.9.6-blue?style=flat-square)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black?style=flat-square)

## Contents

1. [About](#about)
2. [Dependencies](#dependencies)
3. [Running the Code](#running-the-code)
4. [Simulation Parameters](#simulation-parameters)
5. [Code Structure](#code-structure)
6. [Resources](#resources)
7. [Code Documentation](#documentation)
8. [License](#license)
9. [Want to Contribute?](#want-to-contribute)

## About

This code simulates a simple neural network using Pygame library. The network consists of 25 neurons (configurable), each with a probability of being activated. The connection strengths between the neurons are randomly initialized, and they can be strengthened or weakened based on the activation patterns.

![Animated GIF](network.gif)

## Dependencies

The following libraries are required to run this code:

* Pygame
* Random
* Sys

## Running the Code

To run the code, execute the following command in the terminal:

```
python neuron.py
```

This will start the Pygame window and run the simulation.

## Simulation Parameters

The following parameters can be adjusted in the code to change the behavior of the simulation:

- **WINDOW_SIZE**: The size of the game window.
- **NUM_NEURONS**: The number of neurons in the network.
- **INITIAL_PROBABILITY**: The probability of each neuron being activated.
- **MAX_CONNECTION_STRENGTH**: The maximum value for the connection strengths.
- **MIN_CONNECTION_STRENGTH**: The minimum value for the connection strengths.
- **CONNECTION_STRENGTH_DELTA**: The value by which to increase or decrease the connection strength.
- **PROBABILITY_THRESHOLD**: The threshold for updating the neuron probabilities.
- **PROBABILITY_INCREASE**: The value by which to increase the neuron probabilities.
- **PROBABILITY_DECREASE**: The value by which to decrease the neuron probabilities.

## Code Structure

The code is structured into the following functions:

- **draw_background**: Draws a background on the screen.
- **draw_sparks**: Draws random sparks on the screen.
- **draw_connections**: Draws the connections between the neurons on the screen.
- **update_probabilities**: Updates the probabilities of the neurons based on the activation patterns.
- **mutate_connections**: Mutates the connection strengths between the neurons.
- **apply_external_input**: Applies external input to the neurons.
- **apply_feedback**: Applies feedback to the neurons based on their activation patterns.
- **apply_inhibition**: Applies inhibition to the neurons based on their activation patterns.
- **apply_synaptic_plasticity**: Applies synaptic plasticity to the connections between the neurons.
- **apply_learning**: Applies hebbian learning to the connections between the neurons.
- **apply_modulatory_signals**: Applies modulatory signals to the neurons.
- **apply_homeostasis**: Applies homeostasis to the neurons.
- **apply_refractory_period**: Applies a refractory period to the neurons.
- **apply_noise**: Applies noise to the neurons.
- **draw_activation_effect**: Draws the activation effect on the screen.

The `main` function contains the main loop of the game, which handles events, clears the screen, draws the connections, updates the network, and updates the screen.

## Documentation

- [Code Documentation](https://jainsid24.github.io/neural-network-simulation/)

## Resources

- [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [The Brain from Top to Bottom](https://thebrain.mcgill.ca/flash/index_d.html)
- [Neurons and Synapses](https://mind.ilstu.edu/curriculum/neurons_intro/neurons_intro.html)

## License

This code is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Want to Contribute?

Check out `CONTRIBUTING.md`.
