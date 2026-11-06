import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from lib.datagen_attack.credentials import EdgeCredentialAuthority
from lib.datagen_attack.collect_pilot import load_local_key, load_selected_questions


class EdgeCredentialTest(unittest.TestCase):
    def setUp(self):
        self.authority = EdgeCredentialAuthority.from_seed(7)
        self.token = self.authority.issue(1, 2, 1, "round-1")

    def test_valid_token_is_bound_to_edge_and_relation(self):
        result = self.authority.verify(self.token, 1, 2)
        self.assertTrue(result.valid)
        self.assertEqual(result.relation, 1)

    def test_replay_on_another_receiver_fails(self):
        result = self.authority.verify(self.token, 1, 3)
        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "wrong_edge")

    def test_tampering_fails(self):
        body, signature = self.token.rsplit(":", 1)
        tampered = f"{body}:{'0' * len(signature)}"
        result = self.authority.verify(tampered, 1, 2)
        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "bad_signature")

    def test_local_key_loader_reads_only_expected_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text("OTHER=ignored\nOPENROUTER_API_KEY=test-only\n")
            with patch.dict(os.environ, {}, clear=True):
                load_local_key(path)
                self.assertEqual(os.environ["OPENROUTER_API_KEY"], "test-only")
                self.assertNotIn("OTHER", os.environ)

    def test_local_key_loader_can_select_mistral_key(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text(
                "OPENROUTER_API_KEY=ignored\nMISTRAL_API_KEY=mistral-test-only\n"
            )
            with patch.dict(os.environ, {}, clear=True):
                load_local_key(path, variable="MISTRAL_API_KEY")
                self.assertEqual(os.environ["MISTRAL_API_KEY"], "mistral-test-only")
                self.assertNotIn("OPENROUTER_API_KEY", os.environ)

    def test_declared_question_ids_preserve_order(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "questions.jsonl"
            path.write_text(
                '{"qid":"q1","question":"one"}\n'
                '{"qid":"q2","question":"two"}\n'
            )
            rows = load_selected_questions(path, question_ids="q2,q1")
            self.assertEqual([row["qid"] for row in rows], ["q2", "q1"])

    def test_declared_question_ids_fail_on_unknown_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "questions.jsonl"
            path.write_text('{"qid":"q1","question":"one"}\n')
            with self.assertRaisesRegex(ValueError, "unknown qids"):
                load_selected_questions(path, question_ids="q2")


if __name__ == "__main__":
    unittest.main()
