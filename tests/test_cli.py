import pytest
from tb_to_csv.cli import load_config, parse_inline_argument

def test_load_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("logs_dir: /path/to/logs\nconfidence: 0.95")
    config = load_config(str(config_path))
    assert config["logs_dir"] == "/path/to/logs"
    assert config["confidence"] == 0.95

def test_parse_inline_argument():
    arg = '{"key": "value"}'
    parsed = parse_inline_argument(arg)
    assert parsed == {"key": "value"}

    with pytest.raises(ValueError):
        parse_inline_argument("invalid")