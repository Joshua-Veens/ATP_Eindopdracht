import unittest
import BH1750 as BH1750
import A4988 as A4988

motorController = A4988.A4988Library()


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


class TestLightSensorIntegration(unittest.TestCase):
    def test_light_sensor_integration(self):
        light_sensor = BH1750.BH1750Library()
        curtain_controller = CurtainController()
        
        threshold_config = {"light_low_threshold": 100, "temperature_low_threshold": 20, "temperature_high_threshold": 24}

        simulated_light_levels = [80, 120, 40]

        for light_level in simulated_light_levels:       
            simulated_temperature = 22 

            decision = make_decision(light_level, simulated_temperature, threshold_config)

            if "Close Curtains" in decision:
                curtain_controller.close_curtains()
            else:
                curtain_controller.open_curtains()

        # Assertions for the CurtainController state
        self.assertTrue(curtain_controller.is_closed)
        self.assertFalse(curtain_controller.is_open)

if __name__ == '__main__':
    unittest.main()