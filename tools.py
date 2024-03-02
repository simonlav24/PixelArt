import pygame
import editor

TOOL_MOVE = 0
TOOL_PENCIL = 1
TOOL_EYEDROP = 2
TOOL_RECT_SELECT = 3

class Selection:
    def __init__(self):
        self.active = False
        self.rect = None
        self.parent: editor.Editor = None
    def set_rect(self, rect):
        self.rect = rect
    def draw(self):
        if not self.active:
            return
        viewport = self.parent.get_viewport()
        pos = viewport.get_surf_pos_to_win(self.rect[0])
        size = (viewport.size_surf_to_size_win(self.rect[1][0]), viewport.size_surf_to_size_win(self.rect[1][1]))
        pygame.draw.rect(self.parent.win, (100,100,100), (pos, size), 1)

class Tool:
    def __init__(self, type):
        self.parent : editor.Editor = None
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
        color = self.parent.current_color
        self.parent.viewport.set_at(pygame.mouse.get_pos(), color)
    def click_hold(self):
        self.click_press()

class ToolEyeDrop(Tool):
    def __init__(self):
        super().__init__(TOOL_EYEDROP)
    def click_press(self):
        self.parent.set_color(self.parent.viewport.get_at(pygame.mouse.get_pos()))

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