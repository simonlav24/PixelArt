
import pygame
import editor

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

class Effect:
    def __init__(self, effective_editor):
        self.editor : editor.Editor = effective_editor
    def apply(self):
        pass

class EffectHue(Effect):
    def __init__(self, editor, hue_value):
        super().__init__(editor)
        self.hue_value = hue_value
    def apply(self):
        surf = self.editor.viewport.active_layer.get_surf()
        area = None
        if self.editor.selection.active:
            area = self.editor.selection.rect
        apply_effect_hue(surf, self.hue_value, area)