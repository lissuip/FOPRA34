import cirq
import math
import matplotlib.pyplot as plt
import numpy as np

def ut(q0, w, w0, w1, n, t, num):
    for x in range(num-1):
        yield cirq.rx(2*w1*(t/n)*math.cos(w*x*(t/n))).on(q0)
        yield cirq.rz(-w0*(t/n)).on(q0)
    yield cirq.measure(q0, key='out')

w0 = 25
w1 = 2
w = 25.5
t = 4
n = 80

sim = cirq.Simulator()
p1 = [0]
q0 = cirq.NamedQubit('0')
for num in np.arange(1, 81):
    circuit = cirq.Circuit(ut(q0, w, w0, w1, n, t, num))
    state_sim = sim.run(circuit, repetitions=1000)
    p1.append(state_sim.histogram(key='out')[1]/1000)

t= np.arange(0, 4.05, 0.05)
plt.plot(t, p1)
plt.show()

w0 = 2
w1 = 2
w = 2
t = 4
n = 80

sim = cirq.Simulator()
p1 = [0]
q0 = cirq.NamedQubit('0')
for num in np.arange(1, 81):
    circuit = cirq.Circuit(ut(q0, w, w0, w1, n, t, num))
    state_sim = sim.run(circuit, repetitions=1000)
    p1.append(state_sim.histogram(key='out')[1]/1000)

t= np.arange(0, 4.05, 0.05)
plt.plot(t, p1)
plt.show()