
import pygame
from EditorViewModel import *
from View import *

if __name__ == '__main__':
    pygame.init()

    win = pygame.display.set_mode((1280, 720))

    editor_view_model = EditorViewModel()
    pixel_art_view = PixelArtView(win, editor_view_model)
    editor_view_model.set_view(pixel_art_view)

    # setup, create and load default layer
    editor_view_model.load(r'Assets/image.png')

    ### main loop
    run = True
    while run:
        for event in pygame.event.get():
            # editor handle events
            pixel_art_view.handle_event(event)

            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        
        # step
        pixel_art_view.step()
        
        # draw
        win.fill((0,0,0))
        pixel_art_view.draw()
        
        pygame.display.update()

    pygame.quit()