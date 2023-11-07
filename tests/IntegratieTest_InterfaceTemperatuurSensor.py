import unittest
import random


class DS18B20Simulator:  # Temperature sensor
    def __init__(self, location, initial_temperature=30.00):
        self.location = location
        self.temperature = initial_temperature
        self.fanOnOrOff = True

    # Function to convert a 12-bit raw reading to Celsius
    # @location_logger_decorator
    # @timing_decorator
    def get_temperature(self, twelve_bit_value):
        # Extract the bits
        sign_bit = (twelve_bit_value >> 11) & 0x01
        magnitude = twelve_bit_value & 0x07FF

        # Calculate the temperature in Celsius
        resolution = 0.0625
        self.temperature = -magnitude * resolution if sign_bit == 1 else magnitude * resolution

        return self.temperature

    # Function to generate a 12-bit raw reading
    def generate_12_bit_reading(self):
        simulated_temperature = self.temperature + random.uniform(-1.00, 1.00)

        if self.fanOnOrOff:
            simulated_temperature -= 0.3
        else:
            simulated_temperature += 0.3

        # Convert the temperature to a 12-bit raw reading
        resolution = 0.0625
        if simulated_temperature < 0:
            # For negative temperatures, set the sign bit (Bit 11) to 1
            sign_bit = 1
            magnitude = abs(simulated_temperature)
        else:
            sign_bit = 0
            magnitude = simulated_temperature

        raw_reading = int(magnitude / resolution)
        twelve_bit_value = (sign_bit << 11) | raw_reading

        return twelve_bit_value


    def fanOn(self):
        self.fanOnOrOff = True

    def fanOff(self):
        self.fanOnOrOff = False


def make_decision(light_level, temperature, threshold_config):
    light_low_threshold = threshold_config.get("light_low_threshold")
    temperature_low_threshold = threshold_config.get("temperature_low_threshold")
    temperature_high_threshold = threshold_config.get("temperature_high_threshold")
    
    if light_level < light_low_threshold:
        if temperature > temperature_high_threshold:
            decision = "Close Curtains and Turn On Fan"
        elif temperature <= temperature_high_threshold and temperature > temperature_low_threshold:
            decision = "Close Curtains and Turn On Fan"
        else:
            decision = "Close Curtains and Turn Off Fan"
    else:
        if temperature > temperature_high_threshold:
            decision = "Close Curtains and Turn On Fan"
        elif temperature <= temperature_high_threshold and temperature > temperature_low_threshold:
            decision = "Close Curtains and Turn On Fan"
        else:
            decision = "Open Curtains and Turn Off Fan"

    return decision

class TestTemperatureSensorIntegration(unittest.TestCase):
    def test_temperature_sensor_integration(self):
        temperature_sensor = DS18B20Simulator("TestLocation")
        
        threshold_config = {"light_low_threshold": 100, "temperature_low_threshold": 20, "temperature_high_threshold": 24}

        simulated_readings = [23, 25, 22, 26, 21]

        for temperature_reading in simulated_readings:
            twelve_bit_value = temperature_sensor.generate_12_bit_reading()
            
            temperature = temperature_sensor.get_temperature(twelve_bit_value)

            decision = make_decision(light_level=120, temperature=temperature, threshold_config=threshold_config)
            
            # Assertions for the decision
            if temperature > threshold_config["temperature_high_threshold"]:
                self.assertEqual(decision, "Close Curtains and Turn On Fan")
            elif temperature <= threshold_config["temperature_high_threshold"] and temperature > threshold_config["temperature_low_threshold"]:
                self.assertEqual(decision, "Close Curtains and Turn On Fan")
            else:
                self.assertEqual(decision, "Open Curtains and Turn Off Fan")

if __name__ == '__main__':
    unittest.main()
