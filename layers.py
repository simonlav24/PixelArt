import pygame
from typing import List

import gui

class Layer:
    def __init__(self, name=None):
        self.pos = (0,0)
        self.surf: pygame.Surface = None
        self.name = 'new layer'
        if name:
            self.name = name
    def get_surf(self):
        return self.surf
    def get_pos(self):
        return self.pos
    
class LayerBar:
    def __init__(self, pos, win: pygame.Surface, parent):
        self.parent = parent
        self.win = win
        self.pos = pos

    def update_layers(self, layers: List[Layer]):
        radio_layout = []

        for layer in layers:
            layout_button = [
                [gui.Surf(layer.surf, fixed_size=(70,70)), gui.Text(layer.name)],
            ]
            layer_button = gui.ButtonToggleContainer(f'layer_{layer.name}' ,layout_button)
            radio_layout.append([layer_button])

        layout = [
            [gui.Button('Add Layer', 'add_layer')],
            [gui.RadioButtonContainer(radio_layout)],
        ]

        self.layer_bar_gui = gui.Gui(self.win, layout, self.pos, name='layer bar')

    def handle_event(self, event):
        self.layer_bar_gui.handle_event(event)

    def step(self):
        self.layer_bar_gui.step()
        event, values = self.layer_bar_gui.read()
        if event:
            self.parent.handle_internal_event(event, values)

    def draw(self):
        self.layer_bar_gui.draw()

        