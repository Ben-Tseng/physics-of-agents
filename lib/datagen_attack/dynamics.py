"""Forward dynamics with relationship credentials and external attackers."""

from __future__ import annotations

import hashlib
import json
import random
import re
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from tqdm.auto import tqdm

from ..datagen.dynamics import Replica, _aggregate_spin
from ..datagen.samplers import Pi, message_sampler, spin_sampler
from .credentials import EdgeCredentialAuthority


@dataclass
class AuthenticatedReplica(Replica):
    truth: int = 0
    defense: str = "none"
    attack_budget: int = 0
    attack_degree: int = 4
    attack_seed: int = 0
    inbox_unknown: List[List[str]] = field(default_factory=list)
    envelope_history: List[List[Dict[str, Any]]] = field(default_factory=list)
    spin_error_history: List[List[Dict[str, Any]]] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        if self.truth not in (-1, 1):
            raise ValueError("objective attack pilot requires truth in {-1, +1}")
        if self.defense not in ("none", "downgrade", "drop"):
            raise ValueError("defense must be none, downgrade, or drop")
        if not self.inbox_unknown:
            self.inbox_unknown = [[] for _ in range(self.n)]


def _seed(rep: AuthenticatedReplica, label: str) -> int:
    raw = f"{rep.attack_seed}|{rep.name}|{label}".encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")


def _attack_targets(rep: AuthenticatedReplica):
    rng = np.random.default_rng(_seed(rep, "targets"))
    targets = []
    for _ in range(rep.attack_budget):
        size = min(rep.attack_degree, rep.n)
        targets.append(rng.choice(rep.n, size=size, replace=False).tolist())
    return targets


def _false_message(rep: AuthenticatedReplica) -> str:
    false_letter = "B" if rep.truth > 0 else "A"
    false_text = rep.choices[false_letter] if rep.choices else false_letter
    return (
        f"I favor option {false_letter}: {false_text}. "
        f"The available evidence strongly supports option {false_letter}."
    )


def _route_envelopes(
    rep: AuthenticatedReplica,
    envelopes: List[Dict[str, Any]],
    authority: EdgeCredentialAuthority,
    step_idx: int,
):
    agree = [[] for _ in range(rep.n)]
    disagree = [[] for _ in range(rep.n)]
    unknown = [[] for _ in range(rep.n)]
    by_receiver: Dict[int, List[Dict[str, Any]]] = {}
    logs = []
    for envelope in envelopes:
        by_receiver.setdefault(envelope["receiver"], []).append(envelope)

    for receiver, items in by_receiver.items():
        random.Random(f"{rep.name}|{step_idx}|{receiver}").shuffle(items)
        for envelope in items:
            check = authority.verify(
                envelope.get("credential"), envelope["sender"], receiver
            )
            claimed = int(envelope["claimed_relation"])
            if rep.defense == "none":
                route = "agree" if claimed > 0 else "disagree"
            elif check.valid:
                route = "agree" if check.relation > 0 else "disagree"
            elif rep.defense == "downgrade":
                route = "unknown"
            else:
                route = "drop"

            if route == "agree":
                agree[receiver].append(envelope["message"])
            elif route == "disagree":
                disagree[receiver].append(envelope["message"])
            elif route == "unknown":
                unknown[receiver].append(envelope["message"])

            logs.append({
                **envelope,
                "credential": "present" if envelope.get("credential") else "missing",
                "credential_valid": check.valid,
                "verified_relation": check.relation,
                "verification_reason": check.reason,
                "route": route,
            })
    rep.inbox_agree = agree
    rep.inbox_disagree = disagree
    rep.inbox_unknown = unknown
    rep.envelope_history.append(logs)


def _safe_error_text(exc: Exception, limit: int = 1000) -> str:
    """Keep diagnostics useful without ever persisting an API credential."""
    text = str(exc)
    text = re.sub(r"sk-(?:or-v1-)?[A-Za-z0-9_-]+", "[REDACTED_API_KEY]", text)
    return text[:limit]


def _spin_with_retry(rep, agent, pi, use_inbox, parse_retries=2):
    agree = rep.inbox_agree[agent] if use_inbox else []
    disagree = rep.inbox_disagree[agent] if use_inbox else []
    unknown = rep.inbox_unknown[agent] if use_inbox else []
    parse_errors = []
    for attempt in range(parse_retries + 1):
        try:
            value = spin_sampler(
                rep.personas[agent], rep.statement, agree, disagree, pi,
                mode=rep.mode, choices=rep.choices, messages_unknown=unknown,
            )
            if parse_errors:
                return value, {
                    "kind": "parse_retry",
                    "failed_attempts": len(parse_errors),
                    "attempts": attempt + 1,
                    "details": parse_errors,
                }
            return value, None
        except ValueError as exc:
            parse_errors.append(_safe_error_text(exc))
    return 0, {
        "kind": "parse_failure",
        "failed_attempts": len(parse_errors),
        "attempts": parse_retries + 1,
        "details": parse_errors,
    }


