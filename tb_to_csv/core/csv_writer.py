import csv
from typing import Dict, List, Optional

def save_metrics_to_csv(
    all_metrics: Dict[str, Dict[str, str]],
    csv_path: str,
    model_name_mapping: Optional[Dict[str, str]] = None,
    model_sort_order: Optional[List[str]] = None,
    metric_name_mapping: Optional[Dict[str, str]] = None,
    metric_sort_order: Optional[List[str]] = None,
    include_step: Optional[bool] = None,
) -> None:
    """Save collected metrics into a CSV file.

    Args:
        all_metrics (Dict[str, Dict[str, str]]): Dictionary of metrics for each model.
        csv_path (str): Path to the output CSV file.
        model_name_mapping (Optional[Dict[str, str]]): Mapping of model directory names to display names.
        model_sort_order (Optional[List[str]]): Custom sorting order for models in the CSV.
        metric_name_mapping (Optional[Dict[str, str]]): Mapping of metric keys to display names.
        metric_sort_order (Optional[List[str]]): Custom sorting order for metrics in the CSV.
        include_step (Optional[bool]): Whether to include the "Step" key in the CSV.

    Returns:
        None
    """
    if not all_metrics:
        print(f"⚠️  No metrics found. Skipping {csv_path}.")
        return

    # Sort models if a custom sort order is provided
    if model_sort_order:
        sorted_models = []
        missing_models = []
        for model_key in all_metrics.keys():
            if model_sort_order and model_key in model_sort_order:
                sorted_models.append(model_key)
            else:
                missing_models.append(model_key)
                print(f"⚠️  Model '{model_key}' is not included in the model sort order. Adding it to the end.")
        all_metrics_sorted = {model_key: all_metrics[model_key] for model_key in sorted_models + missing_models}
        all_metrics = all_metrics_sorted

    metric_keys = set()
    for metrics in all_metrics.values():
        metric_keys.update(metrics.keys())

    # Remove the "Step" key if not requested
    if not include_step:
        metric_keys.discard("Step")

    # Sort metrics if a custom sort order is provided 
    if metric_sort_order:
        sorted_metrics = []
        missing_metrics = []
        for key in metric_keys:
            if key in metric_sort_order:
                sorted_metrics.append(key)
            else:
                missing_metrics.append(key)
                print(f"⚠️  Metric '{key}' is not included in the metric sort order. Adding it to the end.")
        metric_keys = sorted(sorted_metrics, key=lambda x: metric_sort_order.index(x)) + sorted(missing_metrics)
    else:
        metric_keys = sorted(metric_keys)

    # Write metrics to CSV file
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        header = ["Name"]
        if include_step:
            header.append("Step")
        if metric_name_mapping:
            formatted_keys = []
            for key in metric_keys:
                if key in metric_name_mapping:
                    formatted_keys.append(metric_name_mapping[key])
                else:
                    print(f"⚠️  Metric '{key}' is not included in the metric name mapping. Using the key as-is.")
                    formatted_keys.append(key)
            header += formatted_keys
        else:
            header += metric_keys
        writer.writerow(header)

        for name, metrics in all_metrics.items():
            if model_name_mapping:
                if name in model_name_mapping:
                    name = model_name_mapping[name]
                else:
                    print(f"⚠️  Model '{name}' is not included in the model name mapping. Using the name as-is.")
            row = [name]
            if include_step:
                row.append(metrics.get("Step", "N/A"))
            row += [metrics.get(key, "N/A") for key in metric_keys]
            writer.writerow(row)
