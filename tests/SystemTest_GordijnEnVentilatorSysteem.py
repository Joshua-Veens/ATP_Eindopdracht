import unittest
import random
import BH1750 as BH1750
import A4988 as A4988


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

        # Calculate temperature in Celsius
        resolution = 0.0625
        self.temperature = -magnitude * resolution if sign_bit == 1 else magnitude * resolution

        return self.temperature

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
    

class CurtainController:
    def __init__(self) -> None:
        self.is_closed = False
        self.is_open = False

    def close_curtains(self):
        if not self.is_closed:
            print("Curtains closing.")
            motorController.setDirection(False)
            motorController.takeSteps(420)
            self.is_closed = True
            self.is_open = False

    def open_curtains(self):
        if not self.is_open:
            print("Curtains opening.")
            motorController.setDirection(True)
            motorController.takeSteps(420)
            self.is_open = True
            self.is_closed = False
    

class FanController:
    def __init__(self) -> None:
        self.is_fan_on = False

    def turn_on_fan(self):
        if not self.is_fan_on:
            print("Fan is now on.")
            temperature_sensor.fanOn()
            self.is_fan_on = True
            self.turned_on_once = True 

    def turn_off_fan(self):
        if self.is_fan_on:
            print("Fan is now off.")
            temperature_sensor.fanOff()
            self.is_fan_on = False



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

# Extra so tests dont get to complicated
temperature_sensor = DS18B20Simulator("Woonkamer")
motorController = A4988.A4988Library()


class TestGeautomatiseerdSysteem(unittest.TestCase):

    def setUp(self):
        self.temperature_sensor = DS18B20Simulator("Woonkamer")
        self.motorController = A4988.A4988Library()
        self.curtain_controller = CurtainController()
        self.fan_controller = FanController()
        self.light_sensor = BH1750.BH1750Library()


    def test_system_with_high_temperature_and_low_light(self):
        # Simulate high temperature low light
        self.temperature_sensor.temperature = 30.0
        self.light_sensor.setLightLevel(50)

        threshold_config = {"light_low_threshold": 100, "temperature_low_threshold": 20, "temperature_high_threshold": 24}
        decision = make_decision(self.light_sensor.readLightLevel(), self.temperature_sensor.get_temperature(12), threshold_config)

        self.assertTrue("Close Curtains" in decision)
        self.assertFalse("Turn On Fan" in decision)

        self.assertFalse(self.curtain_controller.is_closed)

        self.assertFalse(self.fan_controller.is_fan_on)

    def test_system_with_low_temperature_and_low_light(self):
        # Simulate low temperature low light
        self.temperature_sensor.temperature = 10.0
        self.light_sensor.setLightLevel(50)

        threshold_config = {"light_low_threshold": 100, "temperature_low_threshold": 20, "temperature_high_threshold": 24}

        decision = make_decision(self.light_sensor.readLightLevel(), self.temperature_sensor.get_temperature(12), threshold_config)

        self.assertTrue("Close Curtains" in decision)
        self.assertTrue("Turn Off Fan" in decision)

        self.assertFalse(self.curtain_controller.is_closed)

        self.assertFalse(self.fan_controller.is_fan_on)

if __name__ == '__main__':
    unittest.main()
