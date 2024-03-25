
import pygame

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