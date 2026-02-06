%nprocshared=32
%mem=64GB
%oldchk=01BDP-NH2_ethanol_m062x_m062x_m062x.chk
%chk=02BDP-NH2_ethanol_m062x_m062x_m062x.chk
# td=(nstates=6) m062x/def2tzvp geom=check guess=read scrf=(SMD, solvent=ethanol)  

BDP-NH2_ethanol_m062x_m062x_m062x

0 1






