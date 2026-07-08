import sys

from ingestion.src import pipeline as pipeline_module
from conftest import make_settings


def test_parse_args_defaults_to_all(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    args = pipeline_module._parse_args()
    assert args.step == "all"


def test_parse_args_accepts_valid_step(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--step", "silver"])
    args = pipeline_module._parse_args()
    assert args.step == "silver"


def _patch_steps(monkeypatch, calls, tmp_path):
    monkeypatch.setattr(pipeline_module, "configure_logging", lambda: None)
    monkeypatch.setattr(pipeline_module, "load_settings", lambda: make_settings(tmp_path))
    monkeypatch.setattr(pipeline_module, "extract_bronze", lambda settings: calls.append("bronze"))
    monkeypatch.setattr(pipeline_module, "build_silver", lambda settings: calls.append("silver"))
    monkeypatch.setattr(pipeline_module, "load_duckdb", lambda settings: calls.append("warehouse"))
    monkeypatch.setattr(pipeline_module, "publish_gold_to_postgres", lambda settings: calls.append("publish"))


def test_main_all_runs_bronze_silver_warehouse_but_not_publish(monkeypatch, tmp_path):
    calls = []
    _patch_steps(monkeypatch, calls, tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--step", "all"])

    pipeline_module.main()

    assert calls == ["bronze", "silver", "warehouse"]


def test_main_publish_only_runs_publish_step(monkeypatch, tmp_path):
    calls = []
    _patch_steps(monkeypatch, calls, tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--step", "publish"])

    pipeline_module.main()

    assert calls == ["publish"]


def test_main_bronze_only_runs_bronze_step(monkeypatch, tmp_path):
    calls = []
    _patch_steps(monkeypatch, calls, tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--step", "bronze"])

    pipeline_module.main()

    assert calls == ["bronze"]
