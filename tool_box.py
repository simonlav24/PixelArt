

import pygame

from tools import Tool


class ToolBox:
    def __init__(self) -> None:
        self.current_tool: Tool = None
    
    def handle_event(self, event):
        ''' handle pygame event '''