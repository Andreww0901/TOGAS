import PySimpleGUI as PyGUI
import subprocess as sp
import os
import base64
import gc
import matplotlib.pyplot as plt
from SettingsGUI import additional_settings
from ast import literal_eval
from __utilities__ import draw_circuit, plot_hist, plot_city, img_resize, img_combine, visualise
from __statecreation___ import poisson, w
from qiskit.quantum_info import random_statevector, Statevector
from pandas import DataFrame
from qiskit_ibm_provider import IBMProvider
from matplotlib import rcParams
from PIL import Image

# IBMProvider.save_account(token="MY_API_TOKEN", overwrite=True)

rcParams['font.family'] = 'IBM Plex Mono'
rcParams['font.serif'] = ['IBM Plex Mono Light']
heading_font = ("IBM Plex Mono", 24)
body_font = ("IBM Plex Mono Light", 16)
bckgrnd_col = 'White'
txt_col = 'Black'

cxList = ['OnePointCX', 'TwoPointCX', 'MessyOnePoint', 'UniformCX']
selList = ['selBest', 'selTournament', 'selRoulette', 'selRandom', 'selWorst', 'selLexicase', 'selDoubleTournament']

if not os.path.exists('./circuitDiagrams/'):
    os.mkdir('./circuitDiagrams/')

