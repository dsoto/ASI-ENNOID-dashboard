import board
import busio
import struct
import time

class BMS_FSM():
    def __init__(self):
        # self.bms_uart = busio.UART(board.TX, board.RX, baudrate=115200) # Feather M4
        self.bms_uart = busio.UART(board.D18, board.D19, baudrate=115200) # Grand Central
        self.bms_request = bytes([0x02, 0x01, 0x04, 0x40, 0x84, 0x03])
        self.response = []
        self.state = 'request'

    def update(self, vehicle_data):

        # print('b', time.monotonic())
        # print('e', time.monotonic())

        # if self.state == 'request':
        if True:
            # print('br', time.monotonic())
            self.bms_uart.write(self.bms_request)
            self.state = 'process'
            # return vehicle_data
        # elif self.state == 'process':
        if True:
            # print('bp', time.monotonic())
            try:
                self.response = self.bms_uart.read(48) # ENNOID 48 DBMS 53
            except:
                print('response failed')

            # if reading battery from BMS
            vehicle_data['battery_voltage_BMS'] = struct.unpack('>L', self.response[3:7],)[0] / 1000.
            vehicle_data['battery_current_BMS'] = -struct.unpack('>l', self.response[7:11])[0] / 1000.

            vehicle_data['high_cell_voltage'] = struct.unpack('>L', self.response[12:16])[0] / 1000.0
            vehicle_data['low_cell_voltage'] = struct.unpack('>L', self.response[20:24])[0] / 1000.0
            vehicle_data['high_battery_temp'] = struct.unpack('>h', self.response[34:36])[0] / 10.0

            self.state = 'request'
            return vehicle_data
