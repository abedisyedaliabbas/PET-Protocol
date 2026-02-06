%nprocshared=32
%mem=64GB
%oldchk=01BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd.chk
%chk=02BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd.chk
# td=(nstates=6) wb97xd/def2tzvp geom=check guess=read scrf=(SMD, solvent=ethanol) 

BDP-NH2_ethanol_wb97xd_wb97xd_wb97xd

0 1






