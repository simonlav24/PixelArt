
import pygame
import gui
from typing import List
from layers import Layer

class PixelArtViewportElement(gui.Element):
    ''' the main viewport canvas element of the gui.
        create the interaction events and notifies gui '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (1000, 500)

        ''' the position and size of the canvas inside the viewport '''
        self.canvas_pos = (100, 100)
        self.canvas_size = (0,0)
    
    def handle_event(self, event):
        ''' pygame event handler for viewport '''
        pass

    def get_layers(self) -> List[Layer]:
        return self.gui.parent.view_model.layers

    def step(self):
        super().step()

    def draw(self):
        win = self.gui.win
        super().draw()
        pygame.draw.rect(win, (255,255,255), (self.pos, self.size), 1)
        pygame.draw.rect(win, (255,255,0), ((self.pos[0] + self.canvas_pos[0], self.pos[1] + self.canvas_pos[1]), self.canvas_size), 1)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(win, (255,255,255), (mouse_pos[0] - 10, mouse_pos[1]), (mouse_pos[0] + 10, mouse_pos[1]))
        pygame.draw.line(win, (255,255,255), (mouse_pos[0], mouse_pos[1] - 10), (mouse_pos[0], mouse_pos[1] + 10))

        pos_in_canvas = (mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])
        pos_in_canvas_text = self.gui.default_font.render(str(pos_in_canvas), True, (255, 255, 255))
        win.blit(pos_in_canvas_text, (mouse_pos[0], mouse_pos[1]))

        layers = self.get_layers()
        for layer in layers:
            win.blit(layer.get_surf(), (self.pos[0] + self.canvas_pos[0] + layer.pos[0], self.pos[1] + self.canvas_pos[1] + layer.pos[1]))


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
    def __init__(self, win, view_model):
        self.win = win
        self.view_model = view_model

        menu_bar = self.create_menu_bar()
        tool_bar = self.create_tool_bar()
        self.viewport = self.create_viewport()
        self.layer_bar = self.create_layer_bar()

        layout = [
            [menu_bar],
            [
                tool_bar, self.viewport
            ],
        ]

        self.view = PixelArtGui(self.win, layout, self.viewport, parent=self)

    def create_menu_bar(self):
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

    def create_tool_bar(self):
        tool_bar = gui.RadioButtonContainer([
            [gui.ButtonToggleContainer('tool_move',   [[gui.Surf(pygame.image.load(r'./Assets/move.png'),      0.08, smooth=True)]], selected=True)],
            [gui.ButtonToggleContainer('tool_select', [[gui.Surf(pygame.image.load(r'./Assets/selection.png'), 0.08, smooth=True)]])],
            [gui.ButtonToggleContainer('tool_pencil', [[gui.Surf(pygame.image.load(r'./Assets/pencil.png'),    0.08, smooth=True)]])],
        ])

        return tool_bar

    def create_viewport(self):
        viewport = PixelArtViewportElement()
        return viewport

    def create_layer_bar(self):
        return None
    
    def handle_event(self, event):
        ''' pygame event handler for entire gui '''
        self.view.handle_event(event)

    def step(self):
        self.view.step()
        event, values = self.view.read()
        if event:
            self.view_model.handle_gui_event(event)

    def draw(self):
        self.view.draw()

    def update_layers(self):
        ''' update the layer bar '''
        layers = self.view_model.layers
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