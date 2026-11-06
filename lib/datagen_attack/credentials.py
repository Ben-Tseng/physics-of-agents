"""Small HMAC edge-credential authority used by the experimental protocol."""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Verification:
    valid: bool
    relation: int | None
    reason: str


class EdgeCredentialAuthority:
    """Issue and verify credentials bound to sender, receiver, and relation."""

    def __init__(self, secret: bytes):
        if not secret:
            raise ValueError("credential secret must not be empty")
        self._secret = secret

    @classmethod
    def from_seed(cls, seed: int):
        secret = hashlib.sha256(f"edge-auth-pilot|{seed}".encode()).digest()
        return cls(secret)

    def _mac(self, body: str) -> str:
        return hmac.new(self._secret, body.encode(), hashlib.sha256).hexdigest()

    def issue(self, sender: int, receiver: int, relation: int, nonce: str) -> str:
        if relation not in (-1, 1):
            raise ValueError("relation must be -1 or +1")
        body = f"{sender}:{receiver}:{relation}:{nonce}"
        return f"{body}:{self._mac(body)}"

    def verify(self, token: str | None, sender: int, receiver: int) -> Verification:
        if not token:
            return Verification(False, None, "missing")
        parts = token.split(":")
        if len(parts) != 5:
            return Verification(False, None, "malformed")
        sender_text, receiver_text, relation_text, nonce, signature = parts
        try:
            token_sender = int(sender_text)
            token_receiver = int(receiver_text)
            relation = int(relation_text)
        except ValueError:
            return Verification(False, None, "malformed")
        if token_sender != sender or token_receiver != receiver:
            return Verification(False, None, "wrong_edge")
        if relation not in (-1, 1):
            return Verification(False, None, "bad_relation")
        body = f"{token_sender}:{token_receiver}:{relation}:{nonce}"
        if not hmac.compare_digest(signature, self._mac(body)):
            return Verification(False, None, "bad_signature")
        return Verification(True, relation, "valid")

    def issue_graph(self, J: np.ndarray, nonce: str) -> dict[tuple[int, int], str]:
        tokens = {}
        senders, receivers = np.nonzero(J)
        for sender, receiver in zip(senders.tolist(), receivers.tolist()):
            tokens[(sender, receiver)] = self.issue(
                sender, receiver, int(J[sender, receiver]), nonce
            )
        return tokens
