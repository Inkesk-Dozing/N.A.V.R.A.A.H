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
        # In default mock mode (no model), it might detect a person via Haar Cascade
        objs = self.vision.detect(None)
        self.assertIsInstance(objs, list)

    def test_mouse_recognition(self):
        # Verify that we can explicitly mock a 'Computer mouse' detection
        print("\n[MOCK TEST] Simulating detection: Computer mouse")
        objs = self.vision.detect(None, mock_objects=["Computer mouse"])
        self.assertIn("Computer mouse", objs)

    def test_phone_recognition(self):
        # Verify that we can explicitly mock a 'Mobile phone' detection
        print("\n[MOCK TEST] Simulating detection: Mobile phone")
        objs = self.vision.detect(None, mock_objects=["Mobile phone"])
        self.assertIn("Mobile phone", objs)

    def test_watch_recognition(self):
        # Verify that we can explicitly mock a 'Watch' detection
        print("\n[MOCK TEST] Simulating detection: Watch")
        objs = self.vision.detect(None, mock_objects=["Watch"])
        self.assertIn("Watch", objs)

    def test_live_camera_vision(self):
        # This test requires a physical camera and will capture 1 frame
        if not config.ENABLE_REAL_CAMERA:
            self.skipTest("Live camera is disabled in config.py")
        
        print("\n[LIVE TEST] Capturing frame from camera...")
        frame = self.vision.get_frame()
        self.assertIsNotNone(frame, "Failed to capture frame from camera")
        
        objs = self.vision.detect(frame)
        print(f"[LIVE TEST] Objects detected: {objs}")
        
        if objs:
            self.feedback.alert(f"I see a {', '.join(objs)}")
        
        self.assertIsInstance(objs, list)

    def test_feedback_mock(self):
        # This just verifies it runs without error in mock mode
        self.feedback.alert("Test message", vibrate=True)
        self.feedback.stop()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
