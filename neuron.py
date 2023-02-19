import pygame
import sys
import random

# Define constants
WINDOW_SIZE = (800, 600)
NUM_NEURONS = 25
INITIAL_PROBABILITY = 0.1
MAX_CONNECTION_STRENGTH = 1.0
MIN_CONNECTION_STRENGTH = 0.0
CONNECTION_STRENGTH_DELTA = 0.1
PROBABILITY_THRESHOLD = 0.5
PROBABILITY_INCREASE = 0.1
PROBABILITY_DECREASE = 0.05


def update_probabilities(
    neurons, connections, threshold=0.5, increase=0.1, decrease=0.05
):
    """
    Update the probabilities of neurons being activated based on the activity of their neighbors.
    If the average activity level of a neuron's neighbors is above the threshold, its probability of
    being activated is increased by the increase amount. If it is below the threshold, its probability
    is decreased by the decrease amount.
    """
    # Compute the activity level of each neuron
    activity_levels = [
        sum(
            [connections[i][j] * neurons[j]["probability"] for j in range(len(neurons))]
        )
        for i in range(len(neurons))
    ]

    # Compute the average activity level of each neuron's neighbors
    neighbor_activity_levels = [
        sum(
            [
                connections[i][j] * activity_levels[j]
                for j in range(len(neurons))
                if j != i
            ]
        )
        / (len(neurons) - 1)
        for i in range(len(neurons))
    ]

    # Update the probabilities of each neuron being activated
    for i in range(len(neurons)):
        if neighbor_activity_levels[i] > threshold:
            neurons[i]["probability"] += increase
        else:
            neurons[i]["probability"] -= decrease

        # Ensure the probability stays within the valid range
        neurons[i]["probability"] = max(0, min(1, neurons[i]["probability"]))


def mutate_connections(connections, mutation_rate=0.1, mutation_size=0.1):
    """
    Mutate the connection strengths between neurons.
    With probability mutation_rate, each connection is mutated by a factor of mutation_size.
    """
    for i in range(len(connections)):
        for j in range(len(connections)):
            if random.uniform(0, 1) < mutation_rate:
                connections[i][j] *= random.uniform(
                    1 - mutation_size, 1 + mutation_size
                )
                connections[i][j] = max(0, min(1, connections[i][j]))


def apply_external_input(neurons, strength=0.1, rate=0.1):
    """
    Apply external input to a random subset of neurons.
    Each neuron in the subset has its probability of being activated increased by strength,
    with probability rate.
    """
    subset = random.sample(neurons, int(len(neurons) * rate))
    for neuron in subset:
        neuron["probability"] = min(1, neuron["probability"] + strength)


def apply_feedback(neurons, connections, feedback_strength=0.1):
    """
    Apply feedback to the network by updating the connection strengths between neurons.
    For each neuron in the network, its feedback weight is calculated as the sum of the
    connection strengths from all other neurons to that neuron, multiplied by the feedback_strength.
    The connection strengths are then updated by adding the feedback weight to each connection.
    """
    for i in range(len(neurons)):
        feedback_weight = (
            sum([connections[j][i] for j in range(len(neurons)) if j != i])
            * feedback_strength
        )
        for j in range(len(neurons)):
            connections[j][i] += feedback_weight
            connections[j][i] = max(0, min(1, connections[j][i]))


def apply_inhibition(
    neurons, connections, inhibition_strength=0.1, inhibition_rate=0.1
):
    """
    Apply global inhibition to the network by reducing the probabilities of all neurons.
    A random subset of neurons is chosen, with size proportional to inhibition_rate.
    The probabilities of these neurons are reduced by inhibition_strength.
    The connection strengths from these neurons to all other neurons are also reduced by a factor of 0.5.
    """
    subset = random.sample(neurons, int(len(neurons) * inhibition_rate))
    for neuron in subset:
        neuron["probability"] = max(0, neuron["probability"] - inhibition_strength)
        for i in range(len(neurons)):
            connections[neurons.index(neuron)][i] *= 0.5
            connections[neurons.index(neuron)][i] = max(
                0, min(1, connections[neurons.index(neuron)][i])
            )


def apply_synaptic_plasticity(
    neurons, connections, window=10, threshold=0.1, factor=0.1
):
    """
    Apply synaptic plasticity to the network by updating the connection strengths between neurons.
    For each neuron in the network, a sliding window of the last `window` activations is computed.
    If the fraction of activations that were positive is above the `threshold`, the connection strengths
    from that neuron to all other neurons are increased by a factor of `factor`.
    If the fraction of activations that were negative is above the `threshold`, the connection strengths
    from that neuron to all other neurons are decreased by a factor of `factor`.
    """
    for i in range(len(neurons)):
        window_start = max(0, i - window)
        window_end = min(len(neurons), i + window + 1)
        window_activities = [
            neurons[j]["probability"] > 0.5 for j in range(window_start, window_end)
        ]
        positive_fraction = sum(window_activities) / len(window_activities)
        negative_fraction = 1 - positive_fraction
        for j in range(len(neurons)):
            if positive_fraction > threshold:
                connections[i][j] *= 1 + factor
                connections[i][j] = max(0, min(1, connections[i][j]))
            elif negative_fraction > threshold:
                connections[i][j] *= 1 - factor
                connections[i][j] = max(0, min(1, connections[i][j]))


