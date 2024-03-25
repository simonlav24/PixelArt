import pygame
import json
from typing import List

import gui

SWITCH_LAYER = 'switch_layer'

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

    def serialize(self) -> str:
        pass

    def deserialize(self, input):
        pass
    
class LayerBar:
    def __init__(self, pos, win: pygame.Surface, parent):
        self.parent = parent
        self.win = win
        self.pos = pos
        self.layer_dict = {}

    def update_layers(self, layers: List[Layer]):
        ''' initial update of layers '''
        radio_layout = []

        first_selected = False
        for layer in layers:

            layer_surf_element = gui.Surf(layer.surf, fixed_size=(50,50))
            self.layer_dict[layer.name] = {'layer': layer, 'element': layer_surf_element}

            layout_button = [
                [layer_surf_element, gui.Text(layer.name, width=100)],
            ]

            layer_button = gui.ButtonToggleContainer(f'{SWITCH_LAYER}_{layer.name}' ,layout_button)
            if not first_selected:
                layer_button.selected = True
                first_selected = True
            radio_layout.append([layer_button])

        layout = [
            [gui.Button('Add Layer', 'add_layer')],
            [gui.RadioButtonContainer(radio_layout)],
        ]

        self.layer_bar_gui = gui.Gui(self.win, layout, self.pos, name='layer bar')

    def update_layer(self, layer_name: str):
        ''' update single layer live '''
        layer = self.layer_dict[layer_name]['layer']
        self.layer_dict[layer_name]['element'].update_surf(layer.surf)

    def handle_event(self, event):
        self.layer_bar_gui.handle_event(event)

    def step(self):
        self.layer_bar_gui.step()
        event, values = self.layer_bar_gui.read()
        if event:
            self.parent.handle_internal_event(event, values)

    def draw(self):
        self.layer_bar_gui.draw()

        