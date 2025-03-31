import importlib
import csv
import yaml
from torch_uncertainty.models.resnet import (
    batched_resnet,
    packed_resnet,
    resnet,
    ensemble_resnet
)
from torch_uncertainty.models.wrappers.mc_dropout import mc_dropout

def instantiate_model(class_path, init_args):
    """Dynamically import and instantiate a model."""
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    model_class = getattr(module, class_name)
    return model_class(**init_args)

def count_parameters(model):
    """Count the number of parameters in a model."""
    return sum(p.numel() for p in model.parameters())

def save_to_csv(data, output_path):
    """Save model parameter counts to a CSV file."""
    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data.keys())  # Write header row
        writer.writerow(data.values())  # Write parameter counts

def main(config_path, output_path):
    """Main function to count parameters and save to CSV."""
    with open(config_path, "r") as file:
        model_configs = yaml.safe_load(file)

    param_counts = {}
    for model_name, config in model_configs.items():
        print(f"Processing model: {model_name}")
        model = instantiate_model(config["class_path"], config["init_args"])
        param_counts[model_name] = count_parameters(model)

    save_to_csv(param_counts, output_path)
    print(f"Parameter counts saved to {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Count model parameters and save to CSV.")
    parser.add_argument("-c", "--config", type=str, required=True, help="Path to the YAML configuration file.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to save the CSV file.")
    args = parser.parse_args()

    main(args.config, args.output)
