%nprocshared=32
%mem=64GB
%oldchk=06BN-1_ethanol_m062x_m062x_m062x.chk
%chk=07BN-1_ethanol_m062x_m062x_m062x.chk
# m062x/def2svp geom=check guess=read SCRF=(SMD, solvent=ethanol, NonEq=Read) 

BN-1_ethanol_m062x_m062x_m062x

0 1











