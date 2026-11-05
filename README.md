# pipeFSC: pipeline for fastsimcoal2 demographic inference

I wrote pipeFSC during my postdoc to run the demographic inference behind
[Poveda-Martínez et al. (2024, *Biological Invasions*)](https://doi.org/10.1007/s10530-024-03317-2),
where we compared alternative demographic scenarios for the cactus moth, *Cactoblastis cactorum*.
It automates the repetitive part of working with fastsimcoal2: running many replicates per model,
keeping the best run, comparing models by AIC and running the parametric bootstrap for confidence intervals.

----------

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)
- [Citation](#citation)
- [License](#license)

----------

## Installation

1. **Clone this repository**:

    ```bash
    git clone https://github.com/niconm89/pipeFSC.git
    cd pipeFSC
    ```

2. **Install the dependencies**:

    - Python 3
    - R, with the packages `optparse`, `plotrix` and `shape`
    - [fastsimcoal2](https://cmpg.unibe.ch/software/fastsimcoal2/) (not included in this repository).
      Download it from the official site and place the executable in `scripts/` with the name `fsc26`,
      which is the name the pipeline expects:

        ```bash
        cp /path/to/downloaded/fsc_executable scripts/fsc26
        chmod +x scripts/fsc26
        ```

      pipeFSC was developed with version 2.6. If you use fastsimcoal2, please cite:
      Excoffier L. et al. (2021). fastsimcoal2: demographic inference under complex evolutionary
      scenarios. *Bioinformatics*, 37(24), 4882–4885.

3. **Optional: add the repository folder to your PATH** to run the scripts from any directory
   (add the line to `~/.bashrc` to make it permanent):

    ```bash
    export PATH=$PATH:/path/to/pipeFSC
    ```

----------

## Usage

### Part 1: model fitting and selection (`pipeFSC.P1.py`)

For each model found in `--modeldir`, runs `--nruns` independent fastsimcoal2 replicates
(100,000 simulations, 40 ECM cycles, maximum-likelihood estimation from the multidimensional SFS),
keeps the replicate with the highest likelihood, computes its AIC, and writes two summary tables
to `--outdir`: `model_AIC.tsv` and `model_PV.tsv`.

- `-m`, `--modeldir`: directory with the three files of each model (`*.est`, `*.tpl`, `*_MSFS.obs`). Required.
- `-o`, `--outdir`: output directory; created if it does not exist. Required.
- `-n`, `--nruns`: number of independent replicates per model. Default: 100.
- `-t`, `--threads`: currently has no effect (see [Limitations](#limitations)).

The three files of each model must share the model name, for example:

```
SingleC0.est
SingleC0.tpl
SingleC0_MSFS.obs
```

### Part 2: confidence intervals by parametric bootstrap (`pipeFSC.P2.py`)

Simulates `--nruns` SFS from the best model, re-estimates the parameters on each one starting
from the best-model values, and collects all estimates in `Final_Table.pv` to compute
confidence intervals.

- `-m`, `--modeldir`: directory with `BestModel.par`, `BestModel.tpl`, `BestModel.est` and `BestModel.pv`. Default: `BestModel`.
- `-n`, `--nruns`: number of bootstrap replicates. Default: 100.
- `-t`, `--threads`: number of cores for fastsimcoal2. Default: 8.

Part 2 does not prepare its input: the four `BestModel.*` files must be created by hand from
the best model selected in Part 1.

### Examples

```bash
python3 pipeFSC.P1.py -m models/ -o results/ -n 100
python3 pipeFSC.P2.py -m BestModel/ -n 100 -t 8
```

The [models](models/) directory contains the models used in the study, and
[examples](examples/) contains a small test run.

----------

## Limitations

pipeFSC was written for a specific study and has not been generalized yet:

- Part 1 only recognizes the model names used in the study (hardcoded in `validate_models()`); other models are skipped.
- In Part 1, fastsimcoal2 runs with 8 cores and 16 batches regardless of `-t`.
- Part 2 expects its input files with fixed names (`BestModel.*`) and does not generate them from Part 1.
- In Part 2, the number of SNPs (`--dnatosnp 3287`) and the parameter names in `Final_Table.pv` are specific to the study dataset.

If you run into problems, please [open an issue](https://github.com/niconm89/pipeFSC/issues).

----------

## Citation

pipeFSC was developed for and used in:

Poveda-Martínez D., Moreyra N.N., Hasson E. et al. (2024). Demographic inference provides
evidence of a quaternary-driven impact on the cactus moth and sheds light on the putative role
of an exotic host. *Biological Invasions*, 26, 2313–2327.
https://doi.org/10.1007/s10530-024-03317-2

----------

## License

This pipeline is distributed under the [MIT License](LICENSE).
