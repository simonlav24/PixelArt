'''
pysimplegui like gui manager for pygame
'''

from typing import List, Any, Tuple, Dict
import pygame

GUI_DEBUG_MODE = False

check_box_image = pygame.image.load(r'./Assets/checkbox.png')
check_box_size = (13, 13)
check_box_areas = [((check_box_size[0] * i, 0), check_box_size) for i in range(4)]

def point_in_rect(pos, rect):
    rect_pos = rect[0]
    rect_size = rect[1]
    return pos[0] > rect_pos[0] and pos[0] < rect_pos[0] + rect_size[0] and\
            pos[1] > rect_pos[1] and pos[1] < rect_pos[1] + rect_size[1]

class ColorPallete:
    def __init__(self):
        self.text_color = (213,213,213)
        self.button_back_color = (93,93,93)
        self.button_focus_back_color = (106,106,106)
        self.button_toggle_back_color = (60,60,70)
        self.button_slider_color = (0,117,255)
        self.button_slider_color2 = (75,160,255)

class Gui:
    def __init__(self, win, layout, pos=(0,0), min_element_height=16, margin=3, inner_element_margin=6, font=None):
        self.win : pygame.Surface = win
        self.layout : List[List[Element]]= layout
        self.default_font = pygame.font.SysFont('Calibri', 14)
        if font:
            self.default_font = font
        self.color_pallete = ColorPallete()
        
        self.focused_element : Element = None
        self.event : str = None
        
        self.min_element_height = min_element_height
        self.margin = margin
        self.inner_element_margin = inner_element_margin
        
        self.elements : List[Element] = []
        self.dict : Dict[str : Element] = {}
        self.pos = pos
        
        self.calculate()
        
        self.mouse_hold = False

    def set_pos(self, pos):
        self.pos = pos
        self.calculate()
    
    def calculate(self):
        ''' process layout, each element receives gui, position and initializes.
            also calculates self size '''
        pos_y_acc = self.pos[1]
        size_x = 0
        size_y = 0
        
        for row in self.layout:
            pos_x_acc = self.pos[0]
            row_y_max = 0

            size_row_x = 0
            for element in row:
                self.elements.append(element)
                element.set_gui(self)
                if element.key:
                    self.dict[element.key] = element
                element.parent = self
                element.pos = (pos_x_acc, pos_y_acc)
                element.initialize()

                size_row_x += element.size[0] + self.margin

                pos_x_acc += element.size[0] + self.margin
                row_y_max = max(row_y_max, element.size[1])

            size_x = max(size_x, size_row_x)
            
            pos_y_acc += row_y_max + self.margin
            size_y += row_y_max + self.margin

        self.size = (size_x - self.margin, size_y - self.margin)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.focused_element:
                    self.notify_event(self.focused_element.key)
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

        if GUI_DEBUG_MODE:
            pygame.draw.rect(self.win, (255,0,0), (self.pos, self.size), 1)
    
    def read(self):
        if not self.event:
            return None, None
        
        event = self.event
        self.event = None
        values = {'gui': self}
        for element in self.elements:
            returned_values = element.get_values()
            if returned_values:
                for value in returned_values:
                    values[value[0]] = value[1]
        return event, values
    
    def notify_event(self, event):
        ''' elements can notify internal events '''
        self.event = event

    def __getitem__(self, key : str) -> 'Element':
        return self.dict[key]

class Element:
    def __init__(self, margin=None):
        self.pos = (0,0)
        self.size = (0,0)
        self.gui : Gui = None
        self.parent : Element | Gui = None
        self.margin = margin
        self.key = None
    
    def initialize(self):
        ''' initial position is given, calculate self size and other attributes '''
        self.margin = self.margin if self.margin is not None else self.gui.inner_element_margin
    
    def set_gui(self, gui):
        self.gui = gui
        
    def step(self):
        pass
        
    def draw(self):
        if GUI_DEBUG_MODE:
            pygame.draw.rect(self.gui.win, (255,255,0), (self.pos, self.size), 1)
        
    def get_values(self) -> Tuple[Any, Any]:
        ''' return key value '''
        return None
        
    def on_click(self):
        pass
        
    def on_release(self):
        pass
    
    def on_hold(self):
        pass

