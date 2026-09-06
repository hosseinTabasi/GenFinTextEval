"""Smoke: ensure study config paths resolve and N formula is documented."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_study_yaml():
    cfg = yaml.safe_load((ROOT / "config" / "study.yaml").read_text())
    n = 10 * len(cfg["variants"]) * 4 * len(cfg["seeds"])
    # 10 events expected; personas file has 4
    assert n >= 200
    assert cfg["falsification"]["margin_belief"] == 0.03
