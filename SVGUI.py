import PySimpleGUI as PyGUI
import base64
from qiskit.quantum_info import Statevector

heading_font = ("IBM Plex Mono", 24)
body_font = ("IBM Plex Mono Light", 16)
bckgrnd_col = 'White'
txt_col = 'Black'


def layout():
    return [[PyGUI.Menu([['File', 'Close']])],
            [PyGUI.Text('EDIT STATEVECTOR', font=heading_font, text_color=txt_col,
                        background_color=bckgrnd_col, key='-HEADING-')],
            [PyGUI.HSeparator(color=txt_col)],
            [PyGUI.Multiline(size=(100, 19), background_color=bckgrnd_col, text_color=txt_col, font=body_font,
                             key='-SV-', sbar_frame_color='black', sbar_trough_color='White', sbar_background_color='Black', sbar_arrow_color='White')],
            [PyGUI.VPush(background_color=bckgrnd_col)],
            [PyGUI.Button('SAVE & CLOSE', font=body_font, button_color=(bckgrnd_col, '#171717'), border_width=0)]]


def custom_statevector(cust_sv, no_qb):
    window = PyGUI.Window('Edit Statevector',
                          layout=layout(),
                          background_color=bckgrnd_col,
                          size=(500, 500),
                          keep_on_top=True,
                          resizable=True,
                          finalize=True,
                          icon=base64.b64encode(
                              open(r'./icon.png', 'rb').read()))

    window['-HEADING-'].update(f'EDITING {no_qb} QUBIT STATEVECTOR')
    window['-SV-'].update(cust_sv)
    s_c = False
    while True:
        event, values = window.read(timeout=1)

        if event == PyGUI.WIN_CLOSED or event == 'Close':
            break

        elif event == 'SAVE & CLOSE':
            s_c = True
            break
    window.close()
    if s_c:
        return values['-SV-']
    else:
        return cust_sv
