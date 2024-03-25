
import pygame
import os
from layers import Layer
from typing import List
import tools

image_formats = ['.png', '.jpeg', '.jpg', '.bmp']

class EditorViewModel:
    def __init__(self):
        self.layers: List[Layer] = []

        self.current_tool = tools.TOOL_MOVE

    def set_view(self, view):
        self.view = view

    def handle_gui_event(self, event):
        print(event)

    def load(self, path: str):
        if(any([path.endswith(i) for i in image_formats])):
            # import image to layer
            image_surf = pygame.image.load(path)
            new_layer = Layer(os.path.basename(path))
            new_layer.set_surf(image_surf)

            self.layers.append(new_layer)
            self.view.update_layers()

    def save(self, path):
        pass

    