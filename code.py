# Feather TFT vehicle telemetry platform

import board
import time
import display_fsm
import bms_fsm
# import asi_fsm
import derived_fsm
import buttons_fsm
import sd_card_fsm

time_stamps = {'event_loop_current':0,
               'event_loop_previous':0,
               'event_loop_elapsed':0}

vehicle_data = {'battery_voltage':0,
                'battery_current':0,
                'battery_voltage_BMS':0,
                'battery_current_BMS':0,
                'high_cell_voltage':0,
                'low_cell_voltage':0,
                'high_battery_temp':0,
                'motor_rpm':0,
                'motor_temperature':0,
                'motor_current':0,
                'controller_temperature':0}

derived_data = {'internal_resistance':0.090,
                'distance':0,
                'battery_voltage_prev':0,
                'battery_current_prev':0,
                'charge':0,
                'energy':0,
                'trip_efficiency':0,
                'instantaneous_efficiency':0}

button_states = {'screen_current':False,
                 'screen_previous':False,
                 'button_flag':False}

spi = board.SPI()

display = display_fsm.DISPLAY(spi)
bms = bms_fsm.BMS_FSM()
# asi = asi_fsm.ASI_FSM()
derived = derived_fsm.DERIVED_FSM()
buttons = buttons_fsm.BUTTONS_FSM(spi)
sd_card = sd_card_fsm.SD_CARD_FSM()

print('Starting Dashboard')

while True:

    time_stamps['event_loop_current'] = time.monotonic()
    time_stamps['event_loop_elapsed'] = time_stamps['event_loop_current'] - time_stamps['event_loop_previous']
    time_stamps['event_loop_previous'] = time_stamps['event_loop_current']

    print(time_stamps['event_loop_elapsed'])
    # print('t', time.monotonic() - time_stamps['event_loop_current'])
    bms.update(vehicle_data)
    # print('b', time.monotonic() - time_stamps['event_loop_current'])
    # asi.update(vehicle_data)
    # print('a', time.monotonic() - time_stamps['event_loop_current'])
    derived.update(vehicle_data, derived_data, time_stamps)
    # print('c', time.monotonic() - time_stamps['event_loop_current'])
    display.update(vehicle_data, derived_data, time_stamps)
    # print('d', time.monotonic() - time_stamps['event_loop_current'])
    button_states = buttons.update(button_states)
    # print('u', time.monotonic() - time_stamps['event_loop_current'])
    button_states = sd_card.update(vehicle_data, derived_data, button_states)
    # print('s', time.monotonic() - time_stamps['event_loop_current'])