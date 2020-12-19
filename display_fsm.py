import board
import displayio
import terminalio
import busio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import adafruit_ili9341
# from adafruit_hx8357 import HX8357 # 3.5TFT

# /Library/Fonts/
# create fonts with: otf2bdf Times\ New\ Roman.ttf -r 100 -p 32 -o tnr-32.bdf
# https://mlibby.com/notes/bdf_fonts_for_circuitpython/

# Release any resources currently in use for the displays
class DISPLAY():

    def __init__(self, spi):
    # def __init__(self):
        displayio.release_displays()

        # self.spi = board.SPI()
        # self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        # self.spi = busio.SPI(board.D52, MISO=board.D50, MOSI=board.D51)
        self.spi = spi
        self.tft_cs = board.D10
        self.tft_dc = board.D9
        self.display_bus = displayio.FourWire(self.spi,
                                              command=self.tft_dc,
                                              chip_select=self.tft_cs)
        # self.display = HX8357(self.display_bus, width=480, height=320)
        self.display = adafruit_ili9341.ILI9341(self.display_bus, width=320, height=240)
        # font = terminalio.FONT
        # font = bitmap_font.load_font("fonts/Arial-16.bdf")
        font = bitmap_font.load_font("fonts/tnr-28.bdf")
        color = 0xFFFFFF
        y_spacing = 34
        y_offset = 16
        # init the group with all the labels here in an array
        self.text_labels = [label.Label(font, color=color, max_glyphs=20, x=10, y=y_offset),
                            label.Label(font, color=color, max_glyphs=20, x=10, y=y_offset + 1 * y_spacing),
                            label.Label(font, color=color, max_glyphs=20, x=10, y=y_offset + 2 * y_spacing),
                            label.Label(font, color=color, max_glyphs=20, x=10, y=y_offset + 3 * y_spacing),
                            label.Label(font, color=color, max_glyphs=20, x=10, y=y_offset + 4 * y_spacing),
                            label.Label(font, color=color, max_glyphs=20, x=10, y=y_offset + 5 * y_spacing),
                            label.Label(font, color=color, max_glyphs=20, x=10, y=y_offset + 6 * y_spacing)]
        self.text_group = displayio.Group(max_size=8)
        for tl in self.text_labels:
            self.text_group.append(tl)
        self.update_line = 0

    def update(self, vehicle_data, derived_data, time_stamps):



        # print('enter update', time.monotonic())
        # rotate through lines to get better response rate and reduce flicker

        if self.update_line == 0:
            text = f'CV: {vehicle_data["high_cell_voltage"]:.2f} {vehicle_data["low_cell_voltage"]:.2f}'
        elif self.update_line == 1:
            if abs(vehicle_data['battery_current']) < 10.0:
                text = f'C {vehicle_data["battery_current"]:.0f} B {vehicle_data["battery_current_BMS"]:.1f} M {vehicle_data["motor_current"]:.0f}'
            else:
                text = f'C {vehicle_data["battery_current"]:.0f} B {vehicle_data["battery_current_BMS"]:.0f} M {vehicle_data["motor_current"]:.0f}'
        elif self.update_line == 2:
            text = f'B {vehicle_data["high_battery_temp"]:.0f} M {vehicle_data["motor_temperature"]:.0f} C {vehicle_data["controller_temperature"]:.0f}'
        elif self.update_line == 3:
            text = f'IR {derived_data["internal_resistance"]*1000:.0f}'
        elif self.update_line == 4:
            text = f'S: {derived_data["speed"]:.1f} {derived_data["distance"]:.1f}'
        elif self.update_line == 5:
            text = f'C {derived_data["charge"]:.2f} E {derived_data["trip_efficiency"]:.2f}'
        elif self.update_line == 6:
            text = f'dt: {time_stamps["event_loop_elapsed"] * 1000:.0f}'

        self.text_group[self.update_line].text = text

        self.update_line += 1
        if self.update_line > 6:
            self.update_line = 0

        self.display.show(self.text_group)

        # print('leave update', time.monotonic())