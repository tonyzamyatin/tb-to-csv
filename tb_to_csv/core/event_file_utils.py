import os
import glob
from typing import Any, Dict, List
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def find_event_files(logs_dir: str) -> List[str]:
    """Find the latest TensorBoard event file per experiment.

    Args:
        logs_dir (str): Path to the logs directory.

    Returns:
        List[str]: List of paths to the latest event files.
    """
    all_event_files = glob.glob(os.path.join(logs_dir, "**/events.out.tfevents.*"), recursive=True)
    all_event_files = sorted(all_event_files, key=os.path.getmtime, reverse=True)

    unique_experiments = {}
    for event_file in all_event_files:
        exp_dir = os.path.dirname(event_file)
        if exp_dir not in unique_experiments:
            unique_experiments[exp_dir] = event_file
    return list(unique_experiments.values())

def extract_metrics(event_file: str) -> Dict[str, Any]:
    """Extract scalar metrics from a given TensorBoard event file.

    Args:
        event_file (str): Path to the TensorBoard event file.

    Returns:
        Dict[str, Any]: Dictionary of extracted metrics.
    """
    event_acc = EventAccumulator(event_file)
    event_acc.Reload()

    available_scalars = event_acc.Tags().get("scalars", [])
    metrics = {}
    last_step = None

    for scalar in available_scalars:
        scalar_events = event_acc.Scalars(scalar)
        if scalar_events:
            metrics[scalar] = scalar_events[-1].value
            last_step = scalar_events[-1].step

    return metrics, last_step

def get_training_duration(event_file: str) -> float:
    """
    Approximate the training duration from a TensorBoard event file.

    Args:
        event_file (str): Path to the TensorBoard event file.

    Returns:
        float: Training duration in seconds.
    """
    event_acc = EventAccumulator(event_file)
    event_acc.Reload()

    # Get all events
    events = event_acc.Tags().get("scalars", [])
    if not events:
        raise ValueError(f"No scalar events found in {event_file}")

    # Extract timestamps from all scalar events
    timestamps = []
    for tag in events:
        scalars = event_acc.Scalars(tag)
        if scalars:
            timestamps.extend([scalar.wall_time for scalar in scalars])

    if not timestamps:
        raise ValueError(f"No timestamps found in {event_file}")

    # Calculate duration
    start_time = min(timestamps)
    end_time = max(timestamps)
    return end_time - start_time
