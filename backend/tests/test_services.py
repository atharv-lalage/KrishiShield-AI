import unittest
from src.services.risk_service import evaluate_risk_profile, generate_price_trend
from src.services.alert_service import load_alerts


class TestServices(unittest.TestCase):
    def test_evaluate_risk_profile_high(self):
        score, level, msg, advisory = evaluate_risk_profile(35.0)
        self.assertEqual(level, "HIGH RISK")
        self.assertGreater(score, 60)
        self.assertEqual(advisory["color"], "error")
        self.assertTrue(len(advisory["steps"]) > 0)

    def test_evaluate_risk_profile_moderate(self):
        score, level, msg, advisory = evaluate_risk_profile(15.0)
        self.assertEqual(level, "MODERATE RISK")
        self.assertEqual(advisory["color"], "warning")

    def test_evaluate_risk_profile_dropping(self):
        score, level, msg, advisory = evaluate_risk_profile(-10.0)
        self.assertEqual(level, "LOW RISK")
        self.assertEqual(advisory["color"], "success")

    def test_generate_price_trend(self):
        trend = generate_price_trend(2500, 2700)
        self.assertEqual(len(trend), 6)
        self.assertEqual(trend[-2]["price"], 2500)
        self.assertEqual(trend[-1]["price"], 2700)

    def test_load_alerts(self):
        alerts = load_alerts()
        self.assertIsInstance(alerts, list)


if __name__ == "__main__":
    unittest.main()
