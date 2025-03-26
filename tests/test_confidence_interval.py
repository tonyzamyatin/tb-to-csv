import pytest
from tb_to_csv.core.confidence_intervals import compute_confidence_interval

def test_compute_confidence_interval_large_sample():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    mean, margin = compute_confidence_interval(data, confidence=0.95)
    assert pytest.approx(mean, 0.1) == 5.5
    assert margin > 0

def test_compute_confidence_interval_small_sample():
    data = [1, 2, 3]
    mean, margin = compute_confidence_interval(data, confidence=0.95)
    assert pytest.approx(mean, 0.1) == 2.0
    assert margin > 0

def test_empty_data():
    assert compute_confidence_interval([], confidence=0.95) is None

def test_invalid_confidence_level():
    with pytest.raises(ValueError):
        compute_confidence_interval([1, 2, 3], confidence=1.5)