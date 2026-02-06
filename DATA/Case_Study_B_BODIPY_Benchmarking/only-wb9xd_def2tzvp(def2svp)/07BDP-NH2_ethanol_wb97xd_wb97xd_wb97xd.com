%nprocshared=32
%mem=64GB
%oldchk=06BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd.chk
%chk=07BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd.chk
# wb97xd/def2tzvp geom=check guess=read SCRF=(SMD, solvent=ethanol, NonEq=Read) pop=(full, orbitals=2, threshorbitals=1)

BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd

0 1











