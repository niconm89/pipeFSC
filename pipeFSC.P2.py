#!/usr/bin/env python3
"""
Created on Mon Oct  09 14:13:22 2023

@author: Nicolás Nahuel Moreyra (niconm89@gmail.com; https://github.com/niconm89)
"""

#Imports
import os
import argparse
import time

#Functions
def run_fsc_step1(modeldir, threads, nruns):
    fsc26_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
    # Get the full path of the BestModel.par file
    bestmodel_par = os.path.abspath(os.path.join(modeldir, 'BestModel.par'))
    os.chdir(modeldir)
    # Execute the fsc26 command with the specified parameters
    print(f'{bestmodel_par}\n')
    if os.path.exists(bestmodel_par):
        command_fsc26 = f'{fsc26_path}/fsc26 --ifile BestModel.par --numsims {nruns} --jobs --msfs --multiSFS --dnatosnp 3287 --noarloutput --minnumloops --cores {threads} --numboot 16'
    else:
        raise RuntimeError(f"{bestmodel_par} - par file - does not exists.")
    #./fsc26 -i BestModel.par -n100 -j -m --multiSFS -s3287 -x -l -c8 -b16
    os.system(command_fsc26)
#end
def run_fsc_step2(modeldir, threads, nruns):
    fsc26_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
    # Get the full path of the files required for fsc
    tplfile = os.path.abspath(os.path.join(modeldir, 'BestModel.tpl')) #Check these paths but don't use them in the fsc26 command because only relative paths don't get Segmentation fault (core dumped)
    estfile = os.path.abspath(os.path.join(modeldir, 'BestModel.est'))
    initValues = os.path.abspath(os.path.join(modeldir, 'BestModel.pv'))
    cwd = os.getcwd()
    if os.path.exists(tplfile) and os.path.exists(estfile) and os.path.exists(initValues):
        for i in range(1, nruns+1):
            modeldir_i = os.path.abspath(os.path.join(modeldir, 'BestModel', f'BestModel_{i}'))
            os.chdir(modeldir_i)
            command_fsc26 = f'{fsc26_path}/fsc26 --tplfile ../../BestModel.tpl --estfile ../../BestModel.est --numsims 100000 --msfs --removeZeroSFS --multiSFS --numloops 40 --initValues ../../BestModel.pv --cores {threads} --maxlhood --numBatches 16 --quiet'
            #command_fsc26 = f'{fsc26_path}/fsc26 --tplfile {tplfile} --estfile {estfile} --numsims 100000 --msfs --removeZeroSFS --multiSFS --numloops 40 --initValues {initValues} --maxlhood --cores {threads} --numBatches 16 --quiet'
            # Execute the fsc command with the specified parameters
            os.system(command_fsc26)
            initValues_i = os.path.join(modeldir_i, 'BestModel/BestModel.pv')
            # Read the BestModel.pv file and concatenate into a table
            with open(initValues_i, 'r') as f:
                initValues_data = f.readlines()
            initValues_data = [line.strip().split() for line in initValues_data]
            # Concatenate the output of the BestModel.pv file for another run
            os.chdir(cwd)
            PV_table = os.path.join(modeldir, 'Final_Table.pv')
            with open(PV_table, 'a') as f:
                if os.stat(PV_table).st_size == 0:
                    header = ['ANCSIZE', 'NPOP1', 'NPOP2', 'NPOP3', 'TDIV1', 'TDIV2', 'MIG1', 'MIG2', 'MIG3']
                    f.write('\t'.join(header) + '\n')
                values = [line.strip().split() for line in initValues_data[1]]
                values = [item for sublist in values for item in sublist]
                f.write('\t'.join(values) + '\n')
    else:
        raise RuntimeError(f"Check your tpl, est and initValues files.")
#end
def main():
    start = time.time() #time 0
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Script to execute fsc26 and fsc commands')
    parser.add_argument('-m', '--modeldir', type=str, default='BestModel', help='Path to the model directory.')
    parser.add_argument('-t', '--threads', type=int, default=8, help='Number of threads (Default: 8).')
    parser.add_argument('-n', '--nruns', type=int, default=100, help='Number of independent runs (Default: 100.')
    # Obtener los argumentos del usuario
    args = parser.parse_args()
    # Verificar si la carpeta Bestmodel y el archivo config.txt existen
    if not os.path.exists(args.modeldir):
        print("Model directory does not exists.")
        return
    # Ejecutar los comandos fsc26 y fsc con los argumentos especificados
    cwd = os.getcwd()
    print("Model directory: " + args.modeldir)
    print("Number of independent runs: " + str(args.nruns))
    print("Number of threads: " + str(args.threads))
    # running models
    print("Running first command.") #This must be differenciate from the first part of the analysis (pipeFSC.p1.py)
    run_fsc_step1(args.modeldir, args.threads, args.nruns)
    print("Running second command.")
    os.chdir(cwd)
    run_fsc_step2(args.modeldir, args.threads, args.nruns)
    print("pipeFSC part 2 has finished.")
    print(f'Time taken to run: {time.time() - start} seconds.')

if __name__ == "__main__":
    main()
