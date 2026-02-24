import unittest
from hardware.sensor import UltrasonicSensor
from hardware.vision import VisionSystem
from hardware.feedback import FeedbackSystem
import config

class TestMocks(unittest.TestCase):
    def setUp(self):
        # Ensure we are in test mode
        config.TEST_MODE = True
        self.sensor = UltrasonicSensor()
        self.vision = VisionSystem()
        self.feedback = FeedbackSystem()

    def test_sensor_mock(self):
        dist = self.sensor.read()
        self.assertIsInstance(dist, float)
        self.assertGreaterEqual(dist, 20.0)
        self.assertLessEqual(dist, 200.0)

    def test_vision_mock(self):
        # In mock mode, detect should return either empty or list with 'person'
        objs = self.vision.detect(None)
        self.assertIsInstance(objs, list)
        if objs:
            self.assertEqual(objs[0], "person")

    def test_feedback_mock(self):
        # This just verifies it runs without error in mock mode
        self.feedback.alert("Test message", vibrate=True)
        self.feedback.stop()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
