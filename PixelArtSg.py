import pygame
import PySimpleGUI as sg
import subprocess, os, ast

def get_color(color = [127,127,127]):
    
    color = pygame.Color(color[0], color[1], color[2])
    
    sg.ChangeLookAndFeel('Reddit')
    layout = [
        [sg.Graph((100,100), (0,0), (100,100), key='graph')],
        [sg.Slider(range=(0,255), default_value=color[0], orientation='horizontal', enable_events=True, key='r')],
        [sg.Slider(range=(0,255), default_value=color[1], orientation='horizontal', enable_events=True, key='g')],
        [sg.Slider(range=(0,255), default_value=color[2], orientation='horizontal', enable_events=True, key='b')],
        [sg.Slider(range=(0,360), default_value=color.hsla[0], orientation='horizontal', enable_events=True, key='h')],
        [sg.Slider(range=(0,100), default_value=color.hsla[1], orientation='horizontal', enable_events=True, key='s')],
        [sg.Slider(range=(0,100), default_value=color.hsla[2], orientation='horizontal', enable_events=True, key='l')],
    ]

    window = sg.Window('color pick', alpha_channel=.99, default_element_size=(40, 1), element_justification='c').Layout(layout)
    window.Finalize()
    graph = window['graph']
    
    color_hex = f'#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}'
    graph.draw_rectangle((0,0), (100,100), fill_color=color_hex)
    
    color = [color[0], color[1], color[2]]
    
    while True:
        event, values = window.Read()
        if event in ['r', 'g', 'b']:
            color = pygame.Color(int(values['r']), int(values['g']), int(values['b']))
            window['h'].update(color.hsla[0])
            window['s'].update(color.hsla[1])
            window['l'].update(color.hsla[2])
        if event in ['h', 's', 'l']:
            color = pygame.Color(0,0,0)
            color.hsla = (int(values['h']), int(values['s']), int(values['l']), 100)
            window['r'].update(color[0])
            window['g'].update(color[1])
            window['b'].update(color[2])
        if values:
            color = pygame.Color(int(values['r']), int(values['g']), int(values['b']))
            color_hex = f'#{int(values["r"]):02x}{int(values["g"]):02x}{int(values["b"]):02x}'
            graph.draw_rectangle((0,0), (100,100), fill_color=color_hex)
        if event in ['Exit', 'ok'] or event is None:
            break

        window.Refresh()
    
    window.close()
    return color

if __name__ == '__main__':
    color = get_color()
    print(color)

