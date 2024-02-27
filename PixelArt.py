import pygame
import argparse
import PixelArtSg
import gui
from typing import Dict, List
pygame.init()

winWidth = 1280
winHeight = 720
win = pygame.display.set_mode((winWidth,winHeight))

### setup

TOOL_MOVE = 0
TOOL_PENCIL = 1
TOOL_EYEDROP = 2
TOOL_RECT_SELECT = 3

def apply_effect_hue(surf: pygame.Surface, amount, area=None):
    if not area:
        area = ((0,0),surf.get_size())
    for x in range(area[0][0], area[0][0] + area[1][0]):
        for y in range(area[0][1], area[0][1] + area[1][1]):
            color = surf.get_at((x, y))
            hue_value = color.hsva[0]
            hue_value = (hue_value + amount) % 360
            color.hsva = (hue_value, color.hsva[1], color.hsva[2], color.hsva[3])
            surf.set_at((x, y), color)

class Layer:
    def __init__(self):
        self.pos = (0,0)
        self.surf = None
    def get_surf(self):
        return self.surf
    def get_pos(self):
        return self.pos

class Editor:
    def __init__(self):
        self.viewport : ViewPort = ViewPort()
        self.viewport.parent = self
        self.color_picker : ColorPicker = ColorPicker()
        self.color_picker.parent = self
            
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

    def step(self):
        if click_hold:
            self.active_tool.click_hold()

    def draw(self):    
        win.fill((37,37,37))
        self.viewport.draw()
        
        self.color_picker.draw()
        self.selection.draw()
        self.active_tool.draw()

class ViewPort:
    def __init__(self):
        self.parent = None
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
    
    def create_background_surf(self):
        size = (int(self.surf.get_width() * self.zoom), int(self.surf.get_height() * self.zoom))
        self.background = pygame.Surface(size)
        bg_rect_size = 20
        colors = [(75, 75, 75), (85, 85, 85)]
        c = 0
        for y in range(0, size[1], bg_rect_size):
            for x in range(0, size[0], bg_rect_size):
                pygame.draw.rect(self.background, colors[c], ((x, y), (bg_rect_size, bg_rect_size)))
                c = (c + 1) % 2

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

class ColorPicker:
    def __init__(self):
        self.current_color = (255,255,255)
        self.offset = (0,0)
        self.rect_size = 100
        self.parent : Editor = None
    def draw(self):
        # draw color at mouse
        pygame.draw.rect(win, editor.viewport.get_at(pygame.mouse.get_pos()), (self.offset, (self.rect_size, self.rect_size)))
        # draw active color
        pygame.draw.rect(win, self.current_color, ((self.offset[0] + self.rect_size, self.offset[1]), (self.rect_size, self.rect_size)))

class Selection:
    def __init__(self):
        self.active = False
        self.rect = None
        self.parent : Editor = None
    def set_rect(self, rect):
        self.rect = rect
    def draw(self):
        if not self.active:
            return
        viewport = self.parent.get_viewport()
        pos = viewport.get_surf_pos_to_win(self.rect[0])
        size = (viewport.size_surf_to_size_win(self.rect[1][0]), viewport.size_surf_to_size_win(self.rect[1][1]))
        pygame.draw.rect(win, (100,100,100), (pos, size), 1)

class Tool:
    def __init__(self, type):
        self.parent : Editor = None
        self.type = type
    def click_press(self):
        pass
    def click_hold(self):
        pass
    def click_release(self):
        pass
    def draw(self):
        pass

class ToolPencil(Tool):
    def __init__(self):
        super().__init__(TOOL_PENCIL)
    def click_press(self):
        color = self.parent.color_picker.current_color
        self.parent.viewport.set_at(pygame.mouse.get_pos(), color)
    def click_hold(self):
        self.click_press()

class ToolEyeDrop(Tool):
    def __init__(self):
        super().__init__(TOOL_EYEDROP)
    def click_press(self):
        self.parent.color_picker.current_color = self.parent.viewport.get_at(pygame.mouse.get_pos())

