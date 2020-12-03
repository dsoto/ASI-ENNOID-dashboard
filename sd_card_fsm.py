import time
import board
import digitalio
import busio
import sdcardio
import storage
import adafruit_sdcard
import os

class SD_CARD_FSM():
    def __init__(self):
        self.spi = busio.SPI(board.SD_SCK, board.SD_MOSI, board.SD_MISO)

        # 5.3
        # self.cs = digitalio.DigitalInOut(board.SD_CS)
        # self.sdcard = adafruit_sdcard.SDCard(self.spi, self.cs)

        # 6.0
        self.cs = board.SD_CS
        self.sdcard = sdcardio.SDCard(self.spi, self.cs)

        self.vfs = storage.VfsFat(self.sdcard)
        self.num_data_points = 10
        self.data_point = 0
        self.start_time = 0

        storage.mount(self.vfs, '/sd')

        self.state = 'write'
        self.last_write_time = 0.0
        self.write_interval = 1.00
        self.start_time = 0.0

        files = os.listdir('/sd/')

        i = 0
        while True:
            filename = 'test_{:02d}.csv'.format(i)
            print(filename)
            i = i + 1
            if filename not in files:
                self.filename = '/sd/' + filename
                break

        with open(self.filename, 'w') as file:
            file.write('time,hv,lv,battery_voltage,battery_current,battery_voltage_BMS,battery_current_BMS,motor_current,temperature,internal_resistance,distance')

    def update(self, vehicle_data, derived_data, button_states):

        if self.state == 'idle':
            # wait until tick
            if time.monotonic() - self.last_write_time > self.write_interval:
                self.state = 'write'

        elif self.state == 'write':
            self.last_write_time = time.monotonic()
            with open(self.filename, 'a') as file:
                file.write('%0.3f' % (time.monotonic() - self.start_time))
                file.write(',')
                file.write('%0.2f' % vehicle_data['high_cell_voltage'])
                file.write(',')
                file.write('%0.2f' % vehicle_data['low_cell_voltage'])
                file.write(',')
                file.write('%0.2f' % vehicle_data['battery_voltage'])
                file.write(',')
                file.write('%0.2f' % vehicle_data['battery_current'])
                file.write(',')
                file.write('%0.2f' % vehicle_data['battery_voltage_BMS'])
                file.write(',')
                file.write('%0.2f' % vehicle_data['battery_current_BMS'])
                file.write(',')
                file.write('%0.2f' % vehicle_data['motor_current'])
                file.write(',')
                file.write('%0.2f' % vehicle_data['high_battery_temp'])
                file.write(',')
                file.write('%0.4f' % derived_data['internal_resistance'])
                file.write(',')
                file.write('%0.2f' % derived_data['distance'])
                file.write('\n')
            self.state = 'idle'
            # self.state = 'write'
        return button_states


        # button_flag -> logging_flag
        #if log_flag == True and self.data_point < self.num_data_points:
        # if button_states['button_flag'] == True and self.data_point < self.num_data_points:
        #     print('enter sd if')
        #     if self.data_point == 0:
        #         self.start_time = time.monotonic()
        #     with open('/sd/test_1.txt', 'a') as file:
        #         print('enter sd write')
        #         file.write('%0.3f' % (time.monotonic() - self.start_time))
        #         file.write(',')
        #         file.write('%0.2f' % vehicle_data['high_cell_voltage'])
        #         file.write('\n')

        #         print(self.data_point, time.monotonic()- self.start_time, 'logging')

        #     self.data_point += 1
        #     button_states['button_flag'] = True
        # else:
        #     self.data_point = 0
        #     button_states['button_flag'] = False
        # print(button_states)
        # return button_states