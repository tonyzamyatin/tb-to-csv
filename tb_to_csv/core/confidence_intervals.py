import numpy as np
from scipy.stats import t, norm
from typing import List, Tuple, Optional

def compute_confidence_interval(data: List[float], confidence: float = 0.95) -> Optional[Tuple[float, float]]:
    """
    Compute the confidence interval for a list of values.

    Automatically decides whether to use the z-distribution (for large sample sizes)
    or the t-distribution (for small sample sizes).

    Args:
        data (List[float]): A list of numerical values.
        confidence (float): The confidence level for the interval (default is 0.95).

    Returns:
        Optional[Tuple[float, float]]: A tuple containing the mean and the margin of error.
        Returns None if the input data is empty.

    Raises:
        ValueError: If the confidence level is not between 0 and 1.
    """
    if len(data) == 0:
        return None

    if not (0 < confidence < 1):
        raise ValueError("Confidence level must be between 0 and 1.")

    mean = np.mean(data)
    stderr = np.std(data, ddof=1) / np.sqrt(len(data))

    if len(data) > 30:
        # Use z-distribution for large sample sizes
        z_score = norm.ppf((1 + confidence) / 2)
        margin = stderr * z_score
    else:
        # Use t-distribution for small sample sizes
        t_critical = t.ppf((1 + confidence) / 2, df=len(data) - 1)
        margin = stderr * t_critical

    return mean, margin