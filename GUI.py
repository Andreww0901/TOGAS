import PySimpleGUI as PyGUI
import subprocess as sp
import os
import base64
import gc
from ast import literal_eval
from __utilities__ import draw_circuit, plot_hist, plot_city, img_resize, img_combine
from qiskit.quantum_info import random_statevector, Statevector
from pandas import DataFrame
from qiskit_ibm_provider import IBMProvider
import matplotlib.pyplot as plt

# IBMProvider.save_account(token="MY_API_TOKEN", overwrite=True)

heading_font = ("IBM Plex Mono", 24)
body_font = ("IBM Plex Mono Light", 16)
bckgrnd_col = 'White'
txt_col = 'Black'

cxList = ['OnePointCX', 'TwoPointCX', 'MessyOnePoint', 'UniformCX']
selList = ['selBest', 'selTournament', 'selRoulette', 'selRandom', 'selWorst', 'selLexicase']

if not os.path.exists('./circuitDiagrams/'):
    os.mkdir('./circuitDiagrams/')

layout = [[PyGUI.Text('Genetic Quantum Circuit Synthesizer For State Preperation', font=heading_font, background_color=bckgrnd_col,
                      text_color=txt_col)],
          [PyGUI.HSeparator(color=txt_col)],
          [PyGUI.Push(background_color=bckgrnd_col)],
          [PyGUI.Text('GENERATION:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Text('', background_color=bckgrnd_col, text_color=txt_col, font=body_font, key='-GEN-'),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Checkbox(":SET SEED", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                          font=body_font, key='-SSEED-', default=True)],
          [PyGUI.Text('BEST FITNESS:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Text('', background_color=bckgrnd_col, text_color=txt_col, font=body_font, key='-BF-'),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Checkbox(":NOISY SIMULATION", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                          font=body_font, key='-SNOISE-', default=False)],
          [PyGUI.Text('POPULATION SIZE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(background_color=bckgrnd_col, text_color=txt_col, font=body_font, default_text="100",
                           border_width=1, key='-POPSIZE-'),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Checkbox(":OPTIMISE T-COUNT", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                          font=body_font, key='-STCOUNT-', default=True)],
          [PyGUI.Text('NO. OF GENERATIONS:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(background_color=bckgrnd_col, text_color=txt_col, font=body_font, default_text="30000",
                           border_width=1, key='-NGENS-'),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Spin([i for i in range(1, 10)], initial_value=3, size=5, key='-NOQB-'),
           PyGUI.Text(':NO. OF QUBITS', background_color=bckgrnd_col, text_color=txt_col, font=body_font)],
          [PyGUI.Text('CROSSOVER PROB.:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(background_color=bckgrnd_col, text_color=txt_col, font=body_font, default_text="0.5",
                           border_width=1, key='-CXPB-'),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Spin([i for i in range(5)], initial_value=1, size=5, key='-NOANCI-'),
           PyGUI.Text(':NO. OF ANCILLAE', background_color=bckgrnd_col, text_color=txt_col, font=body_font)],
          [PyGUI.Text('MUTATION PROB.:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(background_color=bckgrnd_col, text_color=txt_col, font=body_font, default_text="0.5",
                           border_width=1, key='-MUTPB-')],
          [PyGUI.Text('CROSSOVER TYPE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Combo(cxList, size=(35, 20), text_color=txt_col,
                       background_color=bckgrnd_col, font=body_font, readonly=True, default_value='MessyOnePoint',
                       button_background_color=txt_col, button_arrow_color=bckgrnd_col, key='-CX-')],
          [PyGUI.Text('SELECTION TYPE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Combo(selList,
                       size=(35, 20), text_color=txt_col,
                       background_color=bckgrnd_col, font=body_font, readonly=True, default_value='selBest',
                       button_background_color=txt_col, button_arrow_color=bckgrnd_col, key='-SEL-')],
          [PyGUI.Button('START', button_color=(bckgrnd_col, "#1ec74b"), font=body_font, border_width=0),
           PyGUI.Button('STOP', button_color=(bckgrnd_col, "#c91827"), font=body_font, border_width=0),
           PyGUI.Multiline(size=(1000, 1), background_color=bckgrnd_col, text_color=txt_col, font=body_font,
                           key='-LIST-')],
          [PyGUI.HSeparator(color=txt_col)],
          [PyGUI.Push(background_color=bckgrnd_col)],
          [PyGUI.Text('BEST CIRCUIT DESIGN', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Text('STATEVECTOR COMPARISON', background_color=bckgrnd_col, text_color=txt_col, font=body_font)],
          [PyGUI.Image("", key='-CD-'),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Image("", key='-HG-')]]

if __name__ == "__main__":
    window = PyGUI.Window(f'Genetic Quantum Circuit Synthesizer',
                          layout=layout,
                          background_color=bckgrnd_col,
                          resizable=True,
                          finalize=True,
                          icon=base64.b64encode(
                              open(r'./icon.png', 'rb').read()))

    window.Maximize()
    event, values = window.read(timeout=0)

    GA_proc, prev_hof, hof, backend = None, None, None, None
    gen, hof_list, hof_ind = [], [], []
    stop = False
    i = 1

    def sub_process():
        if values['-SNOISE-']:
            provider = IBMProvider()
            avail = [str(bckend.name) for bckend in provider.backends()]
            if 'ibm_lagos' in avail:
                bckend = provider.get_backend('ibm_lagos')
            else:
                bckend = None
        else:
            bckend = None

        if values['-SSEED-']:
            singular = random_statevector(tuple(2 for _ in range(values['-NOQB-'])), seed=2)
        else:
            singular = random_statevector(tuple(2 for _ in range(values['-NOQB-'])))
        plot_city(singular, values['-NOQB-'], "desiredState.png", int(values["-SNOISE-"]))
        print(singular)
        if values['-NOQB-'] <= values['-NOANCI-']:
            return None, None
        else:
            return sp.Popen(
                ['python3', './__main__.py', f'{values["-POPSIZE-"]}', f'{values["-NGENS-"]}', f'{values["-CXPB-"]}',
                 f'{values["-MUTPB-"]}', f'{values["-CX-"]}', f'{values["-SEL-"]}', f'{values["-SSEED-"]}',
                 f'{values["-NOQB-"]+values["-NOANCI-"]}', f'{[x for x in singular.data]}', f'{int(values["-SNOISE-"])}', f'{int(values["-STCOUNT-"])}', f'{int(values["-NOANCI-"])}'],
                stdout=sp.PIPE,
                universal_newlines=True), bckend


    while True:
        event, values = window.read(timeout=1)

        if event == PyGUI.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'START':
            i = 1
            window['-NOQB-'].update(readonly=True)
            window['-NOANCI-'].update(readonly=True)
            window['-NOQB-'].update(disabled=True)
            window['-NOANCI-'].update(disabled=True)
            window['-SSEED-'].update(disabled=True)
            window['-SNOISE-'].update(disabled=True)
            window['-STCOUNT-'].update(disabled=True)
            if GA_proc is not None:
                GA_proc.terminate()
            GA_proc, backend = sub_process()

        elif event == 'STOP' and GA_proc is not None:
            window['-NOQB-'].update(readonly=False)
            window['-NOANCI-'].update(readonly=False)
            window['-NOQB-'].update(disabled=False)
            window['-NOANCI-'].update(disabled=False)
            window['-SSEED-'].update(disabled=False)
            window['-SNOISE-'].update(disabled=False)
            window['-STCOUNT-'].update(disabled=False)
            GA_proc.terminate()
            GA_proc = None

        if GA_proc is not None:
            line = GA_proc.stdout.readline()
            if line.startswith("SV:"):
                print(line)

            elif line.startswith("GEN:"):
                window['-GEN-'].update(f'{line[4:-1]}/{values["-NGENS-"]}')
                gen.append(line[4:-1])

            elif line.startswith("HOF:"):
                hof = literal_eval(line[4:-1])
                hof_list.append(hof[0])
                hof_ind.append(hof[1])
                window['-BF-'].update(f'{hof[0]}')
                if hof[0] >= 100:
                    GA_proc.terminate()
                    GA_proc = None
                    stop = True

            if line.startswith('END') or stop:
                if not os.path.exists(f'./evaluations/selections/{values["-SEL-"]}'):
                    os.mkdir(f'./evaluations/selections/{values["-SEL-"]}')
                df = DataFrame({'Generation': gen, 'HOFFitness': hof_list, 'HOFInd': hof_ind})
                df.to_csv(f'./evaluations/selections/{values["-SEL-"]}/{values["-CXPB-"]}-{values["-MUTPB-"]}-{values["-CX-"]}-{i}.csv',
                          index=False)
                gen.clear()
                hof_ind.clear()
                hof_list.clear()
                stop = False
                if i < 1:
                    i += 1
                    GA_proc = sub_process()

        if prev_hof != hof:
            draw_circuit(hof[1], values['-NOQB-']+values['-NOANCI-'], "hof_Diagram.png", values['-NOANCI-'])
            plot_city(hof[1], values['-NOQB-']+values['-NOANCI-'], "hof_City.png", values['-NOANCI-'], backend)
            img_resize("./circuitDiagrams/hof_Diagram", 4)
            img_combine("./circuitDiagrams/desiredState", "./circuitDiagrams/hof_City")
            img_resize("./circuitDiagrams/combined_img", 2)
            window['-CD-'].update(filename="./circuitDiagrams/hof_Diagram_resized.png")
            window['-HG-'].update(filename="./circuitDiagrams/combined_img_resized.png")
            window['-LIST-'].update(hof[1])
            gc.collect()

        prev_hof = hof

    window.close()
