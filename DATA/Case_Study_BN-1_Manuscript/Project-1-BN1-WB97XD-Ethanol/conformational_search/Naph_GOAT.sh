#!/bin/bash
#PBS -q normal
#PBS -l select=1:ncpus=64:mpiprocs=64:mem=128G
#PBS -l walltime=24:00:00
#PBS -P personal
#PBS -N Naph_GOAT
#PBS -o Naph_GOAT.o
#PBS -e Naph_GOAT.e
# mail alert at (b)eginning, (e)nd and (a)bortion of execution
#PBS -m ea
# send mail to the following address
##PBS -M xyz@gmail.com
 
cd $PBS_O_WORKDIR
np=$( cat  ${PBS_NODEFILE} |wc -l );  ### get # of CPUs
 
/home/users/ntu/xiaogan4/Softwares/orca_6_0_1_linux_x86-64_shared_openmpi416_avx2/orca Naph_GOAT.inp > Naph_GOAT.out
