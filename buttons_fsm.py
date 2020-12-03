# grand central implementation using TFT18 and Seesaw

# TODO: why does initializing this kill the display?
# this needs to share an SPI with the display

import board
import digitalio
from adafruit_stmpe610 import Adafruit_STMPE610_SPI


class BUTTONS_FSM():
    def __init__(self, spi):
        pass
        # self.spi = board.SPI()
        self.spi = spi
        self.cs = digitalio.DigitalInOut(board.D8)
        self.st = Adafruit_STMPE610_SPI(self.spi, self.cs)

    # def update(self, button_states, ss):

    #     buttons = ss.buttons

    #     if buttons.a:
    #         button_states['screen_current'] = True

    #     if button_states['screen_current'] == True and button_states['screen_previous'] == False:
    #         button_states['button_flag'] = True
    #         print('logging flag set to true')

    #     button_states['screen_previous'] = button_states['screen_current']

    #     return button_states

    def update(self, button_states):

        if not self.st.buffer_empty:
            button_states['screen_current'] = True
        else:
            button_states['screen_current'] = False

        if button_states['screen_current'] == True and button_states['screen_previous'] == False:
            button_states['button_flag'] = True
            # button_states['button_flag'] = ~button_states['button_flag']

        button_states['screen_previous'] = button_states['screen_current']

        while True:
            if self.st.buffer_empty:
                break
            else:
                self.st.read_data()

        return button_states


