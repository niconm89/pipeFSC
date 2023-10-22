#!/usr/bin/env python
"""
Created on Mon Oct  09 14:13:22 2023

@author: Nicolás Nahuel Moreyra (niconm89@gmail.com; https://github.com/niconm89)
"""

#%% Imports
import argparse
import os
import shutil
import time
import sys

# Functions
def running_models(model_list, outdir, nruns):
    fsc26_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
    cwd = os.getcwd()
    for model in model_list:
        print("\nModel " + model + ":\n")
        model_path = os.path.join(outdir, model)
        if not os.path.isdir(model_path):
            os.makedirs(model_path, exist_ok=True)
        for i in range(1, nruns+1):
            print("Running replicate #" + str(i))
            replicate_path = os.path.join(model_path, "run" + str(i))
            if not os.path.isdir(replicate_path):
                os.makedirs(replicate_path, exist_ok=True)
            for file in os.listdir(os.path.join(outdir, model)):
                if model in file:
                    shutil.copy(os.path.join(outdir, model, file), os.path.join(replicate_path, file))
                    print("Copied file:", os.path.join(outdir, model, file), "to", os.path.join(replicate_path, file))
            try:
                os.chdir(replicate_path)
                script_path = os.path.abspath(sys.argv[0])
                script_directory = os.path.dirname(script_path)
                os.system(f"{fsc26_path}/fsc26 -t {model}.tpl -e {model}.est -n 100000 -m -0 -u -L 40 -M -c8 -B16 -q")
            except FileNotFoundError as e:
                print(f"Error: {e}")
            os.chdir(cwd)
        #selecting best run per model
        select_best_models(model, outdir)
        os.chdir(cwd)
        calculate_AIC(model, outdir)
        #print("Model to visualize: " + model)
        #visualize_model_fit(model, outdir)
    os.chdir(cwd)
#end
def calculate_AIC(model, outdir):
    AIC_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "calculateAIC.sh")
    cwd = os.getcwd()
    os.chdir(os.path.join(outdir, model, "bestrun"))
    os.system("Rscript " + AIC_path + " " + model)
    os.chdir(cwd)
#end
def generate_PV_table(outdir, model_list):
    file_path = os.path.join(outdir, "model_PV.tsv")
    with open(file_path, 'w') as f:
        #header = {'model_name':'-', 'pv':'-', 'ANCSIZE':'-','NPOP1':'-','NPOP2':'-','NPOP3':'-','TDIV1':'-','TDIV2':'-','TANC':'-','TREC':'-','MIG1':'-','MIG2':'-','MIG3':'-'}
        #header_line = "model_name\tpv\tANCSIZE\tNPOP1\tNPOP2\tNPOP3\tTDIV1\tTDIV2\tTANC\tTREC\tMIG1\tMIG2\tMIG3\n"
        #f.write(header_line + "\n")
        for model_name in model_list:
            file_path = os.path.join(outdir, model_name, "bestrun", f"{model_name}.pv")
            with open(file_path, 'r') as g:
                lines = g.readlines()
                f.write("## " + model_name + ":\n" + ''.join(lines[0]) + ''.join(lines[1]) + "\n\n")
                #f.write("\n")
#end
def generate_AIC_table(outdir, model_list):
    file_path = os.path.join(outdir, "model_AIC.tsv")
    if os.path.exists(file_path):
        mode = 'a'
    else:
        mode = 'w'
    with open(file_path, mode) as f:
        if mode == 'w':
            f.write("model_name\tdeltaL\tAIC\n")
        for model_name in model_list:
            print(model_name)
            with open(os.path.join(outdir, model_name, "bestrun", f"{model_name}.AIC"), 'r') as g:
                columns = g.read().strip().split()
                deltaL = columns[2]
                AIC = columns[3]
                f.write(f"{model_name}\t{deltaL}\t{AIC}\n")
#end
def select_best_models(model, outdir):
    select_best_run_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "fsc-selectbestrun.sh")
    print("Selecting best run for model " + model + "...")
    cwd = os.getcwd()
    os.chdir(os.path.join(outdir, model))
    os.system("bash " + select_best_run_path + " " + model)
    os.chdir(cwd)
