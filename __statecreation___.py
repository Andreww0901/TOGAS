import math
from math import exp, factorial, sqrt, cos, sin, pi

import numpy
from qiskit.quantum_info import Statevector
from sklearn.preprocessing import normalize
from itertools import product


def poisson(lam, k):
    distri = []
    for x in range(2**k):
        distri.append(((lam**x)*(exp(-lam))/factorial(x)))
    return Statevector(normalize([distri])[0], dims=tuple(2 for _ in range(k)))


def w(no_qb):
    indeces = [2 ** i for i in range(no_qb)]
    sv = [0 for _ in range(2 ** no_qb)]
    for j in indeces:
        sv[j] = (1 / sqrt(no_qb))**2
    return Statevector(normalize([sv])[0], dims=tuple(2 for _ in range(no_qb)))


def qft(no_qb, init):
    N = 2**no_qb
    transformation = []
    for i in range(len(init)):
        summation = 0
        for k in range(N):
            summation += init[k] * complex(cos((2 * pi) * (i * k) / N), sin((2 * pi) * (i * k) / N))
        transformation.append(1/sqrt(N) * summation)
    return Statevector(transformation, dims=tuple(2 for _ in range(no_qb)))

