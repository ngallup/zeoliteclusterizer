# zeoliteclusterizer

The zeoliteclusterizer module is meant to streamline the process of screening multiple potential metal catalysts and ligand combinations across an arbitrary set of sub-ring structures and binding poses.  This module facilitates the rapid quantum mechanical characterization of these initial adsorbed species and allows higher level statistical analyses to be performed because of the decrease in combinatoric intractability that exists when this problem is tackled manually.  It operates to produce new Gaussian input files according to the constraints established by the user.  The package itself does not perform quantum mechanics on the resulting structures.  The user will need access to a commercially available quantum package.

In its current form, zeoliteclusterizer is new and experimental.  It is likely to contain bugs but is a fully operational prototype.

## How to Use

First determine the metals, metal charges, and ligands you are interested in screening.  You will then need to build a list of Metal and Ligand objects, with the latter requiring generic coordinates.  A ScaffoldRing object will also need to be created.  The ScaffoldRing object represents the zeolite sub-ring without an adsorbed catalyst.  A list of BindingMode objects will also need to be generated that represent the scaffold and a generic adsorbed species in various conformations.  All of these are fed into a Clusterizer object, which determines which ligand-metal combinations are electronically feasible based on constraints set by the user.  These combinations are then tranformed into a set of cartesian coordinates, which can be written to disk using a G09Output object.
