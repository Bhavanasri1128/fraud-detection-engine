import os
import unittest
from database import init_db
from engine import score_transaction, resolve_alert

class TestFraudEngine(unittest.TestCase):
    def setUp(self):
        self.db = "test_fraud.db"
        if os.path.exists(self.db):
            os.remove(self.db)
        init_db(self.db)

    def tearDown(self):
        if os.path.exists(self.db):
            os.remove(self.db)

    def test_approve_normal(self):
        score, decision, _ = score_transaction("TOK_101", 5000, "DEV_OK", self.db)
        self.assertEqual(decision, "Approve")
        self.assertEqual(score, 0)

    def test_decline_over_limit(self):
        score, decision, _ = score_transaction("TOK_101", 120000, "DEV_BAD", self.db)
        self.assertEqual(decision, "Decline")

    def test_cross_bank_threat_sharing(self):
        score_transaction("TOK_101", 120000, "DEV_BAD", self.db)
        resolve_alert(1, is_fraud=True, db_name=self.db)

        score, decision, reason = score_transaction("TOK_102", 1000, "DEV_BAD", self.db)
        self.assertEqual(decision, "Verify")
        self.assertIn("HDFC Bank", reason)

if __name__ == "__main__":
    unittest.main()
