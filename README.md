# TensorBoard to CSV

TensorBoard-to-CSV is a Python package that extracts metrics from TensorBoard event files, computes confidence intervals, and exports the results to CSV files. It is designed to streamline the analysis and reporting of machine learning experiment results.

## Features

- Extract metrics from TensorBoard event files.
- Compute confidence intervals for metrics across multiple runs.
- Export metrics to CSV files with customizable formatting.
- Support for model and metric name mappings.
- Flexible sorting for models and metrics.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tonyzamyatin/tb-to-csv.git
   cd tb-to-csv
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface (CLI)

Run the package using the CLI:
```bash
cd tb_to_csv
python cli.py -c example_config.yaml
```

### Configuration

The package uses a `config.yaml` file to specify settings. See `tb_to_csv/exampl_config.yaml` for what an example configuration could look like.

### Output

The package generates CSV files for each prefix (e.g., `test_metrics.csv`, `shift_metrics.csv`, `ood_metrics.csv`) in the specified logs directory.

## Development

### Folder Structure

```
tensorboard-to-csv/
├── cli.py                      # Command-line interface
├── config.yaml                 # Example configuration file
├── core/                       # Core functionality
│   ├── aggregation.py          # Aggregates metrics across runs
│   ├── confidence_intervals.py # Computes confidence intervals
│   ├── csv_writer.py           # Writes metrics to CSV
│   ├── event_file_utils.py     # Handles TensorBoard event files
│   ├── metric_processing.py    # Processes and categorizes metrics
├── tests/                      # Tests cases
|   ├── ...
├── requirements.txt            # Dependencies
```

### Running Tests

You can test the package using the provided `test.py`.
First, add the `tb-to-csv` folder to your `PYTHONPATH` and then run:
```bash
pytest tests/
```
Alternitavely, you can run:
```
PYTHONPATH=$(pwd) pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
