import unittest
from src.core.config import (
    PRIMARY_DATA_FILE,
    FALLBACK_DATA_FILE,
    MODEL_DIR,
    DATA_STORAGE_DIR,
    ALERTS_FILE,
    CURRENT_PETROL,
    CURRENT_DIESEL,
)
from src.core.constants import SUPPORTED_CROPS, DEFAULT_ACTIVE_CROPS


class TestConfig(unittest.TestCase):
    def test_paths_exist(self):
        self.assertTrue(PRIMARY_DATA_FILE.exists(), "Primary data file must exist")
        self.assertTrue(FALLBACK_DATA_FILE.exists(), "Fallback data file must exist")
        self.assertTrue(MODEL_DIR.exists(), "Models directory must exist")
        self.assertTrue(DATA_STORAGE_DIR.exists(), "Storage directory must exist")
        self.assertTrue(ALERTS_FILE.exists(), "Alerts storage file must exist")

    def test_constants(self):
        self.assertGreater(CURRENT_PETROL, 0)
        self.assertGreater(CURRENT_DIESEL, 0)
        self.assertIn("Onion", SUPPORTED_CROPS)
        self.assertIn("Wheat", SUPPORTED_CROPS)
        self.assertIn("Potato", DEFAULT_ACTIVE_CROPS)


if __name__ == "__main__":
    unittest.main()
