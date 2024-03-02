import pygame
import argparse
import gui
import customGui
from typing import Dict, List

from editor import *
from tools import *
from effects import *


### setup


def handle_tool_bar_events(event, values, editor : Editor):
    if event == 'tool_move':
        editor.switch_tool(TOOL_MOVE)
    elif event == 'tool_select':
        editor.switch_tool(TOOL_RECT_SELECT)
    elif event == 'tool_pencil':
        editor.switch_tool(TOOL_PENCIL)
    elif event == 'change_color':
        ''' click on color rectangle '''
        layout = [[customGui.ColorPicker('color_picker', color=editor.current_color, enable_events=True)]]
        pos = values['gui']['change_color'].pos
        size = values['gui']['change_color'].size
        gui_color = gui.Gui(win, layout, pos=(pos[0] + size[0] + 4, pos[1] + size[1] + 4))
        editor.guis.append(gui_color)
    elif event == 'color_picker':
        ''' color is changed live in the color picker '''
        color = values['color_picker']
        editor.set_color(color)
    elif event == 'color_ok':
        ''' click ok in color picker '''
        editor.guis.remove(values['gui'])
        color = values['color_picker']
        editor.set_color(color)

def parse_arguments():
    parser = argparse.ArgumentParser(description='PixelArt')
    parser.add_argument('initial_file_path', default='', nargs='?')
    return parser.parse_args()

if __name__ == '__main__':

    pygame.init()

    winWidth = 1280
    winHeight = 720
    win = pygame.display.set_mode((winWidth,winHeight))

    args = parse_arguments()

    editor = Editor(win)

    if args.initial_file_path != '':
        image_path = args.initial_file_path
        image = pygame.image.load(image_path)
        editor.load_iamge(image_path)
    else:
        editor.create_new()

    ### main loop

    click_hold = False
    alt_hold = False
    run = True
    while run:
        for event in pygame.event.get():
            # gui handle events
            for g in editor.guis:
                g.handle_event(event)
            # editor handle events
            editor.handle_events(event)

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.DROPFILE:
                editor.load_iamge(event.file)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    pass
                if event.key == pygame.K_h:
                    hue = EffectHue(editor, 10)
                    hue.apply()
                if event.key == pygame.K_v:
                    editor.switch_tool(TOOL_MOVE)
                if event.key == pygame.K_p:
                    editor.switch_tool(TOOL_PENCIL)
                if event.key == pygame.K_s:
                    editor.switch_tool(TOOL_RECT_SELECT)
                if event.key in [pygame.K_LALT, pygame.K_RALT]:
                    editor.switch_tool(TOOL_EYEDROP)
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    editor.viewport.save('output.png')
                    print(f'saved output.png')
                    
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LALT, pygame.K_RALT]:
                    editor.switch_tool_previous()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        
        # step
        editor.step()

        for g in editor.guis:
            g.step()
        for g in editor.guis:
            event, values = g.read()
            if event:
                print('[EVENT]', event, values)
                handle_tool_bar_events(event, values, editor)
        
        # draw
        editor.draw()

        for g in editor.guis:
            g.draw()
        
        pygame.display.update()