class Text(Element):
    def __init__(self, text, margin=None, width=None):
        super().__init__(margin)
        self.text = text
        self.initial_width = width if width is not None else 0

    def initialize(self):
        super().initialize()
        bg_color = None
        if GUI_DEBUG_MODE:
            bg_color = (10,10,10)
        self.text_surf = self.gui.default_font.render(self.text, True, self.gui.color_pallete.text_color, bg_color)
        self.size = (max(self.text_surf.get_width() + self.margin * 2, self.initial_width), max(self.text_surf.get_height() + self.margin * 2, self.gui.min_element_height))

    def draw(self):
        super().draw()
        pos = self.pos
        self.gui.win.blit(self.text_surf, (self.pos[0] + self.size[0] / 2 - self.text_surf.get_width() / 2, self.pos[1] + self.size[1] / 2 - self.text_surf.get_height() / 2))

class Button(Element):
    def __init__(self, text, key, margin=None):
        super().__init__(margin)
        self.key = key
        self.text = text
        
    def initialize(self):
        super().initialize()
        self.text_surf = self.gui.default_font.render(self.text, True, self.gui.color_pallete.text_color)
        self.size = (self.text_surf.get_width() + self.margin * 2, max(self.text_surf.get_height() + self.margin * 2, self.gui.min_element_height))

    def step(self):
        super().step()
        if self.gui.mouse_hold:
            return
        mouse_pos = pygame.mouse.get_pos()

        if point_in_rect(mouse_pos, (self.pos, self.size)):
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

class CheckBox(Button):
    def __init__(self, text, key, margin=None):
        super().__init__(text, key, margin)
        self.selected = False
    
    def initialize(self):
        super().initialize()
        self.text_surf = self.gui.default_font.render(self.text, True, self.gui.color_pallete.text_color)
        self.size = (self.text_surf.get_width() + self.margin * 3 + check_box_size[0], max(self.text_surf.get_height() + self.margin * 2, self.gui.min_element_height, check_box_size[1]))

    def get_values(self) -> Tuple[Any, Any]:
        return [(self.key, self.selected)]
        
    def on_click(self):
        self.selected = not self.selected
        self.parent.notify_event(self.key)
    
    def draw(self):
        Element.draw(self)
        pos = self.pos
        focus = self is self.gui.focused_element
        selected = self.selected

        if not selected and not focus:
            area = check_box_areas[0]
        if not selected and focus:
            area = check_box_areas[1]
        if selected and not focus:
            area = check_box_areas[2]
        if selected and focus:
            area = check_box_areas[3]

        self.gui.win.blit(check_box_image, (self.pos[0], self.pos[1] + self.size[1] / 2 - check_box_size[1] / 2), area)
        self.gui.win.blit(self.text_surf, (self.pos[0] + check_box_size[0] + self.margin , self.pos[1] + self.size[1] / 2 - self.text_surf.get_height() / 2))

class ButtonImage(Button):
    def __init__(self, text, key, image_surf=None, image_path=None, margin=None):
        super().__init__(text, key, margin)
        if image_surf:
            self.image_surf_original = image_surf
        elif image_path:
            self.image_surf_original = pygame.image.load(image_path)
    
    def initialize(self):
        super().initialize()
        size_y = max(self.text_surf.get_height() + self.margin * 2, self.gui.min_element_height)
        
        scale_factor = size_y / self.image_surf_original.get_height()
        
        self.image_surf = pygame.transform.smoothscale(self.image_surf_original, (scale_factor * self.image_surf_original.get_width(), scale_factor * self.image_surf_original.get_height()))
        size_x = self.text_surf.get_width() + self.margin * 3 + self.image_surf.get_width()
        self.size = (size_x, size_y)
        
    def draw(self):
        super().draw()
        pos = self.pos
        if self is self.gui.focused_element:
            pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_focus_back_color, (self.pos, self.size))
        else:
            pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_back_color, (self.pos, self.size))
        x = self.pos[0] + self.margin
        self.gui.win.blit(self.image_surf, (x, self.pos[1]))
        x += self.image_surf.get_width() + self.margin
        self.gui.win.blit(self.text_surf, (x, self.pos[1]))

