'''
pysimplegui like gui manager for pygame
'''

import pygame

class ColorPallete:
    def __init__(self):
        self.text_color = (255,255,255)
        self.button_back_color = (10,10,20)
        self.button_focus_back_color = (80,80,90)
        self.button_toggle_back_color = (60,60,70)
        self.button_element_color = (100,100,70)

class Gui:
    def __init__(self, win, layout, pos=(0,0), min_element_height=16, margin=3, inner_element_margin=6, font=None):
        self.win = win
        self.layout = layout
        self.default_font = pygame.font.SysFont('Calibri', 12)
        if font:
            self.default_font = pygame.font.SysFont('Calibri', 12)
        self.color_pallete = ColorPallete()
        
        self.focused_element = None
        self.event = None
        
        self.min_element_height = min_element_height
        self.margin = margin
        self.inner_element_margin = inner_element_margin
        
        self.elements = []
        self.pos = pos
        
        self.calculate()
        
        self.mouse_hold = False

    def set_pos(self, pos):
        self.pos = pos
        self.calculate()
    
    def calculate(self):
        pos_y_acc = self.pos[1]
        
        for row in self.layout:
            pos_x_acc = self.pos[0]
            row_y_max = 0
            for element in row:
                self.elements.append(element)
                element.set_gui(self)
                element.pos = (pos_x_acc, pos_y_acc)
                element.initialize()
                pos_x_acc += element.size[0] + self.margin
                row_y_max = max(row_y_max, element.size[1])
            
            pos_y_acc += row_y_max + self.margin
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.focused_element:
                    self.event = self.focused_element.key
                    self.focused_element.on_click()
                self.mouse_hold = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_hold = True
        
        if self.focused_element:
            # send event of mouse held
            if self.mouse_hold:
                self.focused_element.on_hold()
            
    
    def step(self): 
        if not self.mouse_hold:
            self.focused_element = None
        for element in self.elements:
            element.step()
        
    def draw(self):
        for element in self.elements:
            element.draw()
    
    def read(self):
        if not self.event:
            return None, None
        
        event = self.event
        self.event = None
        values = {}
        for element in self.elements:
            value = element.get_value()
            if value:
                values[value[0]] = value[1]
        return event, values

class Element:
    def __init__(self):
        self.pos = (0,0)
        self.size = (0,0)
        self.gui = None
    
    def initialize(self):
        pass
    
    def set_gui(self, gui):
        self.gui = gui
        
    def step(self):
        pass
        
    def draw(self):
        pass
        
    def get_value(self):
        return None
        
    def on_click(self):
        pass
        
    def on_release(self):
        pass
    
    def on_hold(self):
        pass

class Text(Element):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def initialize(self):
        self.text_surf = self.gui.default_font.render(self.text, True, self.gui.color_pallete.text_color)
        self.size = (self.text_surf.get_width() + self.gui.inner_element_margin * 2, max(self.text_surf.get_height() + self.gui.inner_element_margin * 2, self.gui.min_element_height))

    def draw(self):
        super().draw()
        pos = self.pos
        self.gui.win.blit(self.text_surf, (self.pos[0] + self.size[0] / 2 - self.text_surf.get_width() / 2, self.pos[1] + self.size[1] / 2 - self.text_surf.get_height() / 2))

class Button(Element):
    def __init__(self, text, key):
        super().__init__()
        self.key = key
        self.text = text
        
    def initialize(self):
        super().initialize()
        self.text_surf = self.gui.default_font.render(self.text, True, self.gui.color_pallete.text_color)
        self.size = (self.text_surf.get_width() + self.gui.inner_element_margin * 2, max(self.text_surf.get_height() + self.gui.inner_element_margin * 2, self.gui.min_element_height))

    def step(self):
        super().step()
        if self.gui.mouse_hold:
            return
        mouse_pos = pygame.mouse.get_pos()
        pos = self.pos
        if (
            mouse_pos[0] > pos[0]
            and mouse_pos[0] < pos[0] + self.size[0]
            and mouse_pos[1] > pos[1]
            and mouse_pos[1] < pos[1] + self.size[1]
        ):
            self.gui.focused_element = self

    def draw(self):
        super().draw()
        pos = self.pos
        if self is self.gui.focused_element:
            color = self.gui.color_pallete.button_focus_back_color
        else:
            color = self.gui.color_pallete.button_back_color
        pygame.draw.rect(self.gui.win, color, (self.pos, self.size))
        self.gui.win.blit(self.text_surf, (self.pos[0] + self.size[0] / 2 - self.text_surf.get_width() / 2, self.pos[1] + self.size[1] / 2 - self.text_surf.get_height() / 2))