def apply_learning(neurons, connections, learning_rate=0.1):
    """
    Apply Hebbian learning to the network by updating the connection strengths between neurons.
    For each pair of neurons that are activated together, the connection strength between them is
    increased by a factor of `learning_rate`. The connection strengths are clipped to the range [0, 1].
    """
    for i in range(len(neurons)):
        for j in range(len(neurons)):
            if (
                i != j
                and neurons[i]["probability"] > 0.5
                and neurons[j]["probability"] > 0.5
            ):
                connections[i][j] += learning_rate
                connections[i][j] = max(0, min(1, connections[i][j]))


def apply_modulatory_signals(
    neurons, connections, modulatory_strength=0.1, modulatory_rate=0.1
):
    """
    Apply modulatory signals to the network by updating the connection strengths between neurons.
    A random subset of neurons is chosen, with size proportional to modulatory_rate.
    For each neuron in the subset, the connection strengths from that neuron to all other neurons
    are increased or decreased by a random amount in the range [-modulatory_strength, modulatory_strength].
    """
    subset = random.sample(neurons, int(len(neurons) * modulatory_rate))
    for neuron in subset:
        for i in range(len(neurons)):
            connections[neurons.index(neuron)][i] += random.uniform(
                -modulatory_strength, modulatory_strength
            )
            connections[neurons.index(neuron)][i] = max(
                0, min(1, connections[neurons.index(neuron)][i])
            )


def apply_homeostasis(neurons, target_prob=0.1, homeostasis_rate=0.1):
    """
    Apply homeostasis to the network by adjusting the probabilities of neurons based on their activity.
    For each neuron, its probability of activation is increased or decreased by a factor proportional
    to the difference between its current activity and the target activity. The adjustment factor is
    determined by the homeostasis rate parameter.
    """
    for neuron in neurons:
        delta_prob = (target_prob - neuron["probability"]) * homeostasis_rate
        neuron["probability"] = max(0, min(1, neuron["probability"] + delta_prob))


def apply_refractory_period(neurons, refractory_period=10):
    """
    Apply a refractory period to the network by temporarily decreasing the probability of activated neurons.
    For each neuron, if its probability of activation is above 0.5, it is considered activated, and its probability
    is set to 0.0 for the next `refractory_period` time steps.
    """
    for neuron in neurons:
        if neuron["probability"] > 0.5:
            neuron["probability"] = 0.0
            neuron["refractory"] = refractory_period
        elif "refractory" in neuron and neuron["refractory"] > 0:
            neuron["refractory"] -= 1


def apply_noise(neurons, noise_strength=0.05, noise_rate=0.1):
    """
    Apply noise to the network by randomly changing the probability of a subset of neurons.
    A random subset of neurons is chosen, with size proportional to noise_rate.
    For each neuron in the subset, its probability is increased or decreased by a random amount
    in the range [-noise_strength, noise_strength].
    """
    subset = random.sample(neurons, int(len(neurons) * noise_rate))
    for neuron in subset:
        neuron["probability"] += random.uniform(-noise_strength, noise_strength)
        neuron["probability"] = max(0, min(1, neuron["probability"]))


