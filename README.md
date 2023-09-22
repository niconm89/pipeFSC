# wfFSC - workflow for FastSimCoal Demographic Models Pipeline

This is a Python pipeline for running FastSimCoal (FSC) demographic models with replicates. It automates the process of setting up and running FSC models, selecting the best run for each model, calculating AIC scores, and generating PV (Posterior Variance) tables.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Examples](#examples)

## Installation

To use the `wfFSC` pipeline, follow these steps:

1. Clone this repository to your local machine:

    git clone https://github.com/niconm89/wfFSC.git


2. Navigate to the cloned directory:

    cd wfFSC

3. Make sure you have the required dependencies installed:

- Python
- R
- FastSimCoal (FSC)

4. Run the pipeline using the provided Python script:

python wfFSC.py -m /path/to/model/files -o /output/directory -n 100 -t 2

Replace `/path/to/model/files` with the path to the directory containing the necessary FSC model files (*.est, *.tpl, and *_MSFS.obs). You can also specify the number of replicates (`-n`) and the number of threads (`-t`) for running the models.

## Usage

python wfFSC.py -m /path/to/model/files -o /output/directory -n 100 -t 2

- `-m` or `--modeldir`: Path to the directory containing the three required files (*.est, *.tpl, and *_MSFS.obs) for each model selected.
- `-o` or `--outdir`: Path to the directory where the results will be saved. If the output directory does not exist, it will be created. (Default: 03_phylogenetic_tree)
- `-n` or `--nruns`: Number of model run replicates. (Default: 1000)
- `-t` or `--threads`: Number of threads to run in IQ-Tree. (Default: 8)

## License

This pipeline is distributed under the [MIT License](LICENSE).

## Examples

You can find usage examples and more information in the [examples](examples/) directory.

If you encounter any issues or have questions, please [open an issue](https://github.com/niconm89/wfFSC/issues) on the GitHub repository.