
import gui
from typing import List

class ViewBase:
    def __init__(self, guis: List[gui.Gui], view_model):
        self.guis = guis
        self.view_model = view_model
    
    def step(self):
        for gui in self.guis:
            gui.step()
    
    def draw(self):
        for gui in self.guis:
            gui.draw()