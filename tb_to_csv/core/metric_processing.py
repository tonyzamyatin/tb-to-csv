def categorize_metrics(metrics, prefix_mapping):
    """
    Categorize metrics into categories based on the prefix mapping.

    Args:
        metrics (Dict[str, float]): Dictionary of metric names and values.
        prefix_mapping (List[str] or Dict[str, str]): Mapping of prefixes to categories.

    Returns:
        Dict[str, Dict[str, float]]: Categorized metrics.
    """
    if isinstance(prefix_mapping, list):
        # Use the prefix directly as the category
        categorized_metrics = {prefix: {} for prefix in prefix_mapping}
        for key, value in metrics.items():
            for prefix in prefix_mapping:
                if key.startswith(f"{prefix}/"):
                    categorized_metrics[prefix][key.replace(f"{prefix}/", "")] = value
    elif isinstance(prefix_mapping, dict):
        # Use the dictionary values as the category
        categorized_metrics = {category: {} for category in prefix_mapping.values()}
        for key, value in metrics.items():
            for prefix, category in prefix_mapping.items():
                if key.startswith(f"{prefix}/"):
                    categorized_metrics[category][key.replace(f"{prefix}/", "")] = value
    else:
        raise ValueError("prefix_mapping must be a list or a dictionary.")

    return categorized_metrics
