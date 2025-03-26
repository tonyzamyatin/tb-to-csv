import os
import pytest
from unittest.mock import MagicMock, patch
from tb_to_csv.core.event_file_utils import find_event_files, extract_metrics
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def test_find_event_files(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "model1").mkdir()
    (logs_dir / "model1" / "events.out.tfevents.12345").write_text("dummy content")
    event_files = find_event_files(str(logs_dir))
    assert len(event_files) == 1
    assert "events.out.tfevents.12345" in event_files[0]

# TODO: Fix test case
def test_extract_metrics(tmp_path):
    # Create a mock event file
    event_file = tmp_path / "events.out.tfevents.12345"
    event_file.write_text("dummy content")

    # Mock TensorBoard EventAccumulator
    with patch("tb_to_csv.core.event_file_utils.EventAccumulator") as MockEventAccumulator:
        mock_accumulator = MagicMock()
        mock_accumulator.Reload.return_value = None
        mock_accumulator.Scalars.return_value = [
            MagicMock(tag="test/Acc", step=1, value=0.95),
            MagicMock(tag="test/Loss", step=1, value=0.1),
        ]
        MockEventAccumulator.return_value = mock_accumulator

        # Call the function
        metrics, last_step = extract_metrics(str(event_file))

        # Assertions
        assert isinstance(metrics, dict)
        assert metrics["test/Acc"] == 0.95
        assert metrics["test/Loss"] == 0.1
        assert last_step == 1