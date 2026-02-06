%nprocshared=32
%mem=64GB
%oldchk=01BDP-NH2_ethanol_m062x_m062x_m062x.chk
%chk=03BDP-NH2_ethanol_m062x_m062x_m062x.chk
# m062x/def2tzvp geom=check guess=read TD=(NStates=3, Root=2) SCRF=(SMD, solvent=ethanol, CorrectedLR)

BDP-NH2_ethanol_m062x_m062x_m062x

0 1





