def draw_background(screen, color1=(30, 30, 30), color2=(50, 50, 50), size=50):
    """
    Draw a checkerboard pattern with a gradient as the background of the screen.
    The pattern alternates between two colors, and each square has size `size` pixels.
    """
    for x in range(0, screen.get_width(), size):
        for y in range(0, screen.get_height(), size):
            rect = pygame.Rect(x, y, size, size)
            color = [0, 0, 0]
            for i in range(3):
                color[i] = int(
                    color1[i] * (1 - x / screen.get_width())
                    + color2[i] * (x / screen.get_width())
                )
            if (x // size + y // size) % 2 == 0:
                pygame.draw.rect(screen, color, rect)
            else:
                pygame.draw.rect(screen, color[::-1], rect)


def draw_activation_effect(screen, neurons):
    """
    Draw a visual effect around activated neurons.
    For each neuron that is currently activated, draw a circle with a gradient effect that
    fades out towards the edge.
    """
    for neuron in neurons:
        if neuron["probability"] > 0.5:
            # Determine the size of the circle based on the neuron's activation probability
            size = int(neuron["probability"] * 20)

            # Create a surface with a radial gradient
            circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            alpha_values = [
                min(255, int((1 - (float(i) / size)) * 255)) for i in range(size + 1)
            ]
            for i in range(size + 1):
                pygame.draw.circle(
                    circle_surface,
                    (255, 255, 0, alpha_values[i]),
                    (size, size),
                    size - i,
                )

            # Draw the circle on the screen
            screen.blit(circle_surface, (neuron["x"] - size, neuron["y"] - size))


def draw_connections(screen, neurons, connections):
    """
    Draw the connections between neurons on the screen.
    The color of the lines represents the strength of the connection.
    """
    for i in range(len(neurons)):
        for j in range(len(neurons)):
            if connections[i][j] > 0:
                strength = int(connections[i][j] * 255)
                color = (strength, strength, strength)
                pygame.draw.line(
                    screen,
                    color,
                    (neurons[i]["x"], neurons[i]["y"]),
                    (neurons[j]["x"], neurons[j]["y"]),
                    1,
                )


def draw_sparks(
    screen, spark_color=(255, 255, 0), spark_size=2, num_sparks=10, max_speed=5
):
    """
    Draw random sparks on the screen with random trajectories and velocities.
    """
    for i in range(num_sparks):
        x = random.randint(0, screen.get_width())
        y = random.randint(0, screen.get_height())
        vx = random.uniform(-max_speed, max_speed)
        vy = random.uniform(-max_speed, max_speed)
        pygame.draw.circle(screen, spark_color, (x, y), spark_size)
        # Update the position of the spark based on its velocity
        x += vx
        y += vy
        # Bounce the spark off the edges of the screen
        if x < 0 or x > screen.get_width():
            vx *= -1
        if y < 0 or y > screen.get_height():
            vy *= -1


def draw_neurons(screen, neurons):
    """
    Draw circles to represent the neurons on the screen.
    """
    for neuron in neurons:
        pygame.draw.circle(screen, (255, 255, 0), (neuron["x"], neuron["y"]), 3)


def apply_complexities(neurons, connections):
    """
    Apply various complex effects to the network of neurons and connections.
    """
    mutate_connections(connections)
    apply_external_input(neurons)
    apply_feedback(neurons, connections)
    apply_inhibition(neurons, connections)
    apply_synaptic_plasticity(neurons, connections)
    apply_learning(neurons, connections)
    apply_modulatory_signals(neurons, connections)
    apply_homeostasis(neurons)
    apply_refractory_period(neurons)
    apply_noise(neurons)


def initialize_network():
    # Initialize neurons
    neurons = [
        {
            "x": random.randint(0, WINDOW_SIZE[0]),
            "y": random.randint(0, WINDOW_SIZE[1]),
            "probability": INITIAL_PROBABILITY,
        }
        for _ in range(NUM_NEURONS)
    ]

    # Initialize connections
    connections = [
        [
            random.uniform(MIN_CONNECTION_STRENGTH, MAX_CONNECTION_STRENGTH)
            for _ in range(NUM_NEURONS)
        ]
        for _ in range(NUM_NEURONS)
    ]

    return neurons, connections


def update_network(screen, neurons, connections):
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the background
    screen.fill((255, 255, 255))
    draw_background(screen, color1=(30, 30, 30), color2=(50, 50, 50), size=50)

    # Draw the connections between neurons
    draw_connections(screen, neurons, connections)

    # Update the network
    for i, activating_neuron in enumerate(neurons):
        # Determine the target neuron based on connection strengths
        target_neuron = random.choices(neurons, weights=connections[i])[0]

        # Activate or inhibit the target neuron based on connection strength and probability
        if (
            random.uniform(0, 1)
            < connections[i][neurons.index(target_neuron)]
            * activating_neuron["probability"]
        ):
            color = (0, 0, 0)
            delta = CONNECTION_STRENGTH_DELTA
        elif (
            random.uniform(0, 1)
            < connections[neurons.index(target_neuron)][i]
            * activating_neuron["probability"]
        ):
            color = (255, 0, 0)
            delta = -CONNECTION_STRENGTH_DELTA
        else:
            continue

        # Draw a line between the two neurons, using color based on connection strength
        line_width = int(3 * connections[i][neurons.index(target_neuron)])
        pygame.draw.line(
            screen,
            color,
            (activating_neuron["x"], activating_neuron["y"]),
            (target_neuron["x"], target_neuron["y"]),
            line_width,
        )

        # Update the connection strength between the neurons
        connections[i][neurons.index(target_neuron)] += delta

    # Update neuron probabilities and apply complexities
    update_probabilities(
        neurons,
        connections,
        threshold=PROBABILITY_THRESHOLD,
        increase=PROBABILITY_INCREASE,
        decrease=PROBABILITY_DECREASE,
    )
    apply_complexities(neurons, connections)

    # Draw the neurons and activation effect
    draw_neurons(screen, neurons)
    draw_activation_effect(screen, neurons)

    # Draw some sparks
    draw_sparks(screen)

    # Update the screen
    pygame.display.flip()


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Initialize the network
    neurons, connections = initialize_network()

    # Main loop of the game
    while True:
        update_network(screen, neurons, connections)


if __name__ == "__main__":
    main()
