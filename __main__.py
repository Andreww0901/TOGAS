import random
import multiprocessing
import sys
import __utilities__
import __mutations__
import __crossover__
import __algorithms__
import os
from deap import creator, base, tools, algorithms
from qiskit.quantum_info import Statevector
from qiskit_ibm_provider import IBMProvider
from ast import literal_eval
from math import exp

pop_size = int(sys.argv[1])
no_gens = int(sys.argv[2])
if sys.argv[7] == 'True':
    random.seed(2)
no_qb = int(sys.argv[8])
noise = int(sys.argv[10])
t_count = int(sys.argv[11])
ancillae = int(sys.argv[12])
singular = Statevector(literal_eval(sys.argv[9]), dims=tuple(2 for _ in range(no_qb-ancillae)))

if noise:
    provider = IBMProvider()
    avail = [str(bckend.name) for bckend in provider.backends()]
    if 'ibm_lagos' in avail:
        backend = provider.get_backend('ibm_lagos')
    else:
        backend = None
else:
    backend = None

creator.create("FitnessMax", base.Fitness, weights=(1.0, -0.002, -exp(-no_qb)))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("individual", __utilities__.init_setup, creator.Individual, no_qb=no_qb)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", __utilities__.evaluate, no_qb=no_qb, statevector=singular, noise=backend, t_count=t_count, ancillae=ancillae)


def _genetic_algorithm():
    population = toolbox.population(n=2*pop_size)

    initial_fitnesses = toolbox.map(toolbox.evaluate, population)
    for fitness, individual in zip(initial_fitnesses, population):
        individual.fitness.values = fitness

    population = toolbox.select(population, k=pop_size)

    hof = [0, []]
    best_ind = None

    if os.path.exists('./avg_len.txt'):
        os.remove('./avg_len.txt')

    for generation in range(1, no_gens + 1):
        offspring = __algorithms__.modified_varand(population, toolbox, float(sys.argv[3]), float(sys.argv[4]), 2)
        # offspring = algorithms.varAnd(population, toolbox, cxpb=float(sys.argv[3]), mutpb=float(sys.argv[4]))

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population = toolbox.select(offspring, k=pop_size)

        best_fitness = 0
        avg_len = 0
        for individual in population:
            avg_len += len(individual)
            if individual.fitness.values[0] > best_fitness:
                best_fitness, best_ind = individual.fitness.values[0], individual

        if best_ind is not None and best_ind.fitness.values[0] > hof[0]:
            hof[0] = best_ind.fitness.values[0]
            hof[1] = best_ind

        print(f'GEN:{generation}')
        print(f'HOF:{hof}')
        print(f'AVGLEN:{avg_len/len(population)}')
    # print(f'END')


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    match sys.argv[5]:
        case 'TwoPointCX':
            toolbox.register("mate", __crossover__.mod_tp_crossover)
        case 'OnePointCX':
            toolbox.register("mate", __crossover__.mod_op_crossover)
        case 'MessyOnePoint':
            toolbox.register("mate", tools.cxMessyOnePoint)
        case 'UniformCX':
            toolbox.register("mate", tools.cxUniform, indpb=0.5)

    match sys.argv[6]:
        case "selBest":
            toolbox.register("select", tools.selBest)
        case "selTournament":
            toolbox.register("select", tools.selTournament, tournsize=3)
        case "selRoulette":
            toolbox.register("select", tools.selRoulette)
        case "selRandom":
            toolbox.register("select", tools.selRandom)
        case "selWorst":
            toolbox.register("select", tools.selWorst)
        case "selLexicase":
            toolbox.register("select", tools.selLexicase)

    toolbox.register("mutate", __mutations__.mixed_mutation, no_qb=no_qb)
    _genetic_algorithm()
