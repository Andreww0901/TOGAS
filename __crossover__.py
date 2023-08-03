import random


def mod_op_crossover(ind1, ind2):
    if len(ind1) > 2 and len(ind2) > 2:
        min_len = min(len(ind1), len(ind2))
        cxpoint = random.randint(1, min_len - 1)
        ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    return ind1, ind2


def mod_tp_crossover(ind1, ind2):
    if len(ind1) > 2 and len(ind2) > 2:
        min_len = min(len(ind1), len(ind2))
        cxpoint1 = random.randint(1, min_len)
        cxpoint2 = random.randint(1, min_len - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

    return ind1, ind2