def _spin_phase(replicas, pi, k, executor, step_idx, use_inbox):
    futures: Dict[Future, tuple[int, int, int]] = {}
    for r_idx, rep in enumerate(replicas):
        for agent in range(rep.n):
            for sample in range(k):
                future = executor.submit(
                    _spin_with_retry, rep, agent, pi, use_inbox
                )
                futures[future] = r_idx, agent, sample
    raw = [np.zeros((rep.n, k), dtype=np.int8) for rep in replicas]
    errors = [[] for _ in replicas]
    for future in tqdm(
        as_completed(futures), total=len(futures),
        desc=f"step {step_idx}: spins", leave=False,
    ):
        r_idx, agent, sample = futures[future]
        try:
            value, diagnostic = future.result()
            raw[r_idx][agent, sample] = value
            if diagnostic:
                errors[r_idx].append({
                    "agent": agent,
                    "sample": sample,
                    **diagnostic,
                })
        except Exception as exc:
            raw[r_idx][agent, sample] = 0
            errors[r_idx].append({
                "agent": agent,
                "sample": sample,
                "kind": "request_error",
                "exception_type": type(exc).__name__,
                "detail": _safe_error_text(exc),
            })
    for r_idx, rep in enumerate(replicas):
        spins = [_aggregate_spin(raw[r_idx][agent].tolist()) for agent in range(rep.n)]
        rep.spins_raw_history.append(raw[r_idx])
        rep.spins_history.append(np.asarray(spins, dtype=np.int8))
        rep.spin_error_history.append(errors[r_idx])


def _message_phase(replicas, pi, executor, authority, step_idx):
    futures: Dict[Future, tuple[int, int]] = {}
    recipients = []
    for r_idx, rep in enumerate(replicas):
        rep_recipients: Dict[int, List[int]] = {}
        senders, receivers = np.nonzero(rep.J)
        for sender, receiver in zip(senders.tolist(), receivers.tolist()):
            rep_recipients.setdefault(sender, []).append(receiver)
        recipients.append(rep_recipients)
        for sender in rep_recipients:
            future = executor.submit(
                message_sampler,
                rep.personas[sender], rep.statement,
                rep.inbox_agree[sender], rep.inbox_disagree[sender],
                int(rep.spins_history[-1][sender]), pi,
                mode=rep.mode, choices=rep.choices,
                messages_unknown=rep.inbox_unknown[sender],
            )
            futures[future] = r_idx, sender

    messages = [dict() for _ in replicas]
    for future in tqdm(
        as_completed(futures), total=len(futures),
        desc=f"step {step_idx}: messages", leave=False,
    ):
        r_idx, sender = futures[future]
        try:
            messages[r_idx][sender] = future.result()
        except Exception as exc:
            messages[r_idx][sender] = f"[error: {exc}]"

    for r_idx, rep in enumerate(replicas):
        envelopes = []
        honest_history = {}
        for sender, receiver_list in recipients[r_idx].items():
            for receiver in receiver_list:
                relation = int(rep.J[sender, receiver])
                credential = authority.issue(
                    sender, receiver, relation, f"{rep.name}|{step_idx}"
                )
                message = messages[r_idx][sender]
                envelopes.append({
                    "sender": sender,
                    "receiver": receiver,
                    "sender_type": "honest",
                    "claimed_relation": relation,
                    "credential": credential,
                    "message": message,
                })
                honest_history[(sender, receiver)] = message

        false_message = _false_message(rep)
        for offset, receiver_list in enumerate(_attack_targets(rep)):
            sender = rep.n + offset
            for receiver in receiver_list:
                envelopes.append({
                    "sender": sender,
                    "receiver": receiver,
                    "sender_type": "attacker",
                    "claimed_relation": 1,
                    "credential": None,
                    "message": false_message,
                })
        rep.messages_history.append(dict(sorted(honest_history.items())))
        _route_envelopes(rep, envelopes, authority, step_idx)


def _save(rep, output_dir, meta):
    payload = {
        "meta": {**meta, "name": rep.name, "n": rep.n},
        "personas": rep.personas,
        "statement": rep.statement,
        "choices": rep.choices,
        "truth": rep.truth,
        "J": rep.J.astype(int).tolist(),
        "spins_history": [value.astype(int).tolist() for value in rep.spins_history],
        "spins_raw_history": [
            value.astype(int).tolist() for value in rep.spins_raw_history
        ],
        "spin_error_history": rep.spin_error_history,
        "messages_history": [
            {f"{i},{j}": message for (i, j), message in step.items()}
            for step in rep.messages_history
        ],
        "envelope_history": rep.envelope_history,
    }
    with (output_dir / f"{rep.name}.json").open("w") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def run_authenticated_dynamics(
    replicas: List[AuthenticatedReplica],
    pi: Pi,
    authority: EdgeCredentialAuthority,
    num_steps: int,
    k: int,
    max_workers: int,
    output_dir: str,
    config_meta: Dict[str, Any],
):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        _spin_phase(replicas, pi, k, executor, step_idx=0, use_inbox=False)
        for step in tqdm(range(1, num_steps + 1), desc="steps"):
            _message_phase(replicas, pi, executor, authority, step)
            _spin_phase(replicas, pi, k, executor, step, use_inbox=True)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for rep in replicas:
        _save(rep, out, config_meta)
    return replicas
