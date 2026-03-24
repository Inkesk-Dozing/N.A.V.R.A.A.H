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

    def test_complex_scene_recognition(self):
        # Verify that the system can handle complex, multi-object mock inputs
        # simulating a real-world scenario (e.g., Man, Clothing, Watch, Mobile phone)
        # Note: The new VisionSystem applies label mapping, so 'Man' -> 'person'
        print("\n[MOCK TEST] Simulating complex scene: Man, Clothing, Watch, Mobile phone")
        # In current logic, mock_objects bypasses the pipeline and returns the list directly.
        # To test the pipeline, we need to pass these through the mapping if desired, but 
        # since detect() just returns mock_objects early, we just verify the pass-through works.
        complex_scene = ["Man", "Clothing", "Watch", "Mobile phone"]
        objs = self.vision.detect(None, mock_objects=complex_scene)
        self.assertEqual(len(objs), 4)
        self.assertIn("Man", objs)
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
