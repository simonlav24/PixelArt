
import pygame
from pygame.math import Vector2
from typing import List

import gui
from layer_data import LayerBase
from EditorViewModel import EditorViewModel
from tools import ToolType

class PixelArtViewportElement(gui.Element):
    ''' the main viewport canvas element of the gui.
        create the interaction events and notifies gui '''
    
    def __init__(self, context: EditorViewModel, **kwargs):
        super().__init__(**kwargs)
        self.context = context

        # adjust size in gui domain
        self.size = Vector2(1000, 600)

        ''' the position and size of the canvas inside the viewport in win domain '''
        self.canvas_size = Vector2(512, 512)
        self.canvas_pos = self.pos + self.size - self.size / 2 - self.canvas_size / 2

    def initialize(self):
        pass
    
    def handle_event(self, event):
        # print(event)
        ''' pygame event handler for viewport '''
        pass

    def get_layers(self) -> List[LayerBase]:
        return self.gui.parent.view_model.layers

    def step(self):
        super().step()
    
    def get_position_in_canvas(self, pos_in_win: Vector2) -> Vector2:
        return pos_in_win - self.pos

    def draw(self):
        win = self.gui.win
        super().draw()
        
        # draw gui size
        pygame.draw.rect(win, (255,255,255), (self.pos, self.size), 1)

        # draw canvas
        pygame.draw.rect(win, (255,255,0), (self.pos + self.canvas_pos, self.canvas_size), 1)

        # draw cursor
        mouse_pos = Vector2(pygame.mouse.get_pos())
        pygame.draw.line(win, (255,255,255), (mouse_pos[0] - 10, mouse_pos[1]), (mouse_pos[0] + 10, mouse_pos[1]))
        pygame.draw.line(win, (255,255,255), (mouse_pos[0], mouse_pos[1] - 10), (mouse_pos[0], mouse_pos[1] + 10))

        # cursor position
        pos_in_canvas = self.get_position_in_canvas(mouse_pos)
        pos_in_canvas_text = self.gui.default_font.render(str(pos_in_canvas), True, (255, 255, 255))
        win.blit(pos_in_canvas_text, mouse_pos + Vector2(10, 10))

        layers = self.context.layers
        for layer in layers:
            win.blit(layer.render(), self.pos + self.canvas_pos + layer.pos)


class PixelArtGui(gui.Gui):
    ''' the entire gui object of the pixel art '''
    def __init__(self, win: pygame.Surface, layout, viewport_element: PixelArtViewportElement, parent, **kwargs):
        super().__init__(win, layout, **kwargs)
        self.viewport_element = viewport_element
        self.parent = parent
    
    def handle_event(self, event):
        self.viewport_element.handle_event(event)
        super().handle_event(event)

class PixelArtView:
    ''' the view object of the pixel art 
        does the gui's step, draw and pygame event handle'''
    def __init__(self, win, context: EditorViewModel):
        self.win = win
        self.context = context

        menu_bar = self.create_menu_bar(context)
        tool_bar = self.create_tool_bar(context)
        self.viewport = self.create_viewport(context)
        self.layer_bar = self.create_layer_bar(context)

        layout = [
            [menu_bar],
            [
                tool_bar, self.viewport
            ],
        ]

        self.view = PixelArtGui(self.win, layout, self.viewport, parent=self)

    def create_menu_bar(self, context: EditorViewModel) -> gui.Element:
        file_menu = [
            [gui.Button('New', 'menu_file_new'),],
            [gui.Button('Open', 'menu_file_open'),],
            [gui.Button('Save', 'menu_file_save'),],
            [gui.Button('Save As', 'menu_file_save_as'),],
            [gui.Button('Export', 'menu_file_export'),],
        ]

        edit_menu = [
            [gui.Button('Undo', 'menu_edit_undo'),],
            [gui.Button('Undo', 'menu_edit_redo'),],
            [gui.Button('Copy', 'menu_edit_copy'),],
            [gui.Button('Paste', 'menu_edit_paste'),],
        ]

        more_menu = [
            [gui.Button('About', 'menu_more_about'),],
        ]

        menu_bar = gui.ElementComposition([
            [
                gui.ContextMenuButton('File', file_menu),
                gui.ContextMenuButton('Edit', edit_menu),
                gui.ContextMenuButton('More', more_menu),
            ]
        ])

        return menu_bar

    def create_tool_bar(self, context: EditorViewModel) -> gui.Element:
        tool_bar = gui.RadioButtonContainer([
            [gui.ButtonToggleContainer('tool_move',   [[gui.Surf(pygame.image.load(r'./Assets/move.png'),      0.08, smooth=True)]], selected=True)],
            [gui.ButtonToggleContainer('tool_select', [[gui.Surf(pygame.image.load(r'./Assets/selection.png'), 0.08, smooth=True)]])],
            [gui.ButtonToggleContainer('tool_pencil', [[gui.Surf(pygame.image.load(r'./Assets/pencil.png'),    0.08, smooth=True)]])],
        ])

        return tool_bar

    def create_viewport(self, context: EditorViewModel) -> gui.Element:
        viewport = PixelArtViewportElement(context)
        return viewport

    def create_layer_bar(self, context: EditorViewModel) -> gui.Element:
        return None
    
    def handle_event(self, event):
        ''' pygame event handler for entire gui '''
        self.view.handle_event(event)
        self.context.handle_event(event)

    def step(self):
        self.view.step()
        event, values = self.view.read()
        if event:
            self.context.handle_gui_event(event)

    def draw(self, win: pygame.Surface):
        self.view.draw()
        self.context.draw(win)

    def update_layers(self):
        ''' update the layer bar '''
        layers = self.context.layers
        for layer in layers:
            self.viewport.canvas_size = (max(self.viewport.canvas_size[0], layer.surf.get_width()), max(self.viewport.canvas_size[1], layer.surf.get_height()))
        


if __name__ == "__main__":
    pygame.init()

    winWidth = 1280
    winHeight = 720
    win = pygame.display.set_mode((winWidth,winHeight))

    pixel_art_view = PixelArtView(win, None)

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