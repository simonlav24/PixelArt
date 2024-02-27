from typing import Tuple, Any
import pygame
import gui

class Rectangle(gui.Element):
    def __init__(self, color):
        super().__init__()
        self.color = color
    
    def update_color(self, color):
        self.color = color

    def initialize(self):
        self.size = (100,100)

    def draw(self):
        super().draw()
        pygame.draw.rect(self.gui.win, self.color, (self.pos, self.size))

class ColorPicker(gui.ElementComposition):
    def __init__(self, key: str, color=(127, 127, 127)):
        self.key = key
        self.r_key = f'{self.key}_r'
        self.g_key = f'{self.key}_g'
        self.b_key = f'{self.key}_b'
        self.color_rectangle = Rectangle(color)
        sliders_layout = [
            [self.color_rectangle],
            [gui.Text('R', margin=0, width=10) ,gui.Slider(self.r_key, 0, 255, color[0], enable_events=True)],
            [gui.Text('G', margin=0, width=10) ,gui.Slider(self.g_key, 0, 255, color[1], enable_events=True)],
            [gui.Text('B', margin=0, width=10) ,gui.Slider(self.b_key, 0, 255, color[2], enable_events=True)],
        ]
        super().__init__(sliders_layout)

    def get_value(self) -> Tuple[Any, Any]:
        values = {}
        for element in self.elements:
            value = element.get_value()
            if value:
                values[value[0]] = value[1]
        
        return (self.key, (int(values[self.r_key]), int(values[self.g_key]), int(values[self.b_key])))
    
    def notify_event(self, event: str):
        color = self.get_value()[1]
        self.color_rectangle.update_color(color)


if __name__ == '__main__':
    ''' example usage '''
    pygame.init()

    winWidth = 1280
    winHeight = 720
    win = pygame.display.set_mode((winWidth,winHeight))

    ### setup
    
    image = pygame.image.load('output.png')
    
    layout = [
        [gui.Button('press me', key='button1'), gui.Button('me too', key='button2'), gui.CheckBox('toggleMe', key='toggl1')],
        [ColorPicker('rgb_color')]
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
        
        win.fill((37, 37, 37))
        
        gui.step()
        
        event, values = gui.read()
        if event:
            print(event, values)
        
        gui.draw()
        
        
        
        pygame.display.update()