import copy
import PySimpleGUI as PyGUI
import base64
import time
from SVGUI import custom_statevector

heading_font = ("IBM Plex Mono", 24)
body_font = ("IBM Plex Mono Light", 16)
bckgrnd_col = 'White'
txt_col = 'Black'

statevectors = ['Random', 'Poisson', 'W', 'QFT', 'Custom']


def layout():
    return [[PyGUI.Menu([['File', 'Close']])],
            [PyGUI.Text('Additional Settings', font=heading_font, text_color=txt_col, background_color=bckgrnd_col)],
            [PyGUI.HSeparator(color=txt_col)],
            [PyGUI.Text('NO. OF QUBITS:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
             PyGUI.Spin([i for i in range(1, 10)], initial_value=3, size=5, key='-NOQB-')],
            [PyGUI.Text('NO. OF ANCILLAE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
             PyGUI.Spin([i for i in range(5)], initial_value=0, size=5, key='-NOANCI-')],
            [PyGUI.Text('SET SEED:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
             PyGUI.Checkbox("", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                            font=body_font,
                            key='-SSEED-', default=False)],
            [PyGUI.Text('OPTIMISE FOR T-COUNT:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
             PyGUI.Checkbox("", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                            font=body_font,
                            key='-STCOUNT-', default=True)],
            [PyGUI.Text('NOISY SIMULATION:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
             PyGUI.Checkbox("", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                            font=body_font,
                            key='-SNOISE-', default=False)],
            [PyGUI.Text('CIRCUIT/STATEVECTOR VISUALISATION:', background_color=bckgrnd_col, text_color=txt_col,
                        font=body_font),
             PyGUI.Checkbox("", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                            font=body_font,
                            key='-VISUA-', default=True)],
            [PyGUI.Text('IGNORE PHASE INFORMATION:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
             PyGUI.Checkbox("", background_color=bckgrnd_col, checkbox_color=txt_col, text_color=txt_col,
                            font=body_font,
                            key='-PHASEINFO-', default=False)],
            [PyGUI.Text('STATEVECTOR TYPE:', background_color=bckgrnd_col, text_color=txt_col, font=body_font),
             PyGUI.Combo(statevectors, size=(15, 1), text_color=txt_col,
                         background_color=bckgrnd_col, font=body_font, readonly=True, default_value='Poisson',
                         button_background_color=txt_col, button_arrow_color=bckgrnd_col, key='-SVSEL-'),
             PyGUI.Button('EDIT', font=body_font, button_color=(bckgrnd_col, '#171717'), border_width=0, visible=False, key='-CUSTOMBUT-')],
            [PyGUI.VPush(background_color=bckgrnd_col)],
            [PyGUI.Button('SAVE & CLOSE', font=body_font, button_color=(bckgrnd_col, '#171717'), border_width=0)]]


def additional_settings(no_qb, no_anci, sseed, stcount, noisesim, visualisation, svtype, cust_sv, phase_info):
    window = PyGUI.Window('Additional Settings',
                          layout=layout(),
                          background_color=bckgrnd_col,
                          size=(450, 360),
                          keep_on_top=True,
                          resizable=True,
                          finalize=True,
                          icon=base64.b64encode(
                              open(r'./icon.png', 'rb').read()))
    window['-NOQB-'].update(no_qb)
    window['-NOANCI-'].update(no_anci)
    window['-SSEED-'].update(sseed)
    window['-STCOUNT-'].update(stcount)
    window['-SNOISE-'].update(noisesim)
    window['-VISUA-'].update(visualisation)
    window['-SVSEL-'].update(svtype)
    window['-PHASEINFO-'].update(phase_info)
    s_c = False
    while True:
        event, values = window.read(timeout=1)

        if event == PyGUI.WIN_CLOSED or event == 'Close':
            break

        elif event == '-CUSTOMBUT-':
            cust_sv = custom_statevector(cust_sv, values['-NOQB-'])

        elif event == 'SAVE & CLOSE':
            s_c = True
            break

        if values['-SVSEL-'] == 'Custom':
            window['-CUSTOMBUT-'].update(visible=True)
        else:
            window['-CUSTOMBUT-'].update(visible=False)

    window.close()
    if s_c:
        return values['-NOQB-'], values['-NOANCI-'], values['-SSEED-'], values['-STCOUNT-'], values['-SNOISE-'], \
            values['-VISUA-'], values['-SVSEL-'], cust_sv, values['-PHASEINFO-']
    else:
        return no_qb, no_anci, sseed, stcount, noisesim, visualisation, svtype, cust_sv, phase_info
