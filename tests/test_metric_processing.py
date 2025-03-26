from tb_to_csv.core.metric_processing import categorize_metrics

def test_categorize_metrics():
    metrics = {
        "test/Acc": 0.95,
        "test/Loss": 0.1,
        "shift/Acc": 0.85,
        "ood/Acc": 0.80
    }
    prefix_mapping = ["test", "shift", "ood"]
    categorized = categorize_metrics(metrics, prefix_mapping)
    assert "test" in categorized
    assert "shift" in categorized
    assert "ood" in categorized
    assert categorized["test"]["Acc"] == 0.95