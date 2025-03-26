import os
import csv
from tb_to_csv.core.csv_writer import save_metrics_to_csv

def test_save_metrics_to_csv(tmp_path):
    all_metrics = {
        "Model A": {"Acc": "0.95 ±0.01", "Loss": "0.1 ±0.02"},
        "Model B": {"Acc": "0.90 ±0.02", "Loss": "0.15 ±0.03"}
    }
    csv_path = tmp_path / "metrics.csv"
    save_metrics_to_csv(all_metrics, str(csv_path))

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["Name", "Acc", "Loss"]
    assert rows[1] == ["Model A", "0.95 ±0.01", "0.1 ±0.02"]
    assert rows[2] == ["Model B", "0.90 ±0.02", "0.15 ±0.03"]