import os
import yaml
from tb_to_csv.param_count import main
from dummy_models import DummyModel

def test_param_count(tmp_path):
    # Create a temporary YAML configuration file
    config = {
        "TestDummyModel": {
            "class_path": "dummy_models.DummyModel",
            "init_args": {
                "input_size": 10,
                "hidden_size": 20,
                "output_size": 5
            }
        }
    }
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as file:
        yaml.dump(config, file)

    # Define the output CSV path
    output_path = tmp_path / "output.csv"

    # Run the main function
    main(config_path, output_path)

    # Manually calculate the expected parameter count
    dummy_model = DummyModel(input_size=10, hidden_size=20, output_size=5)
    expected_param_count = sum(p.numel() for p in dummy_model.parameters())

    # Verify the output CSV
    with open(output_path, "r") as file:
        lines = file.readlines()

    assert lines[0].strip() == "TestDummyModel"  # Validate the header
    assert int(lines[1].strip()) == expected_param_count  # Validate the parameter count