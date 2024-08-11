
import pygame
from pygame import Vector2
import os
from layer_data import LayerBase, LayerSurf
from typing import List
import tools
from tool_box import ToolBox

image_formats = ['.png', '.jpeg', '.jpg', '.bmp']

class EditorViewModel:
    def __init__(self):
        
        self.layers: List[LayerBase] = []
        self.current_layer: LayerBase = None

        self.tool_box: ToolBox = ToolBox()

    def set_view(self, view):
        self.view = view

    def handle_event(self, event):
        ''' handle pygame event '''
        self.tool_box.handle_event(event)

    def draw(self, win: pygame.Surface):
        pass
    
    def handle_gui_event(self, event):
        print(event)

    def load_image(self, path: str):
        if(any([path.endswith(i) for i in image_formats])):
            # import image to layer
            image_surf = pygame.image.load(path)
            new_layer = LayerSurf(pos=Vector2(0,0), surf=image_surf)

            self.layers.append(new_layer)

    def save(self, path):
        pass

    