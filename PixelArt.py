import pygame
import argparse

from editor import *
from tools import *
from effects import *

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
    run = True
    while run:
        for event in pygame.event.get():
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
        
        # draw
        editor.draw()
        
        pygame.display.update()

    pygame.quit()