import unittest

EXPECTED_PYTHON = "3.12.3"
EXPECTED_OPENCV = "4.6.0"


class TestRequirements(unittest.TestCase):
    def test_python_version(self):
        import sys
        assert sys.version.startswith(EXPECTED_PYTHON), f"Expected Python {EXPECTED_PYTHON}, but got {sys.version}"

    def test_opencv_version(self):
        try:
            import cv2
        except Exception:
            self.fail("OpenCV (cv2) is not installed")
        assert cv2.__version__ == EXPECTED_OPENCV, f"Expected OpenCV {EXPECTED_OPENCV}, but got {cv2.__version__}"

if __name__ == "__main__":
    unittest.main()
