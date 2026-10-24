import unittest
from src.ml.model_loader import load_model_and_scaler


class TestMLLoader(unittest.TestCase):
    def test_load_onion_model(self):
        model, scaler = load_model_and_scaler("Onion")
        self.assertIsNotNone(model, "Onion XGBoost model should load successfully")
        self.assertIsNone(scaler, "Onion diff model does not require a scaler")

    def test_load_wheat_model(self):
        model, scaler = load_model_and_scaler("Wheat")
        self.assertIsNotNone(model, "Wheat model should load successfully")
        self.assertIsNotNone(scaler, "Wheat scaler should load successfully")

    def test_load_potato_model(self):
        model, scaler = load_model_and_scaler("Potato")
        self.assertIsNotNone(model, "Potato model should load successfully")

    def test_load_invalid_crop(self):
        model, scaler = load_model_and_scaler("NonExistentCrop123")
        self.assertIsNone(model)
        self.assertIsNone(scaler)


if __name__ == "__main__":
    unittest.main()
