import BH1750 as BH1750
import A4988 as A4988
import time
import random
from datetime import datetime
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time_microseconds = (end_time - start_time) * 1_000_000  # Convert to microseconds
        print(f"{func.__name__} duurde {execution_time_microseconds:.2f} microseconden")
        return result
    return wrapper

def location_logger_decorator(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        print(f"[LOCATION LOG] Locatie: {self.location}")
        return result
    return wrapper


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


    
# Pure functie om een keuze te maken.
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


# Initialize the sensors and actuators.
temperature_sensor = DS18B20Simulator("Woonkamer")
curtain_controller = CurtainController()
motorController = A4988.A4988Library()
fan_controller = FanController()

lightSensor = BH1750.BH1750Library()


def simulator():
    while True:
        # Read light level and temperature
        temperature = temperature_sensor.get_temperature(temperature_sensor.generate_12_bit_reading())
        lightSensor.generateSimulatedLightLevel()
        lightLevel = lightSensor.readLightLevel()
        print(f"Temperature: {temperature}, light level: {lightLevel}")

        threshold_config = {"light_low_threshold": 100, "temperature_low_threshold": 20, "temperature_high_threshold": 24 }

        # Make decision with current light level and temperature
        decision = make_decision(lightLevel, temperature, threshold_config)

        # Execute decision
        if "Close Curtains" in decision:
            curtain_controller.close_curtains()
        else:
            curtain_controller.open_curtains()

        if "Turn On Fan" in decision:
            fan_controller.turn_on_fan()
        else:
            fan_controller.turn_off_fan()

        # Wait until next measurement
        time.sleep(1)  # 60 = 1 min

        # Print for clear terminal readings
        print("")

simulator()