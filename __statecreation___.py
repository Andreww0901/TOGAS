from math import exp, factorial
from qiskit.quantum_info import Statevector
from sklearn.preprocessing import normalize


def poisson(lam, k):
    distri = []
    for x in range(2**k):
        distri.append(((lam**x)*(exp(-lam))/factorial(x)))
    return Statevector(normalize([distri])[0], dims=tuple(2 for _ in range(k)))
