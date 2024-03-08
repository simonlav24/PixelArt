import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gui import *

def _test(win):
    image = pygame.image.load('output.png')
    
    layout_comp = [
        [Slider('sliderC1', 0, 100, 50)],
        [Slider('sliderC2', 0, 100, 50)],
        [Slider('sliderC3', 0, 100, 50)],
    ]

    layout_button = [
        [Text('im in a button'), Text('me too')],
        [Text('me three'), Surf(image)]
    ]

    layout_button2 = [
        [Text('im in a button'), Text('me too')],
        [Text('me three'), Surf(image)]
    ]

    layout_radio = [
        [ButtonToggleContainer('toggleButonM', layout_button2), CheckBox('checkMe', 'radioCheckbox')]
    ]

    canvas_layout = [
        [
            # Text('im in canvas', pos=(0,0)),
            Text('im in canvas', pos=(20,20)),
            CheckBox('toggleMe', key='toggleCanvas', pos=(100,50)),
            Button('button(100,100)', key='buttonCanvs', pos=(100,100)),
            DragContainer([[Text('DragMe'), Button('drag', 'drag_button')]])
        ]
    ]

    layout = [
        [Button('press me', key='button1'), Button('me too', key='button2'), CheckBox('toggleMe', key='toggl1')],
        [Button('me three', key='button3'), Text('this is text')],
        [Slider('slider1', 0, 100, 50), Slider('slider2', 0, 100, 50, enable_events=True), Slider('slider3', 0, 100, 50), Slider('slider4', 0, 100, 50)],
        [ElementComposition(layout_comp), Button('press me', key='button4'), Text('texty', vertical_alignment=VerticalAlignment.CENTER)],
        [Button('button after last', key='afterlast')],
        [ButtonContainer('buttonContainer1', layout_button)],
        [RadioButtonContainer(layout_radio)],
        [Canvas(canvas_layout)],
    ]
    return Gui(win, layout, pos=(100, 100), margin=10)

def _test2(win):
    surf = pygame.Surface((200, 200))
    surf.fill((0, 255, 105))
    
    layout_texts = [
        [Text('this is text')],
        [Text('this is also text')],
        [Text('and this two')],
    ]

    layout = [
        [Surf(surf), Text('this text is after surf', vertical_alignment=VerticalAlignment.BOTTOM)],
        [Text('this text is before surf'), Surf(surf)],
        [Surf(surf), ElementComposition(layout_texts)],
    ]

    return Gui(win, layout)

def _test_contextmenu(win):
    file_layout = [
        [Button('Open', 'file_open', text_horizontal_alignment=HorizontalAlignment.LEFT, width=150)],
        [Button('Save', 'file_save', text_horizontal_alignment=HorizontalAlignment.LEFT)],
        [Button('Save as', 'file_saveas', text_horizontal_alignment=HorizontalAlignment.LEFT)],
        [Button('Close', 'file_close', text_horizontal_alignment=HorizontalAlignment.LEFT)],
    ]

    edit_layout = [
        [Button('Copy', 'edit_copy', text_horizontal_alignment=HorizontalAlignment.LEFT, width=150)],
        [Button('Paste', 'edit_paste', text_horizontal_alignment=HorizontalAlignment.LEFT)],
        [Button('Clear', 'edit_clear', text_horizontal_alignment=HorizontalAlignment.LEFT)],
    ]

    layout = [
        [
            ContextMenuButton('File', file_layout),
            ContextMenuButton('Edit', edit_layout),
        ],
        [Text('hi, this is text', width=200, text_horizontal_alignment=HorizontalAlignment.CENTER), Button('button', 'button')]
    ]
    return Gui(win, layout, pos=(100,100))

if __name__ == '__main__':
    ''' example usage '''
    pygame.init()
    win = pygame.display.set_mode((1280,720))

    ### setup
    
    # gui = _test(win)
    gui = _test_contextmenu(win)

    ### main loop

    run = True
    while run:
        for event in pygame.event.get():
            gui.handle_event(event)
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        
        win.fill((37, 37, 37))
        
        gui.step()
        
        event, values = gui.read()
        if event:
            print(event, values)
        
        gui.draw()
        pygame.display.update()
    pygame.quit()