#!/bin/bash

#Running fsc26
fsc26_path=/home/nmoreyra/Documents/Repositorios/CODEMO/scripts
NRUNS=50
model=Model1
for i in {1..NRUNS}; do
	mkdir run$i;
	#cp ${model}.tpl ${model}.est ${model}_MSFS.obs fsc26 run$i
	cd run$i
	$fsc26_path/fsc26 -t ../${model}.tpl -e ../${model}.est -n 100000 -m -0 -u -L 40 -M -c8 -B16 -q
	cd ..
done

