import unittest
from unittest.mock import patch

from lib.datagen_attack.dynamics import _safe_error_text, _spin_with_retry


class _Replica:
    inbox_agree = [[]]
    inbox_disagree = [[]]
    inbox_unknown = [[]]
    personas = ["persona"]
    statement = "question"
    mode = "objective"
    choices = {"A": "one", "B": "two"}


class AttackSpinDiagnosticsTest(unittest.TestCase):
    def test_success_after_parse_retry_is_recorded(self):
        with patch(
            "lib.datagen_attack.dynamics.spin_sampler",
            side_effect=[ValueError("bad format"), 1],
        ):
            value, diagnostic = _spin_with_retry(_Replica(), 0, None, False)
        self.assertEqual(value, 1)
        self.assertEqual(diagnostic["kind"], "parse_retry")
        self.assertEqual(diagnostic["failed_attempts"], 1)

    def test_exhausted_parse_retries_are_recorded(self):
        with patch(
            "lib.datagen_attack.dynamics.spin_sampler",
            side_effect=ValueError("bad format"),
        ):
            value, diagnostic = _spin_with_retry(
                _Replica(), 0, None, False, parse_retries=2
            )
        self.assertEqual(value, 0)
        self.assertEqual(diagnostic["kind"], "parse_failure")
        self.assertEqual(diagnostic["failed_attempts"], 3)

    def test_error_text_redacts_api_keys(self):
        text = _safe_error_text(RuntimeError("failed sk-or-v1-secret123 now"))
        self.assertNotIn("secret123", text)
        self.assertIn("[REDACTED_API_KEY]", text)


if __name__ == "__main__":
    unittest.main()
