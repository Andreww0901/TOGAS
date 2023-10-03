import PySimpleGUI as PyGUI
import base64
import textwrap

heading_font = ("IBM Plex Mono", 24)
body_font = ("IBM Plex Mono Light", 16)
bckgrnd_col = 'White'
txt_col = 'Black'


def layout():
    return [[PyGUI.Menu([['File', 'Close']])],
            [PyGUI.Push(background_color=bckgrnd_col),
             PyGUI.Text('⚠ ERROR ⚠', background_color=bckgrnd_col, text_color='Red', font=heading_font),
             PyGUI.Push(background_color=bckgrnd_col)],
            [PyGUI.HSeparator(color=txt_col)],
            [PyGUI.Push(background_color=bckgrnd_col),
             PyGUI.Text('', size=(40, None), background_color=bckgrnd_col, text_color=txt_col, font=body_font, key='-ERRMSG-'),
             PyGUI.Push(background_color=bckgrnd_col)],
            [PyGUI.VPush(background_color=bckgrnd_col)],
            [PyGUI.Push(background_color=bckgrnd_col),
             PyGUI.Button('CLOSE', font=body_font, button_color=(bckgrnd_col, '#171717'), border_width=0),
             PyGUI.Push(background_color=bckgrnd_col)]]


def warning_gui(e):
    window = PyGUI.Window('ERROR',
                          layout=layout(),
                          background_color=bckgrnd_col,
                          size=(500, 200),
                          keep_on_top=True,
                          resizable=True,
                          finalize=True,
                          icon=base64.b64encode(
                              open(r'./icon.png', 'rb').read()))

    window['-ERRMSG-'].update(textwrap.fill(e, 40))
    while True:
        event, values = window.read(timeout=1)

        if event == PyGUI.WIN_CLOSED or event == 'Close':
            break

        elif event == 'CLOSE':
            break
    window.close()