#!/usr/bin/env python3
"""Initialize and score a reviewable B2B backlink outreach campaign."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path


SCORE_FIELDS = {
    "relevance_score": (0, 30),
    "editorial_score": (0, 20),
    "feasibility_score": (0, 15),
    "market_score": (0, 15),
    "contact_score": (0, 10),
    "link_value_score": (0, 10),
    "risk_penalty": (0, 50),
}

PROSPECT_FIELDS = [
    "prospect_url",
    "domain",
    "organization",
    "opportunity_type",
    "target_market",
    "evidence",
    "source_url",
    "contact_name",
    "contact_channel",
    "contact_source_url",
    "suggested_asset",
    "suggested_target_url",
    *SCORE_FIELDS.keys(),
    "risk_notes",
    "total_score",
    "grade",
    "status",
    "checked_at",
]

OUTREACH_FIELDS = [
    "domain",
    "contact_name",
    "contact_channel",
    "contact_source_url",
    "subject",
    "message",
    "approval_status",
    "sent_at",
    "follow_up_at",
    "response_status",
    "live_link_url",
    "target_url",
    "anchor_text",
    "link_attribute",
    "notes",
]


def write_csv(path: Path, fields: list[str]) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.DictWriter(handle, fieldnames=fields).writeheader()


def init_campaign(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    campaign_path = output_dir / "campaign.json"
    if campaign_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {campaign_path}")

    write_csv(output_dir / "prospects.csv", PROSPECT_FIELDS)
    write_csv(output_dir / "outreach_log.csv", OUTREACH_FIELDS)
    campaign = {
        "site": args.site,
        "product": args.product,
        "market": args.market,
        "created_at": date.today().isoformat(),
        "execution_boundary": "Research and drafts only; sending or publishing requires approval.",
    }
    campaign_path.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Campaign initialized: {output_dir}")
    return 0


def parse_score(row: dict[str, str], field: str, row_number: int) -> int:
    minimum, maximum = SCORE_FIELDS[field]
    raw = (row.get(field) or "").strip()
    if raw == "":
        raise ValueError(f"Row {row_number}: missing {field}")
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: {field} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise ValueError(
            f"Row {row_number}: {field} must be between {minimum} and {maximum}"
        )
    return value


def grade(total: int, risk_penalty: int) -> str:
    if risk_penalty >= 30 or total < 45:
        return "Reject"
    if total >= 75 and risk_penalty <= 10:
        return "A"
    if total >= 60 and risk_penalty <= 20:
        return "B"
    return "C"


def score_campaign(args: argparse.Namespace) -> int:
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    if output_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {output_path}")

    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        missing = [field for field in SCORE_FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        fieldnames = list(reader.fieldnames or [])
        for field in ("total_score", "grade"):
            if field not in fieldnames:
                fieldnames.append(field)
        rows = []
        for row_number, row in enumerate(reader, start=2):
            scores = {
                field: parse_score(row, field, row_number) for field in SCORE_FIELDS
            }
            positive_total = sum(
                value for field, value in scores.items() if field != "risk_penalty"
            )
            total = max(0, positive_total - scores["risk_penalty"])
            row["total_score"] = str(total)
            row["grade"] = grade(total, scores["risk_penalty"])
            rows.append(row)

    with output_path.open("w", encoding="utf-8-sig", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Scored {len(rows)} prospects: {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize or score a B2B backlink campaign without sending outreach."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create reviewable campaign files")
    init_parser.add_argument("--output-dir", required=True)
    init_parser.add_argument("--site", required=True)
    init_parser.add_argument("--product", required=True)
    init_parser.add_argument("--market", required=True)
    init_parser.set_defaults(func=init_campaign)

    score_parser = subparsers.add_parser("score", help="Calculate score and grade columns")
    score_parser.add_argument("--input", required=True)
    score_parser.add_argument("--output", required=True)
    score_parser.set_defaults(func=score_campaign)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
