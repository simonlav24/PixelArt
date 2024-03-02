
import pygame
from tools import *
from typing import Dict, List
import gui
import customGui

class Layer:
    def __init__(self):
        self.pos = (0,0)
        self.surf = None
    def get_surf(self):
        return self.surf
    def get_pos(self):
        return self.pos

class Editor:
    def __init__(self, win):
        self.win = win
        self.viewport : ViewPort = ViewPort()
        self.viewport.parent = self
            
        self.previous_tool = TOOL_PENCIL
        self.tools : Dict[int, Tool] = {
            TOOL_PENCIL: ToolPencil(),
            TOOL_EYEDROP: ToolEyeDrop(),
            TOOL_RECT_SELECT: ToolRectangleSelect(),
            TOOL_MOVE: ToolMove(),
            }
        self.active_tool = self.tools[TOOL_PENCIL]
        for tool in self.tools.values():
            tool.parent = self
        self.selection = Selection()
        self.selection.parent = self

        self.current_color = (255,255,255)

        self.guis: List[gui.Gui] = []
        # create tool bar
        tools_radio_layout = [
            [gui.ButtonToggleContainer('tool_move', [[gui.Surf(pygame.image.load(r'./Assets/move.png'), 0.08)]])],
            [gui.ButtonToggleContainer('tool_select', [[gui.Surf(pygame.image.load(r'./Assets/selection.png'), 0.08)]])],
            [gui.ButtonToggleContainer('tool_pencil', [[gui.Surf(pygame.image.load(r'./Assets/pencil.png'), 0.08)]])],
        ]
        tool_bar_layout = [
            [gui.RadioButtonContainer(tools_radio_layout)],
            [customGui.ClickableRectangle('change_color', self.current_color)]
        ]
        self.tool_bar = gui.Gui(self.win, tool_bar_layout, pos=(100, 200))
        self.guis.append(self.tool_bar)

        # event vars
        self.click_hold = False

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active_tool.click_press()
                self.click_hold = True
            if event.button == 5:
                if pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.viewport.zoom_in(0.9)
            if event.button == 4:
                if pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.viewport.zoom_in(1.1)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.active_tool.click_release()
                self.click_hold = False

    def create_new(self):
        new_surf = pygame.Surface((16, 16), pygame.SRCALPHA)

        self.viewport.set_size(new_surf.get_size())

        layer = Layer()
        layer.surf = new_surf

        self.viewport.layers.clear()
        self.viewport.add_layer(layer)
        self.viewport.auto_zoom()

    def load_iamge(self, image_path):
        image = pygame.image.load(image_path)

        self.viewport.set_size(image.get_size())

        layer = Layer()
        layer.surf = image

        self.viewport.layers.clear()
        self.viewport.add_layer(layer)
        self.viewport.auto_zoom()
    
    def get_viewport(self):
        return self.viewport
        
    def get_active_layer(self) -> Layer:
        return self.viewport.active_layer
    
    def switch_tool_previous(self):
        self.active_tool = self.tools[self.previous_tool]

    def switch_tool(self, type):
        if self.active_tool.type == type:
            return
        self.previous_tool = self.active_tool.type
        self.active_tool = self.tools[type]

    def set_color(self, color):
        self.current_color = color
        self.tool_bar['change_color'].update_color(color)

    def step(self):
        if self.click_hold:
            self.active_tool.click_hold()
        
        # step guis
        for g in self.guis:
            g.step()
        for g in self.guis:
            event, values = g.read()
            if event:
                print('[EVENT]', event, values)
                self.handle_tool_bar_events(event, values)

    def draw(self):
        self.win.fill((37,37,37))
        self.viewport.draw()
        
        self.selection.draw()
        self.active_tool.draw()

        # guis step
        for g in self.guis:
            g.draw()
    
    def handle_tool_bar_events(self, event, values):
        if event == 'tool_move':
            self.switch_tool(TOOL_MOVE)
        elif event == 'tool_select':
            self.switch_tool(TOOL_RECT_SELECT)
        elif event == 'tool_pencil':
            self.switch_tool(TOOL_PENCIL)
        elif event == 'change_color':
            ''' click on color rectangle '''
            layout = [[customGui.ColorPicker('color_picker', color=self.current_color, enable_events=True)]]
            pos = values['gui']['change_color'].pos
            size = values['gui']['change_color'].size
            gui_color = gui.Gui(self.win, layout, pos=(pos[0] + size[0] + 4, pos[1] + size[1] + 4))
            self.guis.append(gui_color)
        elif event == 'color_picker':
            ''' color is changed live in the color picker '''
            color = values['color_picker']
            self.set_color(color)
        elif event == 'color_ok':
            ''' click ok in color picker '''
            self.guis.remove(values['gui'])
            color = values['color_picker']
            self.set_color(color)