class ButtonToggle(Button):
    def __init__(self, text, key):
        super().__init__(text, key)
        self.selected = False
    
    def get_value(self):
        return (self.key, self.selected)
        
    def on_click(self):
        self.selected = not self.selected
        
    def draw(self):
        super().draw()
        pos = self.pos
        if self is self.gui.focused_element:
            pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_focus_back_color, (self.pos, self.size))
        elif not self.selected:
            pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_back_color, (self.pos, self.size))
        else:
            pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_toggle_back_color, (self.pos, self.size))
        self.gui.win.blit(self.text_surf, (self.pos[0] + self.size[0] / 2 - self.text_surf.get_width() / 2, self.pos[1] + self.size[1] / 2 - self.text_surf.get_height() / 2))

class ButtonImage(Button):
    def __init__(self, text, key, image_surf):
        super().__init__(text, key)
        self.image_surf_original = image_surf
    
    def initialize(self):
        super().initialize()
        size_y = max(self.text_surf.get_height() + self.gui.inner_element_margin * 2, self.gui.min_element_height)
        
        scale_factor = size_y / self.image_surf_original.get_height()
        
        self.image_surf = pygame.transform.smoothscale(self.image_surf_original, (scale_factor * self.image_surf_original.get_width(), scale_factor * self.image_surf_original.get_height()))
        size_x = self.text_surf.get_width() + self.gui.inner_element_margin * 3 + self.image_surf.get_width()
        self.size = (size_x, size_y)
        
    def draw(self):
        pos = self.pos
        if self is self.gui.focused_element:
            pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_focus_back_color, (self.pos, self.size))
        else:
            pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_back_color, (self.pos, self.size))
        x = self.pos[0] + self.gui.inner_element_margin
        self.gui.win.blit(self.image_surf, (x, self.pos[1]))
        x += self.image_surf.get_width() + self.gui.inner_element_margin
        self.gui.win.blit(self.text_surf, (x, self.pos[1]))

class Slider(Element):
    def __init__(self, key, min_value, max_value, initial_value, width=100):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.width = width
        self.key = key
        
        self.margin = 3
        
    def initialize(self):
        super().initialize()
        self.size = (self.width, self.gui.min_element_height)
        
    def get_value(self):
        return (self.key, self.value)
        
    def step(self):
        super().step()
        if self.gui.mouse_hold and self is not self.gui.focused_element:
            return 
        mouse_pos = pygame.mouse.get_pos()
        pos = self.pos
        if (
            mouse_pos[0] > pos[0]
            and mouse_pos[0] < pos[0] + self.size[0]
            and mouse_pos[1] > pos[1]
            and mouse_pos[1] < pos[1] + self.size[1]
        ):
            self.gui.focused_element = self

    def on_hold(self):
        if self is not self.gui.focused_element:
            return 
        
        x = self.pos[0] + self.margin
        width = self.size[0] - 2 * self.margin
        mouse_pos = pygame.mouse.get_pos()
        
        value = (mouse_pos[0] - x) / width
        
        # clamp
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
        
        self.value = (self.max_value - self.min_value) * value
        
    def draw(self):
        if self is self.gui.focused_element:
            color = self.gui.color_pallete.button_focus_back_color
        else:
            color = self.gui.color_pallete.button_back_color
        pygame.draw.rect(self.gui.win, color, (self.pos, self.size))
        value = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        x = self.pos[0] + self.margin
        y = self.pos[1] + self.margin
        width = (self.size[0] - 2 * self.margin) * value
        height = self.size[1] - 2 * self.margin
        pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_toggle_back_color, ((x, y), (width, height)))
        pygame.draw.line(self.gui.win, self.gui.color_pallete.button_element_color, (x + width, y), (x + width, y + height - 1), 2)
        

if __name__ == '__main__':
    ''' example usage '''
    pygame.init()

    winWidth = 1280
    winHeight = 720
    win = pygame.display.set_mode((winWidth,winHeight))

    ### setup
    
    image = pygame.image.load('output.png')
    
    layout = [
        [Button('press me', key='button1'), Button('me too', key='button2'), ButtonToggle('toggleMe', key='toggl1')],
        [Button('me three', key='button3'), Text('this is text'), ButtonImage('imImage', key='button_image1', image_surf=image)],
        [Slider('slider1', 0, 100, 50), Slider('slider2', 0, 100, 50), Slider('slider3', 0, 100, 50), Slider('slider4', 0, 100, 50)],
    ]
    gui = Gui(win, layout, pos=(200, 200), margin=10)
    
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