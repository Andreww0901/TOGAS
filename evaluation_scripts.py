import subprocess as sp
import pandas as pd
import os
import sys
import time
from itertools import product
from __statecreation___ import poisson, w
from qiskit.quantum_info import random_statevector
from ast import literal_eval

no_qbs = range(4, 7)
states = ['Random', 'Poisson', 'W']

if __name__ == "__main__":
    for qb, state in product(no_qbs, states):
        match state:
            case 'Random':
                singular = random_statevector(tuple(2 for _ in range(qb)), seed=2)
            case 'Poisson':
                singular = poisson(((2**int(qb)) / 2), int(qb))
            case 'W':
                singular = w(qb)

        avg_len = 0
        gens, hof_fit_list, hof, t_count, length = [], [], [], [], []
        os.system('clear')
        print(f'\n ~~~ {qb}-Qubit-{state}-State ~~~ \n')

        start_time = time.perf_counter()
        subproc = sp.Popen(
            ['python3', './__main__.py', f'150', f'20000', f'0.5',
             f'0.25', f'MessyOnePoint', f'selBestDuplication', f'False',
             f'{qb}', f'{[x for x in singular.data]}',
             f'0', f'1', f'0', f'0'],
            stdout=sp.PIPE,
            universal_newlines=True)

        while subproc and avg_len <= 2000:
            line = subproc.stdout.readline()
            if line.startswith('GEN:'):
                gens.append(line[4:-1])
            elif line.startswith('HOF:'):
                hof = literal_eval(line[4:-1])
                hof_fit_list.append(hof[0][0])
                tcnt = 0
                for gate in hof[1]:
                    if gate[0] == "TGate":
                        tcnt += 1
                t_count.append(tcnt)
                length.append(len(hof[1]))
            elif line.startswith("AVGLEN:"):
                avg_len = round(float(line[7:-1]), 3)
            elif line.startswith('END'):
                break
            if len(gens) > 0 and len(hof) > 0:
                print(end='\x1b[2K')
                sys.stdout.write(f'\r   Generation: {gens[-1]} - Best Fitness: {hof[0][0]} - TCount: {t_count[-1]} - Best Ind. Length: {length[-1]} - Average Ind. Length: {avg_len}')
                sys.stdout.flush()

        end_time = time.perf_counter() - start_time
        gens.append(end_time)
        hof_fit_list.append(':TIME')
        t_count.append('~~~')
        length.append('~~~')
        data = {'Generation': gens, 'Fitness': hof_fit_list, 'TCount': t_count, 'Length': length}
        data_frame = pd.DataFrame(data)
        if not os.path.exists('./data'):
            os.mkdir('./data')
        data_frame.to_csv(f'./data/{qb}-Qubit-{state}.csv', index=False)
        os.system('clear')
