
from ..scaffolds import ScaffoldRing, BindingMode
from ..extraframework import Metal, Ligand, Combination, hydroxide, oxide, hydride
from ..clusterizer import *
from ..gaussian import G09Output
import os
import pprint


scaffold = ScaffoldRing(r'/projects/bioenergy/ngallup/git/zeoliteclusterizer/zeoliteclusterizer/tests/optimized_ring/optimized_ring.com')

print scaffold.getLoc()
print scaffold.charge
print scaffold.unpaired
print scaffold.atom_list

modes_dir = os.path.abspath(r'/projects/bioenergy/ngallup/git/zeoliteclusterizer/zeoliteclusterizer/tests/binding_sites')
modes_coms = os.listdir(modes_dir)
modes_coms = [os.path.join(modes_dir, each) for each in modes_coms]

# Note: create a BindingModes container class that takes a directory and
# recurses all .com and .gjf files
modes_coms = [BindingMode(each, scaffold.atom_list) for each in modes_coms]
pprint.pprint([each.metal_ligand_list for each in modes_coms])

# Note: might be worth considering a Metals container class for all Metal
# objects to be easier to read and keep track of.  Might be overengineering
# but is probably more intuitive than requring the user to submit a list of
# objects, especially when only concerned with one metal
#zn = Metal('Zn', [2], [0])
#cu = Metal('Cu', [1], [0])
#cr = Metal('Cr', [3], [0])
sc = Metal('Sc', [1,3], [0])
ti = Metal('Ti', [2,4], [0])
v = Metal('V', [1,3,5], [0])
cr = Metal('Cr', [2,4,6], [0])
mn = Metal('Mn', [3,5], [0])
fe = Metal('Fe', [2], [0])
co = Metal('Co', [1,3], [0])
ni = Metal('Ni', [2], [0])
cu = Metal('Cu', [2], [0])
zn = Metal('Zn', [2], [0])
metals = [sc, ti, v, cr, mn, fe, co, ni, cu, zn]

# Consider a Ligands container class for easier reading
print hydroxide.name, hydroxide.atom_list
print hydride.name, hydride.atom_list
print oxide.name, oxide.atom_list
ligands = [hydroxide, hydride, oxide]

#test = Combination()
#test.addMetal(zn, 2, 0)
#test.addLigand(hydroxide, -1, 0)
#print 'strings: ', test._strings
#print 'Hash: ', test._hashval
#print 'Metal: ', test.metal
#print 'Ligands: ', test.ligands
clusters = Clusterizer(scaffold, modes_coms, metals, 
					ligands, charges=[0], unpaired=[[0]], 
					mix_ligands=False)

output = G09Output(r'/projects/bioenergy/ngallup/git/zeoliteclusterizer/zeoliteclusterizer/tests/tests')
output.writeAllModes(clusters.getFinalModes(), makedirs=True)