class Slider(Element):
    def __init__(self, key, min_value, max_value, initial_value, width=100, enable_events=False, margin=None):
        super().__init__(margin)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.width = width
        self.key = key
        
        self.margin = 3
        self.enable_events = enable_events
        
    def initialize(self):
        super().initialize()
        self.size = (self.width, self.gui.min_element_height)
        
    def get_values(self) -> Tuple[Any, Any]:
        return [(self.key, self.value)]
        
    def step(self):
        super().step()
        if self.gui.mouse_hold and self is not self.gui.focused_element:
            return 
        mouse_pos = pygame.mouse.get_pos()
        if point_in_rect(mouse_pos, (self.pos, self.size)):
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
        if self.enable_events:
            self.parent.notify_event(self.key)
        
    def draw(self):
        super().draw()
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
        pygame.draw.rect(self.gui.win, self.gui.color_pallete.button_slider_color, ((x, y), (width, height)))
        pygame.draw.line(self.gui.win, self.gui.color_pallete.button_slider_color2, (x + width, y), (x + width, y + height - 1), 2)


class ElementComposition(Element):
    def __init__(self, layout, margin=None):
        super().__init__(margin)
        self.layout : List[List[Element]] = layout
        self.elements : List[Element]= []

    def initialize(self):
        super().initialize()
        self.calculate()

    def calculate(self):
        size_x = 0
        size_y = 0
        pos_y_acc = self.pos[1]
        
        for row in self.layout:
            pos_x_acc = self.pos[0]
            row_y_max = 0
            size_row_x = 0
            for element in row:

                self.elements.append(element)
                element.set_gui(self.gui)
                element.parent = self
                element.pos = (pos_x_acc, pos_y_acc)
                element.initialize()

                size_row_x += element.size[0] + self.gui.margin 

                pos_x_acc += element.size[0] + self.gui.margin
                row_y_max = max(row_y_max, element.size[1])
            size_x = max(size_x, size_row_x)
            
            pos_y_acc += row_y_max + self.gui.margin
            size_y += row_y_max + self.gui.margin
        
        self.size = (size_x - self.gui.margin, size_y - self.gui.margin)
    
    def step(self):
        super().step()
        for element in self.elements:
            element.step()
    
    def draw(self):
        super().draw()
        for element in self.elements:
            element.draw()

    def get_values(self) -> Tuple[Any, Any]:
        values = []
        for element in self.elements:
            returned_values = element.get_values()
            if returned_values:
                values += returned_values
        return values


    def notify_event(self, event : str):
        ''' internal elements can notify the parent of events '''
        pass

class RadioButtonContainer(ElementComposition):
    ''' can hold stateful elements and allows only one to be selected '''
    def notify_event(self, event: str):
        for element in self.elements:
            if element.selected and element.key != event:
                element.selected = False

    

if __name__ == '__main__':
    ''' example usage '''
    pygame.init()

    winWidth = 1280
    winHeight = 720
    win = pygame.display.set_mode((winWidth,winHeight))

    ### setup
    
    image = pygame.image.load('output.png')
    
    layout_comp = [
        [Slider('sliderC1', 0, 100, 50)],
        [Slider('sliderC2', 0, 100, 50)],
        [Slider('sliderC3', 0, 100, 50)],
    ]

    layout = [
        [Button('press me', key='button1'), Button('me too', key='button2'), CheckBox('toggleMe', key='toggl1')],
        [Button('me three', key='button3'), Text('this is text'), ButtonImage('imImage', key='button_image1', image_surf=image)],
        [Slider('slider1', 0, 100, 50), Slider('slider2', 0, 100, 50, enable_events=True), Slider('slider3', 0, 100, 50), Slider('slider4', 0, 100, 50)],
        [ElementComposition(layout_comp), Button('press me', key='button4')],
        [Button('button after last', key='afterlast')]
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
        
        win.fill((37, 37, 37))
        
        gui.step()
        
        event, values = gui.read()
        if event:
            print(event, values)
        
        gui.draw()
        
        
        
        pygame.display.update()