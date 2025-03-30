import argparse
import yaml
import ast
from typing import Any, Dict, List, Optional, Union
from tb_to_csv.core.aggregation import process_and_save_metrics


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Parsed configuration as a dictionary.
    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def parse_inline_argument(arg_value: str) -> Union[Dict[str, Any], List[Any]]:
    """Parse an inline dictionary or list argument.

    Args:
        arg_value (str): The string representation of a dictionary or list.

    Returns:
        Union[Dict[str, Any], List[Any]]: The parsed dictionary or list.

    Raises:
        ValueError: If the argument is not a valid dictionary or list.
    """
    try:
        return ast.literal_eval(arg_value)
    except (ValueError, SyntaxError):
        raise ValueError(f"Invalid inline argument: {arg_value}. Must be a valid dictionary or list.")


def main() -> None:
    """Main function to parse arguments, load configuration, and process metrics."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate CSV files from TensorBoard event files, with confidence intervals for metrics.\n\n"
            "Assumed Directory Structure:\n"
            "logs_dir/\n"
            "  model_name/\n"
            "    run_name/\n"
            "      events.out.tfevents.*\n\n"
            "For example, 'logs/resnet18/mc_dropout/seed_42/events.out.tfevents.12345'.\n"
            "Metrics tracked by TensorBoard must include a prefix in their names as 'prefix/metric_name'.\n"
            "For example, 'test/Acc', 'shift/ECE', or 'ood/AUROC'."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c", "--config",
        type=str,
        help="Path to the YAML configuration file. CLI arguments override values in the config."
    )
    parser.add_argument(
        "--logs-dir",
        type=str,
        help="Path to the logs directory. This argument is required if not specified in the config."
    )
    parser.add_argument(
        "--prefix-file-mapping",
        type=str,
        help=(
            "Dictionary or list for prefix mapping to output file names:\n"
            "  - A list of prefixes (e.g., '[\"test\", \"shift\", \"ood\"]').\n"
            "    Metrics for each prefix are saved to '<prefix>_metrics.csv'.\n"
            "  - A dictionary mapping prefixes to custom file names (e.g., '{\"test\": \"test_metrics.csv\"}').\n"
            "If not provided, all metrics are saved to a single CSV file."
        )
    )
    parser.add_argument(
        "--model-name-mapping",
        type=str,
        help=(
            "Dictionary mapping model directory names to display names.\n"
            "For example: '{\"mc_dropout\": \"MC Dropout\", \"ensemble\": \"Deep Ensemble\"}'.\n"
            "If not provided, directory names are used as model names in the CSV."
        )
    )
    parser.add_argument(
        "--model-sort-order",
        type=str,
        help=(
            "Inline list specifying the custom sorting order for models in the CSV.\n"
            "For example: '[\"standard\", \"mc_dropout\", \"ensemble\"]'.\n"
            "If not provided, models are written in the default order."
        )
    )
    parser.add_argument(
        "--metric-name-mapping",
        type=str,
        help=(
            "Dictionary mapping metric keys to display names.\n"
            "For example: '{\"test/Acc\": \"Accuracy\", \"shift/ECE\": \"Expected Calibration Error\"}'.\n"
            "If not provided, metric keys are used as column headers in the CSV."
        )
    )
    parser.add_argument(
        "--metric-sort-order",
        type=str,
        help=(
            "Inline list specifying the custom sorting order for metrics in the CSV.\n"
            "For example: '[\"test/Acc\", \"shift/ECE\", \"ood/AUROC\"]'.\n"
            "If not provided, metrics are written in alphabetical order."
        )
    )
    parser.add_argument(
        "--compute-ci",
        action="store_true",
        help="Compute confidence intervals for aggregated metrics. Default: False."
    )
    parser.add_argument(
        "--confidence",
        type=float,
        help="Confidence level for intervals. Default: 0.95 if not specified in the config."
    )
    parser.add_argument(
        "--separate-columns",
        action="store_true",
        help="Use separate columns for mean and CI. Default: False."
    )
    parser.add_argument(
        "--include-step",
        action="store_true",
        help="Include the 'Step' key in the CSV. Default: False."
    )
    args = parser.parse_args()

    # Load configuration from YAML file if provided
    config: Dict[str, Any] = {}
    if args.config:
        config = load_config(args.config)

    # Determine logs_dir
    logs_dir: str = args.logs_dir or config.get("logs_dir", "")
    if not logs_dir:
        raise ValueError("❌ The logs directory must be specified either via --logs-dir or in the config file.")

    # Parse prefix_mapping
    prefix_file_mapping: Optional[Union[Dict[str, str], List[str]]] = None
    if args.prefix_file_mapping:
        prefix_file_mapping = parse_inline_argument(args.prefix_file_mapping)
    else:
        prefix_file_mapping = config.get("prefix_file_mapping", None)

    # Parse model_name_mapping
    model_name_mapping: Dict[str, str] = {}
    if args.model_name_mapping:
        model_name_mapping = parse_inline_argument(args.model_name_mapping)
    else:
        model_name_mapping = config.get("model_name_mapping", {})

    # Parse model_sort_order
    model_sort_order: Optional[List[str]] = None
    if args.model_sort_order:
        model_sort_order = parse_inline_argument(args.model_sort_order)
    else:
        model_sort_order = config.get("model_sort_order", None)

    # Parse metric_name_mapping
    metric_name_mapping: Dict[str, str] = {}
    if args.metric_name_mapping:
        metric_name_mapping = parse_inline_argument(args.metric_name_mapping)
    else:
        metric_name_mapping = config.get("metric_name_mapping", {})

    # Parse metric_sort_order
    metric_sort_order: Optional[List[str]] = None
    if args.metric_sort_order:
        metric_sort_order = parse_inline_argument(args.metric_sort_order)
    else:
        metric_sort_order = config.get("metric_sort_order", None)

    # Determine other parameters
    compute_ci: bool = args.compute_ci or config.get("compute_ci", False)
    confidence: float = args.confidence or config.get("confidence", 0.95)
    combine_columns: bool = not args.separate_columns if args.separate_columns is not None else config.get("combine_columns", True)
    include_step: bool = args.include_step or config.get("include_step", False)

    # Process and save metrics
    process_and_save_metrics(
        logs_dir, 
        prefix_file_mapping,
        model_name_mapping,
        model_sort_order,
        metric_name_mapping,
        metric_sort_order,
        compute_ci,
        confidence,
        combine_columns,
        include_step
    )


if __name__ == "__main__":
    main()