class ToolRectangleSelect(Tool):
    def __init__(self):
        super().__init__(TOOL_RECT_SELECT)
        
        self.start = None
        self.end = None
    def click_press(self):
        editor = self.parent
        viewport = self.parent.get_viewport()
        self.start = viewport.get_mouse_pos_on_surf(pygame.mouse.get_pos())
        editor.selection.active = True
    def click_hold(self):
        viewport = self.parent.get_viewport()
        self.end = viewport.get_mouse_pos_on_surf(pygame.mouse.get_pos())
        min_x = min(self.start[0], self.end[0])
        max_x = max(self.start[0], self.end[0])
        min_y = min(self.start[1], self.end[1])
        max_y = max(self.start[1], self.end[1])
        rect = ((min_x, min_y), (max_x - min_x, max_y - min_y))
        self.parent.selection.set_rect(rect)

class ToolMove(Tool):
    def __init__(self):
        super().__init__(TOOL_MOVE)
        self.last_pos = None
    def click_press(self):
        viewport = self.parent.get_viewport()
        self.last_pos = viewport.get_mouse_pos_on_surf(pygame.mouse.get_pos())
    def click_hold(self):
        viewport = self.parent.get_viewport()
        last = self.last_pos
        current = viewport.get_mouse_pos_on_surf(pygame.mouse.get_pos())
        offset = (current[0] - last[0], current[1] - last[1])
        self.last_pos = viewport.get_mouse_pos_on_surf(pygame.mouse.get_pos())
        layer = self.parent.get_active_layer()
        layer.pos = (layer.pos[0] + offset[0], layer.pos[1] + offset[1])

class Effect:
    def __init__(self, editor):
        self.editor : Editor = editor
    def apply(self):
        pass

class EffectHue(Effect):
    def __init__(self, editor, hue_value):
        super().__init__(editor)
        self.hue_value = hue_value
    def apply(self):
        surf = editor.viewport.active_layer.get_surf()
        area = None
        if self.editor.selection.active:
            area = self.editor.selection.rect
        apply_effect_hue(surf, self.hue_value, area)

def handle_tool_bar_events(event, values, editor):
    if event == 'tool_move':
        editor.switch_tool(TOOL_MOVE)
    elif event == 'tool_select':
        editor.switch_tool(TOOL_RECT_SELECT)
    elif event == 'tool_pencil':
        editor.switch_tool(TOOL_PENCIL)

def parse_arguments():
    parser = argparse.ArgumentParser(description='PixelArt')
    parser.add_argument('initial_file_path', default='', nargs='?')
    return parser.parse_args()

args = parse_arguments()

editor = Editor()

if args.initial_file_path != '':
    image_path = args.initial_file_path
    image = pygame.image.load(image_path)
    editor.load_iamge(image_path)
else:
    editor.create_new()


tool_bar_layout = [
    [gui.ButtonImage('', key='tool_move', image_path=r'./Assets/move.png')],
    [gui.ButtonImage('', key='tool_select', image_path=r'./Assets/selection.png')],
    [gui.ButtonImage('', key='tool_pencil', image_path=r'./Assets/pencil.png')],
]
tool_bar = gui.Gui(win, tool_bar_layout, pos=(100, 200))

### main loop

click_hold = False
alt_hold = False
run = True
while run:
    for event in pygame.event.get():
        tool_bar.handle_event(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.DROPFILE:
            editor.load_iamge(event.file)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                editor.active_tool.click_press()
                click_hold = True
            if event.button == 5:
                if pygame.key.get_mods() & pygame.KMOD_ALT:
                    editor.viewport.zoom_in(0.9)
            if event.button == 4:
                if pygame.key.get_mods() & pygame.KMOD_ALT:
                    editor.viewport.zoom_in(1.1)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                editor.active_tool.click_release()
                click_hold = False
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
            if event.key == pygame.K_c:
                color = PixelArtSg.get_color(editor.color_picker.current_color)
                editor.color_picker.current_color = color
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
    
    editor.step()
    tool_bar.step()
    event, values = tool_bar.read()
    if event:
        handle_tool_bar_events(event, values, editor)
    
    editor.draw()
    tool_bar.draw()
    
    pygame.display.update()