layout = [[PyGUI.Menu([['File', ['Visualise Solution', 'Exit']], ['Settings', ['Additional Settings']],
                       ['Help', ['General Help', 'About']]])],
          [PyGUI.Text('Genetic Quantum Circuit Synthesizer For State Preperation', font=heading_font,
                      background_color=bckgrnd_col,
                      text_color=txt_col)],
          [PyGUI.HSeparator(color=txt_col)],
          [PyGUI.Push(background_color=bckgrnd_col)],
          [PyGUI.Text('GENERATION:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Text('', background_color=bckgrnd_col, text_color=txt_col, font=body_font, key='-GEN-')],
          [PyGUI.Text('BEST FITNESS:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Text('', background_color=bckgrnd_col, text_color=txt_col, font=body_font, key='-BF-')],
          [PyGUI.Text('POPULATION SIZE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(size=(20, 1), background_color=bckgrnd_col, text_color=txt_col, font=body_font,
                           default_text="100",
                           border_width=1, key='-POPSIZE-'),
           PyGUI.Push(background_color=bckgrnd_col)],
          [PyGUI.Text('NO. OF GENERATIONS:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(size=(17, 1), background_color=bckgrnd_col, text_color=txt_col, font=body_font,
                           default_text="30000",
                           border_width=1, key='-NGENS-')],
          [PyGUI.Text('CROSSOVER PROB.:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(size=(20, 1), background_color=bckgrnd_col, text_color=txt_col, font=body_font,
                           default_text="0.5",
                           border_width=1, key='-CXPB-'),
           PyGUI.Push(background_color=bckgrnd_col)],
          [PyGUI.Text('MUTATION PROB.:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.InputText(size=(21, 1), background_color=bckgrnd_col, text_color=txt_col, font=body_font,
                           default_text="0.5",
                           border_width=1, key='-MUTPB-')],
          [PyGUI.Text('CROSSOVER TYPE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Combo(cxList, size=(20, 1), text_color=txt_col,
                       background_color=bckgrnd_col, font=body_font, readonly=True, default_value='MessyOnePoint',
                       button_background_color=txt_col, button_arrow_color=bckgrnd_col, key='-CX-')],
          [PyGUI.Text('SELECTION TYPE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
           PyGUI.Combo(selList,
                       size=(20, 1), text_color=txt_col,
                       background_color=bckgrnd_col, font=body_font, readonly=True, default_value='selBest',
                       button_background_color=txt_col, button_arrow_color=bckgrnd_col, key='-SEL-'),
           PyGUI.Push(background_color=bckgrnd_col),
           PyGUI.Text('', background_color=bckgrnd_col, text_color=txt_col, font=body_font, key='-AVGLEN-'),
           PyGUI.Text(':AVERAGE SOLUTION LENGTH', background_color=bckgrnd_col, text_color=txt_col, font=body_font)],
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
    no_qb, no_anci, sseed, stcount, noisesim, visualisation, svtype, phase_info = 6, 0, False, True, False, False, 'Poisson', False
    gen, hof_list, hof_ind = [], [], []
    stop = False
    i = 1


    def sub_process():
        if noisesim:
            provider = IBMProvider()
            avail = [str(bckend.name) for bckend in provider.backends()]
            if 'ibm_lagos' in avail:
                bckend = provider.get_backend('ibm_lagos')
            else:
                bckend = None
        else:
            bckend = None

        if svtype == 'Poisson':
            singular = poisson(((2**int(no_qb)) / 2), int(no_qb))
        elif svtype == 'W':
            singular = w(no_qb)
        elif svtype == 'Random':
            if sseed:
                singular = random_statevector(tuple(2 for _ in range(no_qb)), seed=2)
            else:
                singular = random_statevector(tuple(2 for _ in range(no_qb)))
        plot_city(singular, no_qb, "desiredState.png", int(noisesim))
        print(singular)
        if no_qb <= no_anci:
            return None, None
        else:
            return sp.Popen(
                ['python3', './__main__.py', f'{values["-POPSIZE-"]}', f'{values["-NGENS-"]}', f'{values["-CXPB-"]}',
                 f'{values["-MUTPB-"]}', f'{values["-CX-"]}', f'{values["-SEL-"]}', f'{sseed}',
                 f'{no_qb + no_anci}', f'{[x for x in singular.data]}',
                 f'{int(noisesim)}', f'{int(stcount)}', f'{int(no_anci)}', f'{int(phase_info)}'],
                stdout=sp.PIPE,
                universal_newlines=True), bckend


    while True:
        event, values = window.read(timeout=1)

        if event == PyGUI.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'START':
            poisson_ = False
            i = 1
            if GA_proc is not None:
                GA_proc.terminate()
            GA_proc, backend = sub_process()

        elif event == 'STOP' and GA_proc is not None:
            GA_proc.terminate()
            GA_proc = None

        elif event == 'Additional Settings' and GA_proc is None:
            no_qb, no_anci, sseed, stcount, noisesim, visualisation, svtype, phase_info = additional_settings(no_qb, no_anci, sseed, stcount, noisesim, visualisation, svtype, phase_info)

        elif event == 'Visualise Solution' and hof is not None:
            visualise(hof, no_qb, no_anci, backend)
            Image.open('./circuitDiagrams/hof_Diagram.png').show()
            Image.open('./circuitDiagrams/combined_img.png').show()
            Image.open('./circuitDiagrams/hof_Hist.png').show()

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
                if hof[0] >= 100:
                    GA_proc.terminate()
                    GA_proc = None
                    stop = True

            elif line.startswith("AVGLEN:"):
                window['-AVGLEN-'].update(f'{line[7:-1]}')

            if line.startswith('END') or stop:
                if not os.path.exists(f'./evaluations/selections/{values["-SEL-"]}'):
                    os.mkdir(f'./evaluations/selections/{values["-SEL-"]}')
                df = DataFrame({'Generation': gen, 'HOFFitness': hof_list, 'HOFInd': hof_ind})
                df.to_csv(
                    f'./evaluations/selections/{values["-SEL-"]}/{values["-CXPB-"]}-{values["-MUTPB-"]}-{values["-CX-"]}-{i}.csv',
                    index=False)
                gen.clear()
                hof_ind.clear()
                hof_list.clear()
                stop = False
                if i < 1:
                    i += 1
                    GA_proc = sub_process()

        if prev_hof != hof:
            if visualisation:
                visualise(hof, no_qb, no_anci, backend)
                window['-CD-'].update(filename="./circuitDiagrams/hof_Diagram_resized.png")
                if phase_info:
                    window['-HG-'].update(filename="./circuitDiagrams/hof_Hist_resized.png")
                else:
                    window['-HG-'].update(filename="./circuitDiagrams/combined_img_resized.png")
            window['-LIST-'].update(hof[1])
            window['-BF-'].update(f'{hof[0]} - GATE COUNT:{len(hof[1])}')
            gc.collect()

        prev_hof = hof

    window.close()
