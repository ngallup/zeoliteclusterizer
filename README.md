# zeoliteclusteizer - rapid catalyst screening in Python
- Version: 0.1.1
- Author: Nathan Gallup
- Email: gallup@chem.ucla.edu, nathan.gallup@nrel.gov

The zeoliteclusterizer module is meant to streamline the process of screening multiple potential metal catalysts and ligand combinations across an arbitrary set of sub-ring structures and binding poses.  This module facilitates the rapid quantum mechanical characterization of these initial adsorbed species and allows higher level statistical analyses to be performed because of the decrease in combinatoric intractability that exists when this problem is tackled manually.  It operates to produce new Gaussian input files according to the constraints established by the user.  The package itself does not perform quantum mechanics on the resulting structures.  The user will need access to a commercially available quantum package.  It is currently written with Gaussian in mind, but it should be simple to extend to other packages such as NWChem, GAMESS, Turbomole, etc.

In its current form, zeoliteclusterizer is new and experimental.  It is likely to contain bugs but is a fully operational prototype.

## Usage

First determine the metals, metal charges, and ligands you are interested in screening.  You will then need to build a list of Metal and Ligand objects, with the latter requiring generic coordinates.  A ScaffoldRing object will also need to be created.  The ScaffoldRing object represents the zeolite sub-ring without an adsorbed catalyst.  A list of BindingMode objects will also need to be generated that represent the scaffold and a generic adsorbed species in various conformations.  All of these are fed into a Clusterizer object, which determines which ligand-metal combinations are electronically feasible based on constraints set by the user.  These combinations are then tranformed into a set of cartesian coordinates, which can be written to disk using a G09Output object.  More specific instructions will be included as the package matures.

## History

Around 2016 the National Renewable Energy Laboratory (NREL) began working on new technologies to upgrade the waste products of biomass pyrrolysis into commercially useful fuel and fuel precursors.  A central focus of this effort was to engineer zeolite-type structures as catalysts to facilitate this waste upgrade by taking advantage of the catalytic action of adsorbed metal species.  Zeolites are periodic, but contain a decent number of subrings on which adsorbed metal species can bind and react, all of which need to be probed for catalytic stability.  This is further complicated by there being a large abundance of potential zeolite crystal structures, each with different subring topologies, and a large number of potential metal hosts and ligand combinations.  A screening methodology was required to provide guidance towards promising catalyst designs, and this package was developed to streamline this process by providing a means to screen any desired ligand-metal combination on top of an arbitrary sub-ring structure, enabling the ability to probe a huge spectrum metals and ligands.