class ViewPort:
    def __init__(self):
        self.parent: Editor = None
        self.zoom = 1.0
        self.layers : List[Layer] = []

        # the surf that represents the viewport
        self.surf = pygame.Surface((100,100), pygame.SRCALPHA)
        self.offset = (0,0)
        self.active_layer : Layer = None
        self.background : pygame.Surface = None

    def add_layer(self, layer):
        self.layers.append(layer)
        self.active_layer = layer

    def zoom_in(self, value):
        self.zoom *= value
        self.create_background_surf()
    
    def create_background_surf(self):
        size = (int(self.surf.get_width() * self.zoom), int(self.surf.get_height() * self.zoom))
        self.background = pygame.Surface(size)
        bg_rect_size = 20
        colors = [(75, 75, 75), (85, 85, 85)]
        row_start_c = 0
        c = row_start_c
        for y in range(0, size[1], bg_rect_size):
            for x in range(0, size[0], bg_rect_size):
                pygame.draw.rect(self.background, colors[c], ((x, y), (bg_rect_size, bg_rect_size)))
                c = (c + 1) % 2
            row_start_c = (row_start_c + 1) % 2
            c = row_start_c

    def auto_zoom(self):
        self.zoom = 500 / self.surf.get_width()
        self.create_background_surf()

    def set_size(self, size):
        self.surf = pygame.Surface(size, pygame.SRCALPHA)

    def get_mouse_pos_on_surf(self, pos_on_win):
        return (int((pos_on_win[0] - self.offset[0]) / self.zoom), int((pos_on_win[1] - self.offset[1]) / self.zoom))
    
    def get_surf_pos_to_win(self, pos_on_surf):
        return (pos_on_surf[0] * self.zoom + self.offset[0], pos_on_surf[1] * self.zoom + self.offset[1])
    
    def size_surf_to_size_win(self, size):
        return size * self.zoom
    
    def draw(self):
        win = self.parent.win
        # blit background
        win.blit(self.background, self.offset)

        # clear
        self.surf.fill((0,0,0,0))
        
        for l in self.layers:
            self.surf.blit(l.get_surf(), l.get_pos())
    
        zoom = (self.surf.get_width() * self.zoom, self.surf.get_height() * self.zoom)
        
        surf = pygame.transform.scale(self.surf, zoom)
        
        self.offset = (win.get_width() / 2 - surf.get_width() / 2, win.get_height() / 2 - surf.get_height() / 2)
        win.blit(surf, self.offset)
        
        # draw viewport outline
        pygame.draw.rect(win, (255, 255, 255), (self.offset, zoom), 1)
        
        # draw pixel rect
        mouse_pos = pygame.mouse.get_pos()
        pos = (int((mouse_pos[0] - self.offset[0]) / self.zoom), int((mouse_pos[1] - self.offset[1]) / self.zoom))
        pos = (self.offset[0] + pos[0] * self.zoom , (self.offset[1] + pos[1] * self.zoom) )
        size = (self.zoom, self.zoom)
        pygame.draw.rect(win, (255, 255, 100), (pos, size), 1)
        
    def get_at(self, target_pos):
        pos = self.get_mouse_pos_on_surf(target_pos)
        if pos[0] < 0 or pos[0] >= self.surf.get_width() or pos[1] < 0 or pos[1] >= self.surf.get_height():
            return (0,0,0)
        return self.surf.get_at(pos)

    def set_at(self, target_pos, color):
        pos = self.get_mouse_pos_on_surf(target_pos)
        if pos[0] < 0 or pos[0] >= self.surf.get_width() or pos[1] < 0 or pos[1] >= self.surf.get_height():
            return
        surf = self.active_layer.get_surf()
        pos_offset = (pos[0] - self.active_layer.pos[0], pos[1] - self.active_layer.pos[1])
        surf.set_at(pos_offset, color)
    
    def save(self, path):
        pygame.image.save(self.surf, path)