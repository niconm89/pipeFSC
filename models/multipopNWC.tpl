//Number of population samples
3
//Population effective sizes (number of genes)
938452
NPOP1
NPOP2
//Samples sizes
14
14
14
//Growth rates	: negative growth implies population expansion
0
0
0
//Number of migration matrices : 0 implies no migration between demes
2
//Migration matrix 0
0 MIG1 MIG2
MIG1 0 MIG3
MIG2 MIG3 0
//Migration matrix 1
0 0 0
0 0 0
0 0 0
//historical event: time, source, sink, migrants, new deme size, new growth rate, migration matrix index
2 historical event
TDIV1 0 1 1 RESIZE1 0 1
TDIV2 1 2 1 RESIZE2 0 1
//Number of independent loci [chromosome] 
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per generation recombination and mutation rates and optional parameters
FREQ 1 0 2.9e-9 OUTEXP
