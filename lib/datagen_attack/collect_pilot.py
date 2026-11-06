"""Run a small objective live-model pilot with authenticated relationships."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ..datagen.collect_energy import load_canonical_personas, load_questions, model_slug
from ..datagen.graph import sample_J_num_edges_symmetric
from ..datagen.utils import make_mock_pi
from ..datagen_frontier.dashscope import make_dashscope_pi
from ..datagen_frontier.deepinfra import make_deepinfra_pi
from ..datagen_frontier.mistral import make_mistral_pi
from ..datagen_frontier.openrouter import make_openrouter_pi
from .credentials import EdgeCredentialAuthority
from .dynamics import AuthenticatedReplica, run_authenticated_dynamics


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--backend", choices=("openrouter", "deepinfra", "dashscope", "mistral"),
        default="openrouter",
    )
    parser.add_argument("--model", default="qwen/qwen3.5-9b")
    parser.add_argument("--provider", default="DeepInfra")
    parser.add_argument("--defense", choices=("none", "downgrade", "drop"), default="none")
    parser.add_argument("--attack-budget", type=int, default=0)
    parser.add_argument("--attack-degree", type=int, default=4)
    parser.add_argument("--num-agents", type=int, default=8)
    parser.add_argument("--num-edges", type=int, default=28)
    parser.add_argument("--num-steps", type=int, default=2)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--question-file", default="data/obj/test.jsonl")
    parser.add_argument(
        "--question-ids",
        help="Comma-separated qids. Preserves the requested order and overrides --limit.",
    )
    parser.add_argument("--trajectories", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--request-timeout", type=float, default=60.0)
    parser.add_argument("--api-max-retries", type=int, default=4)
    parser.add_argument("--min-request-interval", type=float, default=0.0)
    parser.add_argument(
        "--service-tier", choices=("standard", "priority", "flex"),
        default="standard",
        help="DeepInfra scheduling tier; ignored by other backends.",
    )
    parser.add_argument(
        "--deepinfra-fail-fast", action="store_true",
        help="Return an immediate 429 instead of queueing when DeepInfra is busy.",
    )
    parser.add_argument("--max-workers", type=int, default=8)
    parser.add_argument("--output-dir")
    parser.add_argument("--mock", action="store_true")
    return parser.parse_args()


def load_selected_questions(path, limit=1, question_ids=None):
    """Load a declared question set; fail rather than silently changing the sample."""
    requested = []
    if question_ids:
        requested = [value.strip() for value in question_ids.split(",") if value.strip()]
        if len(requested) != len(set(requested)):
            raise ValueError("--question-ids contains duplicates")
    questions = load_questions(path, None if requested else limit)
    if not requested:
        return questions
    by_id = {question["qid"]: question for question in questions}
    missing = [qid for qid in requested if qid not in by_id]
    if missing:
        raise ValueError(f"unknown qids in {path}: {', '.join(missing)}")
    return [by_id[qid] for qid in requested]


def load_local_key(path=Path(".env"), variable="OPENROUTER_API_KEY"):
    """Load one explicitly named API key from the ignored local env file."""
    if os.environ.get(variable) or not path.exists():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == variable:
            os.environ[variable] = value.strip().strip("'\"")
            return


def main():
    args = parse_args()
    if args.num_edges % 2:
        raise ValueError("--num-edges counts nonzero symmetric entries and must be even")
    if args.attack_budget < 0 or args.attack_degree < 0:
        raise ValueError("attack budget and degree must be nonnegative")
    if args.api_max_retries < 0:
        raise ValueError("API max retries must be nonnegative")
    if args.min_request_interval < 0:
        raise ValueError("minimum request interval must be nonnegative")

    questions = load_selected_questions(
        args.question_file, args.limit, args.question_ids
    )
    personas = load_canonical_personas("data/obj/personas.json", args.num_agents)
    import numpy as np

    rng = np.random.default_rng(args.seed)
    J = sample_J_num_edges_symmetric(args.num_agents, args.num_edges, rng)
    replicas = []
    for question in questions:
        truth = {"A": 1, "B": -1}[question["answer"]]
        for repeat in range(args.trajectories):
            replicas.append(AuthenticatedReplica(
                name=f"{question['qid']}__J0__rep{repeat:02d}",
                personas=list(personas),
                statement=question["question"],
                J=J.copy(),
                mode="objective",
                choices=question["choices"],
                truth=truth,
                defense=args.defense,
                attack_budget=args.attack_budget,
                attack_degree=args.attack_degree,
                attack_seed=args.seed,
            ))

    if args.mock:
        pi = make_mock_pi(args.seed)
    elif args.backend == "dashscope":
        load_local_key(variable="DASHSCOPE_API_KEY")
        load_local_key(variable="DASHSCOPE_BASE_URL")
        pi = make_dashscope_pi(
            model=args.model,
            temperature=args.temperature,
            max_retries=args.api_max_retries,
            request_timeout=args.request_timeout,
            min_request_interval=args.min_request_interval,
            enable_thinking=False,
        )
    elif args.backend == "deepinfra":
        load_local_key(variable="DEEPINFRA_API_KEY")
        pi = make_deepinfra_pi(
            model=args.model,
            temperature=args.temperature,
            max_retries=args.api_max_retries,
            request_timeout=args.request_timeout,
            min_request_interval=args.min_request_interval,
            service_tier=(None if args.service_tier == "standard" else args.service_tier),
            fail_fast=args.deepinfra_fail_fast,
        )
    elif args.backend == "mistral":
        load_local_key(variable="MISTRAL_API_KEY")
        pi = make_mistral_pi(
            model=args.model,
            temperature=args.temperature,
            max_retries=args.api_max_retries,
            request_timeout=args.request_timeout,
            min_request_interval=args.min_request_interval,
        )
    else:
        load_local_key(variable="OPENROUTER_API_KEY")
        pi = make_openrouter_pi(
            model=args.model,
            temperature=args.temperature,
            reasoning="none",
            provider=args.provider,
            allow_fallbacks=False,
            data_collection="deny",
            request_timeout=args.request_timeout,
            max_retries=args.api_max_retries,
            min_request_interval=args.min_request_interval,
        )

    output_dir = args.output_dir or (
        f"data/attack_pilot/{model_slug(args.model)}/{args.defense}"
        f"__attack{args.attack_budget}__seed{args.seed}"
    )
    estimated_calls = len(replicas) * args.num_agents * (
        args.k + args.num_steps * (1 + args.k)
    )
    meta = {
        "experiment": "authenticated_edge_attack_pilot",
        "backend": "mock" if args.mock else args.backend,
        "model": "mock" if args.mock else args.model,
        "provider": "mock" if args.mock else (
            "Mistral AI" if args.backend == "mistral" else (
                "Alibaba Cloud Model Studio" if args.backend == "dashscope" else (
                    "DeepInfra direct" if args.backend == "deepinfra" else args.provider
                )
            )
        ),
        "allow_fallbacks": False,
        "data_collection": "deny",
        "reasoning": (
            "none" if args.backend in ("openrouter", "deepinfra", "dashscope")
            else "provider_default"
        ),
        "temperature": args.temperature,
        "request_timeout_seconds": args.request_timeout,
        "api_max_retries": args.api_max_retries,
        "min_request_interval_seconds": args.min_request_interval,
        "service_tier": args.service_tier if args.backend == "deepinfra" else None,
        "deepinfra_fail_fast": (
            args.deepinfra_fail_fast if args.backend == "deepinfra" else None
        ),
        "max_workers": args.max_workers,
        "num_agents": args.num_agents,
        "num_edges": args.num_edges,
        "num_steps": args.num_steps,
        "k": args.k,
        "defense": args.defense,
        "attack_budget": args.attack_budget,
        "attack_degree": args.attack_degree,
        "seed": args.seed,
        "question_file": args.question_file,
        "question_ids": [question["qid"] for question in questions],
        "estimated_api_calls": estimated_calls,
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(
        f"[attack-pilot] replicas={len(replicas)} calls={estimated_calls} "
        f"model={meta['model']} defense={args.defense} attack={args.attack_budget} "
        f"-> {output_dir}",
        flush=True,
    )
    authority = EdgeCredentialAuthority.from_seed(args.seed)
    run_authenticated_dynamics(
        replicas, pi, authority, args.num_steps, args.k, args.max_workers,
        output_dir, meta,
    )


if __name__ == "__main__":
    main()
