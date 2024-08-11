import pygame
from pygame.math import Vector2

from typing import List
from pydantic import BaseModel, ConfigDict

import gui

SWITCH_LAYER = 'switch_layer'


class LayerBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    pos: Vector2 = Vector2(0, 0)
    require_update: bool = False

    def render(self) -> pygame.Surface:
        pass


class LayerSurf(LayerBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    surf: pygame.Surface

    def render(self) -> pygame.Surface:
        return self.surf


class TextLayer(LayerBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    text: str
    font: pygame.font