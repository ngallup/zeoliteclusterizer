import string
from gaussian import GaussianInput
import os, sys
import numpy as np
import copy

class ScaffoldRing(GaussianInput):
	'''
	For defining the zeolite scaffold ring and its inherent chemical and
	electronic properties, as well as providing an easy collection of atom
	coordinates and characteristics
	'''
	def getLoc(self):
		return self.input_loc

	def __init__(self, comfile):
		self.input_loc = os.path.abspath(comfile)
		with open(comfile,'r') as infile:
			lines = infile.readlines()
			
			self.head_lines, self.charge, self.unpaired, self.atom_start = self.readHeader(lines)
			self.atom_list = self.readAtoms(self.atom_start, lines)

class BindingMode(GaussianInput):
	'''
	For defining the binding mode rings to be permutated upon.  Primarily for
	parsing out the metal binding modes and ligand locations.
	'''
	def __init__(self, comfile, scaffold_atoms):
		self.input_loc = os.path.abspath(comfile)
		with open(comfile, 'r') as infile:
			lines = infile.readlines()

			self.metal_ligand_list = self.getMetalsLigands(lines, scaffold_atoms)

	def getMetalsLigands(self, lines, scaffold_atoms):
		'''
		Returns list of metal and ligand locations.  Current implementation
		is very primative: the method simply compares the list lengths and
		truncates the leading atoms.  More advanced handling should be
		implemented at a later time.
		'''
		atom_list = []
		scaffold_len = len(scaffold_atoms)

		# Need to find the beginning of the atom list
		index = 0
		while('Title Card Required' not in lines[index]):
			index += 1
		index += 3

		# Want to truncate atom list
		index += scaffold_len
		line = lines[index].split()
		while(self.startsWithLetter(line) == True):
			self.addSplit(line, atom_list)
			index += 1
			line = lines[index].split()

		return atom_list
	
	def getLoc(self):
		return self.input_loc

	def getNumLigands(self):
		'''
		Currently assumes only a single metal.  Should be good approximation
		but one day may need to be changed.
		'''
		return len(self.metal_ligand_list)-1

	def getMetal(self):
		'''
		Specifically looks for "X" as the metal to be replaced
		'''
		result = []
		for line in self.metal_ligand_list:
			if line[0] == 'X':
				result.append(line)
		return result

	def getLigands(self):
		result = []
		for line in self.metal_ligand_list:
			if line[0] != 'X':
				result.append(line)
		return result

class AbstractMode(object):
	'''
	A class to bind a particular Combination and BindingMode object to make it
	easier to iterate upon all possible conformations and finally write to an
	output file
	'''
	def __init__(self, combo_obj, binding_obj, scaffold, mixed=True):
		self.combo = combo_obj
		self.bindingMode = binding_obj
		self.scaffold = scaffold
		self.conformations = self._createConformers(self.combo, 
													self.bindingMode, mixed)

	def _createConformers(self, combo, binding, mixed):
		'''
		Create all the various possible conformations.  Dynammic programming is
		overkill but a good practice.  If ligands aren't mixed, don't need to
		actually create conformational variety because of symmetry.
		'''
		conformations = []
		prevConfs = {}

		initial = copy.deepcopy(binding.metal_ligand_list) # Create copy
		initial = self._replaceMetal(combo, initial)

		ligandList = combo.ligands

		if mixed:
			# Remember to make use of the prevConfs dict for DP, like would be
			# necessary for 2OH's and a hydride
			conformations = self._transformMixedLigs()
		else:
			conformations = self._transformSameLigs(initial, ligandList)
			
		return conformations

	def _replaceMetal(self, combo, conf_list):
		for elem in conf_list:
			if 'X' in elem:
				elem[0] = combo.metal.name
				break
		return conf_list

	def _transformSameLigs(self, coords, ligand_list):
		conformation = []
		conformation.append(list(coords[0]))
		for i, lig in enumerate(ligand_list):
			coord = np.array(coords[i+1][2:], dtype=np.float32)
			ligCoords = [atom[1:] for atom in lig.atom_list]
			ligCoords = np.array(ligCoords)
			ligCoords = coord + ligCoords
			newLig = self._prependAtomInfo(lig, ligCoords)
			for each in newLig:
				conformation.append(each)

		return conformation

	def _prependAtomInfo(self, ligand, coords):
		atoms = []
		for atom, coord in zip(ligand.atom_list, coords.tolist()):
			newAtom = []
			newAtom.append(str(atom[0]))
			newAtom.append('0')
			for i in range(3):
				newAtom.append(str(coord[i]))
				
			atoms.append(newAtom)
		
		return atoms
			
	
	def _transformMixedLigs(self):
		print "I'm not defined yet!"
		sys.exit()
