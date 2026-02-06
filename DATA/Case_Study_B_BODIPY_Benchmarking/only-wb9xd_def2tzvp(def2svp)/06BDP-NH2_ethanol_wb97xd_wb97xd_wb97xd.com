%nprocshared=32
%mem=64GB
%oldchk=05BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd.chk
%chk=06BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd.chk
# wb97xd/def2tzvp geom=check guess=read TD=(Read, NStates=3, Root=1) SCRF=(SMD, solvent=ethanol, CorrectedLR, NonEq=Save)

BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd

0 1











