import pytest
from tb_to_csv.core.aggregation import process_and_save_metrics
from tb_to_csv.core.event_file_utils import find_event_files

def test_process_and_save_metrics(tmp_path):
    # Create a mock logs directory with event files
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "model1").mkdir()
    (logs_dir / "model1" / "events.out.tfevents.12345").write_text("dummy content")

    # Mock inputs
    prefix_file_mapping = ["test", "shift", "ood"]
    model_name_mapping = {"model1": "Model 1"}
    model_sort_order = ["Model 1"]
    metric_name_mapping = {"Acc": "Accuracy"}
    metric_sort_order = ["Accuracy"]
    confidence = 0.95
    combine_columns = True
    include_step = False

    # Call the function
    process_and_save_metrics(
        str(logs_dir),
        prefix_file_mapping,
        model_name_mapping,
        model_sort_order,
        metric_name_mapping,
        metric_sort_order,
        confidence,
        combine_columns,
        include_step
    )

    # Assert that event files were found
    event_files = find_event_files(str(logs_dir))
    assert len(event_files) > 0

    # TODO: Add more test cases to cover all cases