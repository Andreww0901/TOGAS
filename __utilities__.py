import random
from math import pi, sqrt, floor, exp
from cmath import isclose
from qiskit import QuantumCircuit, assemble, Aer, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.fake_provider import FakeVigo
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import state_fidelity, Statevector, random_statevector
from qiskit_aer import AerSimulator
from itertools import product
from numpy.random import poisson
from numpy import abs, vdot
from PIL import Image

universal_set = ["CNOT", "TGate", "TDGGate", "XGate", "SXGate"]


def ind_setup(no_qb):
    gate_choice = random.choice(universal_set)
    if gate_choice != "CNOT" and gate_choice != "TOFGate":
        if gate_choice == "Barrier":
            return [gate_choice]
        elif gate_choice != "PGate":
            return [gate_choice, [random.randint(0, no_qb - 1)]]
        else:
            return [gate_choice, [random.randint(0, no_qb - 1), round(random.uniform(-pi, pi), 4)]]
    else:
        if gate_choice == "CNOT":
            control = random.randint(0, no_qb - 1)
            target = random.choice([i for i in range(0, no_qb) if i not in [control]])
            return [gate_choice, [control, target]]
        else:
            control0 = random.randint(0, no_qb - 1)
            control1 = random.choice([i for i in range(0, no_qb) if i not in [control0]])
            target = random.choice([i for i in range(0, no_qb) if i not in [control0, control1]])
            return [gate_choice, [control0, control1, target]]


def init_setup(container, no_qb):
    return container([ind_setup(no_qb) for _ in range(0, poisson(10))])


def add_gates(circuit, individual):
    for gate in individual:
        match gate[0]:
            case "HGate":
                circuit.h(gate[1])
            case "PGate":
                circuit.rz(gate[1][1], gate[1][0])
            case "TGate":
                circuit.t(gate[1])
            case "TDGGate":
                circuit.tdg(gate[1])
            case "CNOT":
                circuit.cx(gate[1][0], gate[1][1])
            case "TOFGate":
                circuit.ccx(gate[1][0], gate[1][1], gate[1][2])
            case "Barrier":
                circuit.barrier()
            case "XGate":
                circuit.x(gate[1])
            case "ZGate":
                circuit.z(gate[1])
            case "SXGate":
                circuit.sx(gate[1])
    return circuit


def circuit_builder(individual, no_qb, ancillae=0):
    circuit = QuantumCircuit(no_qb, no_qb-ancillae)
    circuit = add_gates(circuit, individual)
    circuit.save_statevector()
    circuit.measure([x for x in range(0, no_qb-ancillae)], [y for y in range(0, no_qb-ancillae)])
    return circuit


def evaluate(individual, no_qb, statevector, t_count, ancillae, noise=None):
    circuit = circuit_builder(individual, no_qb, ancillae)
    if noise:
        simulator = AerSimulator.from_backend(noise)
    else:
        simulator = Aer.get_backend('aer_simulator')
    qobj = transpile(circuit, simulator)
    result = simulator.run(qobj).result().get_statevector()
    result = Statevector(list(result.data)[:2**(no_qb-ancillae)], dims=tuple(2 for _ in range(no_qb-ancillae)))
    if t_count:
        no_tg = 0
        no_cnot = 0
        for x in range(len(individual)):
            if individual[x][0] == 'TGate' or individual[x][0] == 'TDGGate':
                no_tg += 1
            elif individual[x][0] == 'CNOT':
                no_cnot += 1
        return state_fidelity(result, statevector, validate=False) - (no_tg * 0.00001),
    else:
        return state_fidelity(result, statevector, validate=False),


def draw_circuit(individual, no_qb, filename, ancillae):
    circuit = circuit_builder(individual, no_qb, ancillae)
    circuit.draw(output="mpl", filename=f'./circuitDiagrams/{filename}')


def plot_hist(individual, no_qb, filename):
    circuit = circuit_builder(individual, no_qb)
    simulator = Aer.get_backend('aer_simulator')
    job = simulator.run(circuit, shots=10000)
    results = job.result()
    counts = results.get_counts(circuit)
    plot_histogram(counts, filename=f'./circuitDiagrams/{filename}')


def plot_city(individual, no_qb, filename, ancillae, noise=None):
    if isinstance(individual, Statevector):
        individual.draw(output='city', filename=f'./circuitDiagrams/{filename}', title='Desired State', color=['cornflowerblue', 'yellow'])
    elif isinstance(individual, list):
        circuit = circuit_builder(individual, no_qb, ancillae)
        if noise:
            simulator = AerSimulator.from_backend(noise)
        else:
            simulator = Aer.get_backend('aer_simulator')
        qobj = transpile(circuit, simulator)
        result = simulator.run(qobj).result().get_statevector()
        result = Statevector(list(result.data)[:2 ** (no_qb - ancillae)], dims=tuple(2 for _ in range(no_qb - ancillae)))
        result.draw(output='city', filename=f'./circuitDiagrams/{filename}', title='Best Generated State', color=['cornflowerblue', 'yellow'])
    else:
        return


def img_resize(filename, scale):
    img = Image.open(f'{filename}.png')
    imgw, imgh = img.size
    img = img.resize((round(imgw / scale), round(imgh / scale)))
    img.save(f'{filename}_resized.png')


def img_combine(file1, file2):
    img1 = Image.open(f'{file1}.png')
    img2 = Image.open(f'{file2}.png')
    image_size = img1.size
    combined_img = Image.new('RGB', (image_size[0], 2*image_size[1]), (250, 250, 250))
    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2, (0, image_size[1]))
    combined_img.save('./circuitDiagrams/combined_img.png')
