import unittest
import time
from hardware.sensor import UltrasonicSensor
from hardware.vision import VisionSystem
from hardware.feedback import FeedbackSystem
import config

class TestMocks(unittest.TestCase):
    def setUp(self):
        config.TEST_MODE = True
        self.sensor = UltrasonicSensor()
        self.vision = VisionSystem()
        self.feedback = FeedbackSystem()

    def tearDown(self):
        self.feedback.shutdown()

    # ------------------------------------------------------------------
    # Pipeline / unit tests (silent — no fake audio from fake objects)
    # ------------------------------------------------------------------

    def test_sensor_mock(self):
        """Sensor returns a plausible float distance."""
        dist = self.sensor.read()
        self.assertIsInstance(dist, float)
        self.assertGreaterEqual(dist, 20.0)
        self.assertLessEqual(dist, 200.0)

    def test_vision_pipeline(self):
        """Vision detect() returns a list (even when frame is None)."""
        objs = self.vision.detect(None)
        self.assertIsInstance(objs, list)

    def test_feedback_system(self):
        """FeedbackSystem queues audio and vibrates without raising exceptions."""
        self.feedback.alert("Feedback system check", vibrate=True)
        self.feedback.wait_for_speech()
        self.feedback.stop()
        self.assertTrue(True)

    def test_mock_passthrough(self):
        """detect() passes mock_objects straight through (pipeline sanity check)."""
        fake = ["person on your right", "stairs directly ahead"]
        objs = self.vision.detect(None, mock_objects=fake)
        # Only assert the list is returned intact — no audio from fake labels
        self.assertEqual(objs, fake)

    # ------------------------------------------------------------------
    # Real camera test — captures live frames and speaks what it sees
    # ------------------------------------------------------------------

    def test_live_camera_realtime(self):
        """
        Opens the laptop camera, captures frames for LIVE_SECONDS, runs the
        full YOLO detection pipeline on every frame, and speaks only the
        objects that are actually visible.  A debug window shows bounding boxes.
        """
        if not config.ENABLE_REAL_CAMERA:
            self.skipTest("Live camera is disabled in config.py (ENABLE_REAL_CAMERA=False)")

        LIVE_SECONDS = 8          # How long to run the live loop
        ANNOUNCE_COOLDOWN = 3.0   # Minimum seconds between audio announcements

        print("\n[LIVE] Starting real-time camera analysis...")
        print(f"[LIVE] Running for {LIVE_SECONDS} seconds. Look at the camera!")

        start = time.time()
        last_announced = 0.0
        frames_captured = 0
        all_seen = set()

        while time.time() - start < LIVE_SECONDS:
            frame = self.vision.get_frame()
            if frame is None:
                print("[LIVE] ⚠ Could not read frame — is the camera free?")
                time.sleep(0.5)
                continue

            frames_captured += 1

            # Run full detection pipeline on the real frame
            objs = self.vision.detect(frame)

            # Show bounding-box debug window (closes automatically after loop)
            self.vision.show_frame(frame)

            if objs:
                all_seen.update(objs)
                now = time.time()
                # Only speak when something new is detected (respects cooldown)
                if now - last_announced >= ANNOUNCE_COOLDOWN:
                    print(f"[LIVE] Detected: {objs}")
                    self.feedback.alert(objs)
                    last_announced = now

            time.sleep(0.05)  # ~20 fps polling rate

        # Wait for the last speech to finish before ending the test
        self.feedback.wait_for_speech()

        elapsed = time.time() - start
        print(f"\n[LIVE] Finished after {elapsed:.1f}s — {frames_captured} frames captured.")
        print(f"[LIVE] All objects seen during session: {all_seen if all_seen else 'none detected'}")

        self.assertGreater(frames_captured, 0, "No frames were captured — camera may not be working")


if __name__ == '__main__':
    unittest.main(verbosity=2)
