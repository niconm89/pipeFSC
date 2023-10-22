# pipeFSC - Pipeline for Fastsimcoal demographic simulations 

This is a Python pipeline for running Fastsimcoal (FSC). It automates the process of setting up and running FSC models, selecting the best run for each model, calculating AIC scores, and generating files for posterior confidence intervals estimations.
----------

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Examples](#examples)
----------

## Installation

To use the `pipeFSC` pipeline, follow these steps:

1. **Clone this repository to your local machine**:

    ```bash
    git clone https://github.com/niconm89/pipeFSC.git
    ```

2. **Navigate to the cloned directory**:

    ```bash
    cd pipeFSC
    ```

3. **Make sure you have the required dependencies installed**:

- Python
- R
    - optparse
    - plotrix
    - shape
- [FastSimCoal (FSC)](http://cmpg.unibe.ch/software/fastsimcoal2/)

4. **Add pipeFSC path to your $PATH variable**

    To add a folder to the system's PATH in a Linux/Unix system, you can follow these steps:

- **Open a Terminal**: You'll need to use the command line.
- **Identify the Folder**: Ensure you know the full path to the folder you want to add to the PATH. For example, let's say your folder is located at /path/to/your/folder.
- **Edit the .bashrc or .bash_profile File**: You'll typically edit your user-specific configuration file. This file is located in your home directory, and you can use a text editor like nano or vi to open it. For example, use:
    ```bash
    nano ~/.bashrc
    ```
    or

    ```bash
    nano ~/.bash_profile
    ```

- **Add the Folder to PATH**: Add the following line to the file, replacing /path/to/your/folder with the actual folder path:
    ```bash
    export PATH=$PATH:/path/to/your/folder
    ```
    This line appends your folder to the existing PATH.
- Save and Exit: If you're using nano, press `Ctrl + O` to save, and `Ctrl + X` to exit.
- Source the File: To apply the changes immediately, run:

    ```bash
    source ~/.bashrc
    ```
    or

    ```bash
    source ~/.bash_profile
    ```
    This step is necessary to refresh your terminal with the updated PATH.

- **Verify the Change**: You can check if the folder has been added to the PATH by running:

    ```bash
    echo $PATH
    ```
    You should see your folder's path in the list.

    Your folder should now be part of the system's PATH, making it easier to run executables and scripts located within that folder from any directory in your terminal.

    This process is common on Linux/Unix systems, but please note that the specific file you need to edit (.bashrc or .bash_profile) can vary depending on your shell (e.g., Bash, Zsh, etc.). If you're using a different shell, you may need to modify a different configuration file.

    **Note**: Ensure that you have the necessary permissions to edit these configuration files. If you're not the system administrator, you might need to use sudo to gain the required permissions.

5. **Run the pipeline using the provided Python script**:
    ```bash
    python pipeFSC.py -m /path/to/model/files -o /output/directory -n 100 -t 2
    ```
    **Replace** `/path/to/model/files` with the path to the directory containing the necessary FSC model files (*.est, *.tpl, and *_MSFS.obs). 
    
    **Note** that you must place all the three files for each model you want to run in the same directory (`-m /path/to/model/files`, see below). You can also specify the number of replicates (`-n`) and the number of threads (`-t`) for running the models.
    ```bash
    $ ls pipeFSC/examples/test_SingleC_n3/
    SingleC0.est
    SingleC1.est
    SingleC2A.est
    SingleC2B.est
    SingleC2N.est
    SingleC0_MSFS.obs
    SingleC1_MSFS.obs
    SingleC2A_MSFS.obs
    SingleC2B_MSFS.obs
    SingleC2N_MSFS.obs
    SingleC0.tpl
    SingleC1.tpl
    SingleC2A.tpl
    SingleC2B.tpl
    SingleC2N.tpl
    ```
----------
## Usage

### pipeFSC part1

#### Aca va la descripcion del analisis

- `-m` or `--modeldir`: Path to the directory containing the three required files (*.est, *.tpl, and *_MSFS.obs) for each model selected.
- `-o` or `--outdir`: Path to the directory where the results will be saved. If the output directory does not exist, it will be created. (Default: 03_phylogenetic_tree)
- `-n` or `--nruns`: Number of model run replicates. (Default: 1000)
- `-t` or `--threads`: Number of threads to run. (Default: 8)

### pipeFSC part2

#### Aca va la descripcion del analisis

- `-m` or `--modeldir`: Path to the directory containing the three required files (*.est, *.tpl, and *_MSFS.obs) for each model selected.
- `-o` or `--outdir`: Path to the directory where the results will be saved. If the output directory does not exist, it will be created. (Default: 03_phylogenetic_tree)
- `-n` or `--nruns`: Number of model run replicates. (Default: 1000)
- `-t` or `--threads`: Number of threads to run. (Default: 8)

----------
### Examples

Part1 
```bash
./pipeFSC.P1.py -m /path/to/model/files -o /output/directory -n 100 -t 4
```

Part2
```bash
./pipeFSC.P2.py -m /path/to/modeldir -n 100 -t 8
```

You can find usage examples and more information in the [examples](examples/) directory.

----------
## Examples
If you encounter any issues or have questions, please [open an issue](https://github.com/niconm89/pipeFSC/issues) on the GitHub repository.

----------
## License
This pipeline is distributed under the [MIT License](LICENSE).
