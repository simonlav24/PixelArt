from typing import Tuple, Any
import pygame
import gui

class RGBSliders(gui.ElementComposition):
    def __init__(self, key: str):
        self.key = key
        self.r_key = f'{self.key}_r'
        self.g_key = f'{self.key}_g'
        self.b_key = f'{self.key}_b'
        sliders_layout = [
            [gui.Slider(self.r_key, 0, 255, 127)],
            [gui.Slider(self.g_key, 0, 255, 127)],
            [gui.Slider(self.b_key, 0, 255, 127)],
        ]
        super().__init__(sliders_layout)

    def get_value(self) -> Tuple[Any, Any]:
        values = {}
        for element in self.elements:
            value = element.get_value()
            if value:
                values[value[0]] = value[1]
        
        return (self.key, (int(values[self.r_key]), int(values[self.g_key]), int(values[self.b_key])))


if __name__ == '__main__':
    ''' example usage '''
    pygame.init()

    winWidth = 1280
    winHeight = 720
    win = pygame.display.set_mode((winWidth,winHeight))

    ### setup
    
    image = pygame.image.load('output.png')
    
    layout = [
        [gui.Button('press me', key='button1'), gui.Button('me too', key='button2'), gui.ButtonToggle('toggleMe', key='toggl1')],
        [RGBSliders('rgb_color')]
    ]
    gui = gui.Gui(win, layout, pos=(200, 200), margin=10)
    
    ### main loop

    run = True
    while run:
        for event in pygame.event.get():
            gui.handle_event(event)
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        
        win.fill((100, 100, 100))
        
        gui.step()
        
        event, values = gui.read()
        if event:
            print(event, values)
        
        gui.draw()
        
        
        
        pygame.display.update()