#end
def validate_models(modeldir):
    model_files = {
        "multipopCWN": ["multipopCWN.est", "multipopCWN_MSFS.obs", "multipopCWN.tpl"],
        "multipopNWC": ["multipopNWC.est", "multipopNWC_MSFS.obs", "multipopNWC.tpl"],
        "multipopWNC": ["multipopWNC.est", "multipopWNC_MSFS.obs", "multipopWNC.tpl"],
        "SingleC0": ["SingleC0.est", "SingleC0_MSFS.obs", "SingleC0.tpl"],
        "SingleC1": ["SingleC1.est", "SingleC1_MSFS.obs", "SingleC1.tpl"],
        "SingleC2A": ["SingleC2A.est", "SingleC2A_MSFS.obs", "SingleC2A.tpl"],
        "SingleC2B": ["SingleC2B.est", "SingleC2B_MSFS.obs", "SingleC2B.tpl"],
        "SingleC2N": ["SingleC2N.est", "SingleC2N_MSFS.obs", "SingleC2N.tpl"],
        "SingleN0": ["SingleN0.est", "SingleN0_MSFS.obs", "SingleN0.tpl"],
        "SingleN1": ["SingleN1.est", "SingleN1_MSFS.obs", "SingleN1.tpl"],
        "SingleN2A": ["SingleN2A.est", "SingleN2A_MSFS.obs", "SingleN2A.tpl"],
        "SingleN2B": ["SingleN2B.est", "SingleN2B_MSFS.obs", "SingleN2B.tpl"],
        "SingleN2N": ["SingleN2N.est", "SingleN2N_MSFS.obs", "SingleN2N.tpl"],
        "SingleW0": ["SingleW0.est", "SingleW0_MSFS.obs", "SingleW0.tpl"],
        "SingleW1": ["SingleW1.est", "SingleW1_MSFS.obs", "SingleW1.tpl"],
        "SingleW2A": ["SingleW2A.est", "SingleW2A_MSFS.obs", "SingleW2A.tpl"],
        "SingleW2B": ["SingleW2B.est", "SingleW2B_MSFS.obs", "SingleW2B.tpl"],
        "SingleW2N": ["SingleW2N.est", "SingleW2N_MSFS.obs", "SingleW2N.tpl"]
    }
    models_present = []
    files_present = []
    for model, files in model_files.items():
        if all(os.path.isfile(os.path.join(modeldir, file)) for file in files):
            models_present.append(model)
            for file in files:
                files_present.append(file)
    return models_present, files_present
#end
def move_and_create_modeldirs(modeldir, outdir, file_list, model_list):
    for model in model_list:
        model_path = os.path.join(outdir, model)
        if not os.path.isdir(model_path):
            os.makedirs(model_path, exist_ok=True)
        for file in file_list:
            if model in file:
                if file.endswith(".est") or file.endswith(".tpl"):
                    file_name = os.path.splitext(file)[0]
                elif file.endswith("_MSFS.obs"):
                    file_name = file.split("_")[0]
                else:
                    raise RuntimeError("modeldir contains files without the right format.")
                file_path = os.path.join(model_path, file)
                shutil.copy(os.path.join(modeldir, file), file_path)
                print("Copied file:", os.path.join(modeldir, file), "to", file_path)
#end
def validate_params(args):
    'It receives the object of arguments and validates mandatory arguments to run the pipeline.'
    mandatory_args = {}
    if not os.path.isdir(args.modeldir):
        raise RuntimeError("The directory containing est, tpl and _MSFS.obs files can not be found.")
    if not os.path.isdir(args.outdir):
        try:
            os.makedirs(args.outdir, exist_ok=True)
        except:
            raise RuntimeError("The output directory can not be created.")
    # Add your edits here
    if args.nruns < 1:
        raise ValueError("Number of replicates must be equal or greater than fifty.")
    if args.threads <= 0:
        raise ValueError("Number of threads must be greater than zero.")
#end
'''
def visualize_model_fit(model, outdir):
    FStools = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "SFStool.R")
    plotModel = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "plotModel.R")
    cwd = os.getcwd()
    os.chdir(outdir)
    os.system("Rscript " + FStools + " -t print2D -i " + model)
    os.system("Rscript " + plotModel + " -p " + model + " -l NyerMak,PundMak")
    os.chdir(cwd)
#end
'''
#%% Menu -> Usage
def usage():
   	# This function sets up the command line arguments for the script using argparse.
	# It returns the parsed arguments.
	parser = argparse.ArgumentParser(
		description='''pipeFSC: pipeline for FastSimCoal demographic simulations''')
	parser.add_argument('-m', '--modeldir', type=str, required=True, help='Path to the directory containing the three files (*.est, *.tpl and *_MSFS.obs) for each model selected.')
	parser.add_argument('-o', '--outdir', type=str, required=True, default='03_phylogenetic_tree', help='Path to save results. If the output directory does not exists, it will be created. Default: 04_phylogenetic_tree')
	parser.add_argument('-n', '--nruns', type=int, required=False, default="100", help='Number of model run replicates. Default: 1000')
	parser.add_argument('-t', '--threads', type=int, required=False, default="2", help='Number of threads to run in IQ-Tree. Default: 8')
	return parser.parse_args()
#end

#%% Main program
if __name__ == '__main__':
	args = usage()
	start = time.time() #time 0
	validate_params(args)
	# Test the function using the 'models' directory located in the same path as this script
	try:
		modeldir = os.path.abspath(args.modeldir)
		model_list, file_list = validate_models(modeldir)
	except Exception as e:
		print("Error:", str(e))
		model_list = []
		file_list = []
	move_and_create_modeldirs(modeldir, args.outdir, file_list, model_list)
	print("Output direcry: " + str(args.outdir))
	print("Number of replicates: " + str(args.nruns))
	print("Number of threads: " + str(args.threads))
	print("Identifying models to run.")
	print("Arguments checked!\nRunning models: " + ",".join(model_list))
	# running models
	print("Running models.")
	running_models(model_list, args.outdir, args.nruns)
	print("Generating AIC table.")
	generate_AIC_table(args.outdir, model_list)
	print("Generating PV table.")
	generate_PV_table(args.outdir, model_list)
	print("Pipeline finished.")
	print(f'Time taken to run: {time.time() - start} seconds.')
    # This is the main part of the script. It first parses the command line arguments, then starts the timer,
	# runs the model_partitions function with the parsed arguments, then prints the time taken to run.
#end

