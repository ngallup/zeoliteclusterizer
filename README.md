# zeoliteclusteizer - rapid catalyst screening in Python
- Version: 0.1.1
- Author: Nathan Gallup
- Email: gallup@chem.ucla.edu, nathan.gallup@nrel.gov

The zeoliteclusterizer module is meant to streamline the process of screening multiple potential metal catalysts and ligand combinations across an arbitrary set of sub-ring structures and binding poses.  This module facilitates the rapid quantum mechanical characterization of these initial adsorbed species and allows higher level statistical analyses to be performed because of the decrease in combinatoric intractability that exists when this problem is tackled manually.  It operates to produce new Gaussian input files according to the constraints established by the user.  The package itself does not perform quantum mechanics on the resulting structures.  The user will need access to a commercially available quantum package.  It is currently written with Gaussian in mind, but it should be simple to extend to other packages such as NWChem, GAMESS, Turbomole, etc.

In its current form, zeoliteclusterizer is new and experimental.  It is likely to contain bugs but is a fully operational prototype.

## Installation

The simplest way to get zeoliteclusterizer is to download it via pip.  Simply call
```
pip install zeoliteclusterizer
```
from the command line, and the package is ready for use!  Note, however, that the absolute latest versions of zeoliteclusterizer will be here on GitHub before being considered stable enough to commit to the PyPi repository.  PyPi versions will be reserved to stable builds and major new features.

## Usage

First determine the metals, metal charges, and ligands you are interested in screening.  You will then need to build a list of Metal and Ligand objects, with the latter requiring generic coordinates.  A ScaffoldRing object will also need to be created.  The ScaffoldRing object represents the zeolite sub-ring without an adsorbed catalyst.  A list of BindingMode objects will also need to be generated that represent the scaffold and a generic adsorbed species in various conformations.  All of these are fed into a Clusterizer object, which determines which ligand-metal combinations are electronically feasible based on constraints set by the user.  These combinations are then tranformed into a set of cartesian coordinates, which can be written to disk using a G09Output object.  More specific instructions will be included as the package matures.

An code example is presented below that enables the screening of the first row of the d-block with hydride, hydroxide, and oxide ligands, against a scaffold that has a charge of -1.  Common ligands are provided in the extraframework module, but we'll discuss how to make your own as well.
```
from zeoliteclusterizer.scaffolds import ScaffoldRing, BindingMode
from zeoliteclusterizer.extraframework import Metal, Ligand, hydroxide, oxide, hydride
from zeoliteclusterizer.clusterizer import Clusterizer
from zeoliteclusterizer.gaussian import G09Output

# We first need to specify the scaffold
scaffold = ScaffoldRing(<path to scaffold ring>)

# Now we need to specify the binding modes we're interested in probing
modes_dir = os.path.abspath(<path to directory holding desired binding configurations>)
modes = os.listdir(modes_dir)
modes = [os.path.join(modes_dir, each) for each in modes_coms]
modes = [BindingMode(each, scaffold.atom_list) for each in modes_coms]

# Specify all the metals, charges, and spin states we're interesting in screening
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

# Create of list of ligands we want to combine with each of these metals
ligands = [hydroxide, hydride, oxide]

# The Clusterizer object will take all of this data and perform all the cominatorics for us.  Here we specify that we only want scaffold-metal-ligand combinations that only have a total charge of 0, and 0 unpaired electrons.  We also specify that we don't want mixed ligand combinations for all accepted geometries.
clusters = Clusterizer(scaffold, modes_coms, metals, 
                        ligands, charges=[0], unpaired=[[0]], 
					              mix_ligands=False)
                        
# Finally, we need to write all these modes to a directory in a format that Gaussian 09 appreciates, creating new directory for each file
output = G09Output(<directory to contains all resulting .com/.gjf files>)
output.writeAllModes(clusters.getFinalModes(), makedirs=True)
```

## History

Around 2016 the National Renewable Energy Laboratory (NREL) began working on new technologies to upgrade the waste products of biomass pyrrolysis into commercially useful fuel and fuel precursors.  A central focus of this effort was to engineer zeolite-type structures as catalysts to facilitate this waste upgrade by taking advantage of the catalytic action of adsorbed metal species.  Zeolites are periodic, but contain a decent number of subrings on which adsorbed metal species can bind and react, all of which need to be probed for catalytic stability.  This is further complicated by there being a large abundance of potential zeolite crystal structures, each with different subring topologies, and a large number of potential metal hosts and ligand combinations.  A screening methodology was required to provide guidance towards promising catalyst designs, and this package was developed to streamline this process by providing a means to screen any desired ligand-metal combination on top of an arbitrary sub-ring structure, enabling the ability to probe a huge spectrum metals and ligands.
