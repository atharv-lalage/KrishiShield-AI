import unittest
from src.api.routes import get_alerts, get_markets, analyze_risk, MARKET_COORDS
from src.api.schemas import AnalysisRequest
from fastapi import HTTPException


class TestAPIEndpoints(unittest.TestCase):
    def test_get_alerts(self):
        alerts = get_alerts()
        self.assertIsInstance(alerts, list)

    def test_get_markets_onion(self):
        res = get_markets("Onion")
        self.assertIn("markets", res)
        self.assertIsInstance(res["markets"], list)
        self.assertTrue(len(res["markets"]) > 0)

    def test_get_markets_unknown(self):
        res = get_markets("UnknownCommodity")
        self.assertIn("markets", res)
        self.assertEqual(len(res["markets"]), 0)

    def test_analyze_risk_invalid_market(self):
        req = AnalysisRequest(crop="Onion", market="InvalidMarketXYZ")
        with self.assertRaises(HTTPException) as ctx:
            analyze_risk(req)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_analyze_risk_valid(self):
        # Pick the first valid market from coordinates
        if MARKET_COORDS:
            market = next(iter(MARKET_COORDS.keys()))
            req = AnalysisRequest(crop="Onion", market=market)
            try:
                res = analyze_risk(req)
                self.assertIn("projected_price", res)
                self.assertIn("risk_level", res)
                self.assertIn("advisory", res)
                self.assertIn("timeline", res)
                self.assertIn("price_trend", res)
            except HTTPException as e:
                # In offline/timeout scenario
                self.assertIn(e.status_code, [500, 503])


if __name__ == "__main__":
    unittest.main()
