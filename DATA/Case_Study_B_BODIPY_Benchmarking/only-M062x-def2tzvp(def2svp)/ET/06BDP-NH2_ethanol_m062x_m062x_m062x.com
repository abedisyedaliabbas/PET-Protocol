%nprocshared=32
%mem=64GB
%oldchk=05BDP-NH2_ethanol_m062x_m062x_m062x.chk
%chk=06BDP-NH2_ethanol_m062x_m062x_m062x.chk
# m062x/def2tzvp geom=check guess=read TD=(Read, NStates=3, Root=1) SCRF=(SMD, solvent=ethanol, CorrectedLR, NonEq=Save)

BDP-NH2_ethanol_m062x_m062x_m062x

0 1











