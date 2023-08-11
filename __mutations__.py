import random
from __utilities__ import ind_setup


def gate_value_change(individual, no_qb):
    if len(individual) > 1:
        gate_index = random.randrange(0, len(individual))
        if individual[gate_index][0] == "PGate":
            if random.random() < 0.1:
                individual[gate_index][1][0] = random.randrange(0, no_qb)
            else:
                individual[gate_index][1][1] = individual[gate_index][1][1] + round(random.uniform(-0.4, 0.4))

        elif individual[gate_index][0] == "CNOT":
            if random.random() < 0.5:
                individual[gate_index][1][0] = random.choice(
                    [i for i in range(0, no_qb) if i not in [individual[gate_index][1][1]]])
            else:
                individual[gate_index][1][1] = random.choice(
                    [i for i in range(0, no_qb) if i not in [individual[gate_index][1][0]]])

        elif individual[gate_index][0] == "TOFGate":
            rand = random.random()
            if rand <= 0.33:
                individual[gate_index][1][0] = random.choice([i for i in range(0, no_qb) if
                                                              i not in [individual[gate_index][1][1],
                                                                        individual[gate_index][1][2]]])
            elif 0.33 < rand <= 0.66:
                individual[gate_index][1][1] = random.choice([i for i in range(0, no_qb) if
                                                              i not in [individual[gate_index][1][0],
                                                                        individual[gate_index][1][2]]])
            else:
                individual[gate_index][1][2] = random.choice([i for i in range(0, no_qb) if
                                                              i not in [individual[gate_index][1][0],
                                                                        individual[gate_index][1][1]]])
        elif individual[gate_index][0] == "Barrier":
            pass
        else:
            individual[gate_index][1][0] = random.randrange(0, no_qb - 1)
    return individual,


def del_gate(individual):
    if len(individual) > 3:
        individual.pop(random.randrange(0, len(individual)))
    return individual,


def add_gate(individual, no_qb):
    if len(individual) < 1:
        individual.append(ind_setup(no_qb))
    else:
        individual.insert(random.randrange(0, len(individual)), ind_setup(no_qb))
    return individual,


def switch(individual, no_qb):
    if len(individual) > 0:
        index = random.randrange(0, len(individual))
        individual.pop(index)
        if len(individual) > 0:
            individual.insert(index, ind_setup(no_qb))
        else:
            individual.append(ind_setup(no_qb))

    return individual,


def optimise(individual):
    x = 0
    while x < len(individual)-1:
        match individual[x][0]:
            case "TGate":
                if individual[x + 1][0] == 'TDGGate' and individual[x + 1][1][0] == individual[x][1][0]:
                    individual.pop(x)
                    individual.pop(x)
            case "TDGGate":
                if individual[x + 1][0] == 'TGate' and individual[x + 1][1][0] == individual[x][1][0]:
                    individual.pop(x)
                    individual.pop(x)
            case "XGate":
                if individual[x + 1][0] == 'XGate' and individual[x + 1][1][0] == individual[x][1][0]:
                    individual.pop(x)
                    individual.pop(x)
            case "CNOT":
                if individual[x + 1][0] == 'CNOT' and individual[x + 1][1][0] == individual[x][1][0] and individual[x + 1][1][1] == individual[x][1][1]:
                    individual.pop(x)
                    individual.pop(x)
        x += 1
    return individual,


def sequence_insertion(individual, no_qb):
    sequence = [ind_setup(no_qb) for _ in range(random.randrange(25))]
    if len(individual) < 1:
        for gate in sequence:
            individual.append(gate)
    else:
        index = random.randrange(0, len(individual))
        sequence.reverse()
        for gate in sequence:
            individual.insert(index, gate)

    return individual,


def sequence_deletion(individual):
    if len(individual) >= 1:
        start = random.randrange(len(individual))
        for _ in range(random.randrange(len(individual)-start)):
            individual.pop(start)
    return individual,


def mixed_mutation(individual, no_qb):
    match random.randrange(0, 7):
        case 0:
            individual, = gate_value_change(individual, no_qb)
        case 1:
            individual, = del_gate(individual)
        case 2:
            individual, = add_gate(individual, no_qb)
        case 3:
            individual, = switch(individual, no_qb)
        case 4:
            individual, = optimise(individual)
        case 5:
            individual, = sequence_insertion(individual, no_qb)
        case 6:
            individual, = sequence_deletion(individual)
    return individual,
