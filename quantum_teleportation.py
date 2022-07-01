import random
import numpy as np
import cirq


def make_quantum_teleportation_circuit(ranX, ranY):
    circuit = cirq.Circuit()
    msg, alice, bob = cirq.LineQubit.range(3)

    # Creates Bell state to be shared between Alice and Bob.
    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])
    # Creates a random state for the Message.
    circuit.append([cirq.X(msg) ** ranX, cirq.Y(msg) ** ranY])
    # Bell measurement of the Message and Alice's entangled qubit.
    circuit.append([cirq.CNOT(msg, alice), cirq.H(msg)])
    # Uses the two classical bits from the Bell measurement to recover the
    # original quantum Message on Bob's entangled qubit.
    circuit.append([cirq.CNOT(alice, bob), cirq.CZ(msg, bob)])

    return circuit

def main():
    ranX = random.random()
    ranY = random.random()
    circuit = make_quantum_teleportation_circuit(ranX, ranY)

    print("Circuit:")
    print(circuit)

    sim = cirq.Simulator()

    # Run a simple simulation that applies the random X and Y gates that
    # create our message.
    q0 = cirq.LineQubit(0)
    message = sim.simulate(cirq.Circuit([cirq.X(q0) ** ranX, cirq.Y(q0) ** ranY]))

    print("\nBloch Sphere of Message After Random X and Y Gates:")
    # Prints the Bloch Sphere of the Message after the X and Y gates.
    expected = cirq.bloch_vector_from_state_vector(message.final_state_vector, 0)
    print(
        "x: ",
        np.around(expected[0], 4),
        "y: ",
        np.around(expected[1], 4),
        "z: ",
        np.around(expected[2], 4),
    )

    # Records the final state of the simulation.
    final_results = sim.simulate(circuit)

    print("\nBloch Sphere of Qubit 2 at Final State:")
    # Prints the Bloch Sphere of Bob's entangled qubit at the final state.
    teleported = cirq.bloch_vector_from_state_vector(final_results.final_state_vector, 2)
    print(
        "x: ",
        np.around(teleported[0], 4),
        "y: ",
        np.around(teleported[1], 4),
        "z: ",
        np.around(teleported[2], 4),
    )
    return expected, teleported

if __name__ == '__main__':
    main()