import unittest


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


class TestDecisionMaking(unittest.TestCase):
    def test_light_low_temp_high(self):
        # Test the case when light is below threshold and temperature is high
        threshold_config = {"light_low_threshold": 50, "temperature_low_threshold": 20, "temperature_high_threshold": 30}
        decision = make_decision(40, 35, threshold_config)
        self.assertEqual(decision, "Close Curtains and Turn On Fan")

    def test_light_low_temp_medium(self):
        # Test the case when light is below threshold and temperature is in the medium range
        threshold_config = {"light_low_threshold": 50, "temperature_low_threshold": 20, "temperature_high_threshold": 30}
        decision = make_decision(40, 25, threshold_config)
        self.assertEqual(decision, "Close Curtains and Turn On Fan")

    def test_light_low_temp_low(self):
        # Test the case when light is below threshold and temperature is below the low threshold
        threshold_config = {"light_low_threshold": 50, "temperature_low_threshold": 20, "temperature_high_threshold": 30
        }
        decision = make_decision(40, 15, threshold_config)
        self.assertEqual(decision, "Close Curtains and Turn Off Fan")


if __name__ == '__main__':
    unittest.main()