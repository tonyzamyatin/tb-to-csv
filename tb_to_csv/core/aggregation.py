from typing import Dict, List
import os
from typing import Optional, Union
from tb_to_csv.core.event_file_utils import extract_metrics, find_event_files
from tb_to_csv.core.metric_processing import categorize_metrics
from tb_to_csv.core.csv_writer import save_metrics_to_csv
from tb_to_csv.core.confidence_intervals import compute_confidence_interval


def aggregate_metrics_by_model(event_files, prefix_mapping):
    """Aggregate metrics across runs for each model."""
    model_metrics = {}

    for event_file in event_files:
        # Extract model_name and run_name from the directory structure
        relative_path = os.path.relpath(event_file)
        model_key, run_name = relative_path.split(os.sep)[-3:-1]

        metrics, _ = extract_metrics(event_file)
        if not metrics:
            print(f"⚠️ No metrics extracted from {event_file}. Skipping...")
            continue

        # Initialize the model's metrics dictionary if not already present
        if model_key not in model_metrics:
            if isinstance(prefix_mapping, list):
                model_metrics[model_key] = {prefix: {} for prefix in prefix_mapping}
            elif isinstance(prefix_mapping, dict):
                model_metrics[model_key] = {category: {} for category in prefix_mapping.values()}
            else:
                raise ValueError("prefix_mapping must be a list or a dictionary.")

        # Categorize metrics into the appropriate categories
        categorized_metrics = categorize_metrics(metrics, prefix_mapping)

        # Aggregate metrics for each category
        for category, category_metrics in categorized_metrics.items():
            for key, value in category_metrics.items():
                if key not in model_metrics[model_key][category]:
                    model_metrics[model_key][category][key] = []
                model_metrics[model_key][category][key].append(value)
        
    return model_metrics


def compute_ci_by_model(model_metrics, confidence=0.95, combine_columns=True):
    """Compute confidence intervals for metrics across runs for each model."""
    ci_model_metrics = {}

    for model_name, categories in model_metrics.items():
        ci_model_metrics[model_name] = {}
        for category, metrics in categories.items():
            ci_metrics = {}
            for key, values in metrics.items():
                mean, margin = compute_confidence_interval(values, confidence)
                if combine_columns:
                    ci_metrics[key] = f"{mean:.3f} ±{margin:.3f}"
                else:
                    ci_metrics[f"{key} Mean"] = f"{mean:.3f}"
                    ci_metrics[f"{key} ± CI"] = f"{margin:.3f}"
            ci_model_metrics[model_name][category] = ci_metrics

    return ci_model_metrics


def process_and_save_metrics(
    logs_dir: str,
    prefix_file_mapping: Optional[Union[Dict[str, str], List[str]]],
    model_name_mapping: Dict[str, str],
    model_sort_order: Optional[List[str]],
    metric_name_mapping: Dict[str, str],
    metric_sort_order: Optional[List[str]],
    confidence: float,
    combine_columns: bool,
    include_step: bool,
) -> None:
    """Process metrics, compute confidence intervals, and save to CSV files.

    Args:
        logs_dir (str): Path to the logs directory containing event files.
        prefix_file_mapping (Optional[Union[Dict[str, str], List[str]]]): Mapping of prefixes to file names or a list of prefixes.
        model_name_mapping (Dict[str, str]): Mapping of model directory names to display names.
        model_sort_order (Optional[List[str]]): Custom sorting order for models in the CSV.
        metric_name_mapping (Dict[str, str]): Mapping of metric keys to display names.
        metric_sort_order (Optional[List[str]]): Custom sorting order for metrics in the CSV.
        confidence (float): Confidence level for intervals.
        combine_columns (bool): Whether to combine mean and CI into one column.
        include_step (bool): Whether to include the "Step" key in the CSV.

    Returns:
        None
    """
    # Find all event files
    event_files = find_event_files(logs_dir)
    if not event_files:
        raise FileNotFoundError(f"❌ No event files found in logs directory {logs_dir}")

    # Aggregate metrics by model
    model_metrics = aggregate_metrics_by_model(event_files, prefix_file_mapping)

    # Compute confidence intervals for each model
    ci_model_metrics = compute_ci_by_model(model_metrics, confidence, combine_columns)

    # Sort models if a custom sort order is provided
    if model_sort_order:
        ci_model_metrics_sorted = {
            model_key: ci_model_metrics[model_key]
            for model_key in model_sort_order
            if model_key in ci_model_metrics
        }
        ci_model_metrics = ci_model_metrics_sorted

    # Save metrics to CSV files
    if prefix_file_mapping:
        if isinstance(prefix_file_mapping, list):
            prefix_file_mapping = {prefix: f"{prefix}_metrics.csv" for prefix in prefix_file_mapping}

        for prefix, file_name in prefix_file_mapping.items():
            category_metrics = {}
            category_metrics = {
                model_name: metrics.get(prefix, {})
                for model_name, metrics in ci_model_metrics.items()
            }
            csv_path = os.path.join(logs_dir, file_name)
            save_metrics_to_csv(category_metrics, csv_path, model_name_mapping, model_sort_order, metric_name_mapping, metric_sort_order, include_step=include_step)
            print(f"✅ Saved {csv_path} with {len(category_metrics)} models.")
    else:
        all_metrics = {
            model_name: {key: value for category_metrics in metrics.values() for key, value in category_metrics.items()}
            for model_name, metrics in ci_model_metrics.items()
        }
        csv_path = os.path.join(logs_dir, "all_metrics.csv")
        save_metrics_to_csv(all_metrics, csv_path, model_name_mapping, model_sort_order, metric_name_mapping, metric_sort_order, include_step=include_step)
        print(f"✅ Saved {csv_path} with {len(all_metrics)} models.")