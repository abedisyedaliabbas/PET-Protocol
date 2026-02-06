%nprocshared=32
%mem=64GB
%oldchk=06BDP-NH2_ethanol_m062x_m062x_m062x.chk
%chk=07BDP-NH2_ethanol_m062x_m062x_m062x.chk
# m062x/def2tzvp geom=check guess=read SCRF=(SMD, solvent=ethanol, NonEq=Read) pop=(full, orbitals=2, threshorbitals=1)

BDP-NH2_ethanol_m062x_m062x_m062x

0 1











