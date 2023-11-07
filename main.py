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
    def __init__(self, location):
        self.location = location
        self.temperature = 0.0

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
        simulated_temperature = random.uniform(-5, 40)

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



class BH1750Simulator: # Light Sensor
    def __init__(self, location):
        self.light_level = 0 
        self.location = location

    # @location_logger_decorator
    # @timing_decorator
    def get_light_level(self):
        self.light_level = random.uniform(0, 1000)
        return self.light_level
    

class CurtainController: # Curtain controller
    def __init__(self) -> None:
        pass

    def close_curtains(self):
        print("Curtains are closing.")
        return
    
    def open_curtains(self):
        print("Curtains are opening.")
        return
    

class FanController: # Fan Controller
    def __init__(self) -> None:
        pass

    def turn_on_fan(self):
        print("Fan is now on.")
        return
    
    def turn_off_fan(self):
        print("Fan is now off.")
        return
    

# Initialize the sensors and actuators.
temperature_sensor = DS18B20Simulator("Woonkamer")
light_sensor = BH1750Simulator("Woonkamer")
curtain_controller = CurtainController()
fan_controller = FanController()


# Pure functie voor het maken van een keuze.
def make_decision(light_level, temperature, threshold_config):
    # Extract threshold values from the configuration
    light_threshold = threshold_config.get("light_threshold")
    temperature_threshold = threshold_config.get("temperature_threshold")

    decision_lambda = lambda light_level, light_threshold, temperature, temperature_threshold: "Close Curtains and Turn On Fan" if light_level < light_threshold and temperature > temperature_threshold else "Close Curtains and Turn Off Fan" if temperature > temperature_threshold else "Open Curtains and Turn Off Fan"
    return decision_lambda(light_level, light_threshold, temperature, temperature_threshold)


# Recursieve functie voor het uitvoeren van het programma
def mainProgram():
    # Read light level and temperature
    light_level = light_sensor.get_light_level()
    temperature = temperature_sensor.get_temperature(temperature_sensor.generate_12_bit_reading())
    print(light_level, temperature)

    threshold_config = {"light_threshold": 100, "temperature_threshold": 25}

    # Make decision with current light level and temperature
    decision = make_decision(light_level, temperature, threshold_config)

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
    return mainProgram()

mainProgram()