from __future__ import annotations

import argparse
import logging

from ingestion.src.bronze import extract_bronze
from ingestion.src.config import load_settings
from ingestion.src.logging_utils import configure_logging
from ingestion.src.publish import publish_gold_to_postgres
from ingestion.src.silver import build_silver
from ingestion.src.warehouse import load_duckdb

LOGGER = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    args = _parse_args()
    settings = load_settings()

    LOGGER.info("pipeline_started step=%s warehouse=%s", args.step, settings.warehouse_path)

    if args.step in ("bronze", "all"):
        extract_bronze(settings)

    if args.step in ("silver", "all"):
        build_silver(settings)

    if args.step in ("warehouse", "all"):
        load_duckdb(settings)

    if args.step == "publish":
        publish_gold_to_postgres(settings)

    LOGGER.info("pipeline_finished step=%s", args.step)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Investment batch data pipeline")
    parser.add_argument(
        "--step",
        choices=["bronze", "silver", "warehouse", "publish", "all"],
        default="all",
        help="Pipeline step to execute.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
