import board
import busio
import struct
import time

class ASI_FSM():
    def __init__(self):
        # self.asi_uart = busio.UART(board.D12, board.D13, baudrate=115200) # Feather M4
        self.asi_uart = busio.UART(board.D16, board.D17, baudrate=115200) # Grand Central
        self.asi_request = bytes([0x01, 0x03, 0x01, 0x03, 0x00, 0x08, 0xB5, 0xF0])
        self.response = []
        self.state = 'request'

    def update(self, vehicle_data):

        # if self.state == 'request':
        if True:
            # print('ar', time.monotonic())
            self.asi_uart.write(self.asi_request)

            self.state = 'process'
            # return vehicle_data

        # elif self.state == 'process':
        if True:

            try:
                # print('ap', time.monotonic())
                self.response = self.asi_uart.read(21)

                vehicle_data['controller_temperature'] = struct.unpack('>h', self.response[3:5])[0] / 1.0
                vehicle_data['motor_temperature'] = struct.unpack('>h', self.response[7:9])[0] / 1.0
                vehicle_data['motor_current'] = struct.unpack('>h', self.response[9:11])[0] / 32.0
                vehicle_data['motor_rpm'] = struct.unpack('>h', self.response[11:13])[0] / 1.0

                # if reading battery from ASI
                vehicle_data['battery_voltage'] = struct.unpack('>h', self.response[15:17])[0] / 32.0
                vehicle_data['battery_current'] = struct.unpack('>h', self.response[17:19])[0] / 32.0

                self.state = 'request'

            except:
                print('ASI response failed')

            return vehicle_data