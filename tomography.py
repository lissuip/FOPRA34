import cirq
import math
import numpy as np



def single_qubit_tomography(sampler, qubit, circuit, repetitions):
    qc_z = cirq.Circuit(circuit, cirq.ops.measure(qubit, key='z'))
    results = sampler.run(qc_z, repetitions=repetitions)
    rho_11 = np.mean(results.measurements['z'])
    rho_00 = 1.0 - rho_11

    qc_x = cirq.Circuit(circuit, cirq.ops.H(qubit), cirq.ops.measure(qubit, key='z'))
    results = sampler.run(qc_x, repetitions=repetitions)
    rho_01_re = -(2*np.mean(results.measurements['z'])-1)/2

    qc_y = cirq.Circuit(circuit, cirq.rz(math.pi/2).on(qubit), cirq.H(qubit), cirq.ops.measure(qubit, key='z'))
    results = sampler.run(qc_y, repetitions=repetitions)
    rho_01_im = (2*np.mean(results.measurements['z'])-1)/2

    rho_01 = rho_01_re + rho_01_im*1j
    rho_10 = np.conj(rho_01)

    rho = np.array([[rho_00, rho_01],
                    [rho_10, rho_11]])

    return rho

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
sampler = cirq.Simulator()
qubit = cirq.NamedQubit('qubit')
qc = cirq.Circuit([cirq.ry(math.pi/4).on(qubit), cirq.rz(math.pi/8).on(qubit)])
repetitions = 10000

print(qc)
print(single_qubit_tomography(sampler, qubit, qc, repetitions))

result = cirq.experiments.single_qubit_state_tomography(sampler, qubit, qc, repetitions)
print(result.data)
