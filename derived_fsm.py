class DERIVED_FSM():

    def __init__(self):
        self.current_timestamp = 0
        self.previous_timestamp = 0
        # TODO: does ASI know the pole pairs correctly?
        # self.pole_pairs = 23
        self.wheel_circumference = 1.89

    def update(self, vehicle_data, derived_data, time_stamps):

        derived_data['speed'] = vehicle_data['motor_rpm'] * self.wheel_circumference / 60.0
        derived_data['distance'] += derived_data['speed'] * time_stamps['event_loop_elapsed'] / 1000.0

        derived_data['charge'] += vehicle_data['battery_current'] * time_stamps['event_loop_elapsed'] / 1000.0 / 3600.
        derived_data['energy'] += vehicle_data['battery_current'] * vehicle_data['battery_voltage'] * time_stamps['event_loop_elapsed'] / 1000.0 / 3600.

        if derived_data['distance'] > 0.0:
            derived_data['trip_efficiency'] = derived_data['energy'] / derived_data['distance']
        else:
            derived_data['trip_efficiency'] = 0

        # TODO: implement internal resistance
        #derived_data['internal_resistance']
        filter_alpha = 0.99
        current_threshold = 0.5
        if abs(vehicle_data['battery_current'] - derived_data['battery_current_prev']) > current_threshold:
            derived_data['internal_resistance_prev'] = derived_data['internal_resistance']
            derived_data['internal_resistance'] = - (derived_data['battery_voltage_prev'] - vehicle_data['battery_voltage']) / (derived_data['battery_current_prev'] - vehicle_data['battery_current'])
            derived_data['internal_resistance'] = filter_alpha * derived_data['internal_resistance_prev'] + (1 - filter_alpha) * derived_data['internal_resistance']

        # update previous readings with current
        derived_data['battery_current_prev'] = vehicle_data['battery_current']
        derived_data['battery_voltage_prev'] = vehicle_data['battery_voltage'
