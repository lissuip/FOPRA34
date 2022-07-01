import cirq
import math
import matplotlib.pyplot as plt
import numpy as np


def ut(q0, w, w0, w1, n, t):
    for x in range(79):
        yield cirq.rx(2 * w1 * (t / n) * math.cos(w * x * (t / n))).on(q0)
        yield cirq.rz(-w0 * (t / n)).on(q0)
    yield cirq.measure(q0, key='out')

w0 = 25
w1 = 2
n = 80
t = math.pi/w1
q0 = cirq.NamedQubit('0')
sim = cirq.Simulator()
p1 = []

for w in np.arange(10, 40.1, 0.1):
    circuit = cirq.Circuit(ut(q0, w, w0, w1, n, t))
    state_sim = sim.run(circuit, repetitions=1000)
    p1.append(state_sim.histogram(key='out')[1] / 1000)

print("Population:")
print(p1)
t = np.arange(10, 40.1, 0.1)
plt.plot(t, p1)
plt.show()
