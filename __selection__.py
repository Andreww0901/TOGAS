import random
from operator import attrgetter


def selBestDuplication(population, k, fit_attr="fitness"):
    sorted_pop = sorted(population, key=attrgetter(fit_attr), reverse=True)
    best_ind = sorted_pop[:10]
    [best_ind.append(random.choice(sorted_pop)) for _ in range(0, 10)]
    return best_ind * round(k/20)
