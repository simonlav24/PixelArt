import pygame
import gui
import customGui

class ToolBar:
    def __init__(self, pos, win: pygame.Surface, parent):
        self.parent = parent
        self.win = win
        self.pos = pos

        tools_radio_layout = [
            [gui.ButtonToggleContainer('tool_move',   [[gui.Surf(pygame.image.load(r'./Assets/move.png'),      0.08, smooth=True)]])],
            [gui.ButtonToggleContainer('tool_select', [[gui.Surf(pygame.image.load(r'./Assets/selection.png'), 0.08, smooth=True)]])],
            [gui.ButtonToggleContainer('tool_pencil', [[gui.Surf(pygame.image.load(r'./Assets/pencil.png'),    0.08, smooth=True)]])],
        ]
        tool_bar_layout = [
            [gui.RadioButtonContainer(tools_radio_layout)],
            [customGui.ClickableRectangle('change_color', self.parent.current_color)]
        ]
        self.tool_bar_gui = gui.Gui(self.win, tool_bar_layout, pos=(100, 200), name='tool bar')

        self.color_picker_gui: gui.Gui = None

    def update_color(self, color):
        self.tool_bar_gui['change_color'].update_color(color)

    def handle_event(self, event):
        self.tool_bar_gui.handle_event(event)
        if self.color_picker_gui:
            self.color_picker_gui.handle_event(event)

    def step(self):
        # step
        self.tool_bar_gui.step()
        if self.color_picker_gui:
            self.color_picker_gui.step()

        # read
        event, values = self.tool_bar_gui.read()
        if event == 'change_color':
            ''' click on color rectangle '''
            layout = [[customGui.ColorPicker('color_picker', color=self.parent.current_color, enable_events=True)]]
            pos = values['gui']['change_color'].pos
            size = values['gui']['change_color'].size
            self.color_picker_gui = gui.Gui(self.win, layout, pos=(pos[0] + size[0] + 4, pos[1] + size[1] + 4), name='color picker')
        if event:
            self.parent.handle_internal_event(event, values)

        if self.color_picker_gui:
            event, values = self.color_picker_gui.read()
            if event == 'color_ok':
                ''' click ok in color picker '''
                self.color_picker_gui = None
            if event:
                self.parent.handle_internal_event(event, values)


    def draw(self):
        self.tool_bar_gui.draw()
        if self.color_picker_gui:
            self.color_picker_gui.draw()
