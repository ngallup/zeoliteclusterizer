
import sys
from Extraframework import Combination
from Scaffolds import AbstractMode
from Gaussian import OutputTest

class Clusterizer(object):
	'''
	The Clusterizer is the meat of ZeoliteClusterizer, hence the name.  It tries
	to take advantage of dynamic programming practices to streamline the
	metal-ligand combinatorics.

	The basic intended workflow is like this:
	(1) Place binding modes in hash table, using ligand number as key
	(2) Feed parameters to combinations method, accumulate allowed Combinations
			using DP concepts based on electronic parameters
	(3) Iterate over allowed combinations, matching to modes in hash table
	(4) Create conformational variety of each Combination-Mode match
	(5) Write conformations to disk
	'''
	def __init__(self, scaffold, binding_list, metals, 
					ligands, charges=[0], unpaired=[[0]], mix_ligands=True):

		# Need hash tables of binding modes and counter charges
		self.maxLigs = 0
		self._modes = self.makeModesHashTable(binding_list)
		self._cCharges = self.makeChargesHashTable(scaffold, charges, unpaired)
		self.combinations = []
		self.finalModes = None

		if mix_ligands == False:
			for metal in metals:
				self.makePureCombinations(scaffold, binding_list, metal, ligands, 
													charges, unpaired)
		else:
			self.makeMixCombinations(scaffold, binding_list, metal, ligands,
											charges, unpaired, combos)

		abstractModes = [AbstractMode(combo, mode, scaffold, mixed=False) 
			for combo, mode in self.matchingModes(self.combinations, self._modes)]

		self.finalModes = abstractModes

	def makeModesHashTable(self, binding_modes):
		'''
		Returns a hash table consisting of binding modes with the ligand number
		as the key with values consisting of a list of modes that contain that
		number of ligands
		'''
		hashTable = {}

		for mode in binding_modes:
			ligNum = mode.getNumLigands()
			if ligNum > self.maxLigs:
				self.maxLigs = ligNum
			if ligNum not in hashTable:
				hashTable[ligNum] = [mode]
			else:
				hashTable[ligNum].append(mode)
		
		return hashTable

	def makeChargesHashTable(self, scaffold, charges, unpaireds):
		hashTable = {}
		for charge, unpaired in zip(charges, unpaireds):
			charge -= scaffold.charge
			hashTable[charge] = unpaired
		return hashTable

	def makePureCombinations(self, scaffold, binding_list, metal, ligands, 
									charge, unpaired):
		'''
		Since we're only specifying pure ligand combinations, we can use
		simple math to construct combinations
		'''
		prevCombos = {}

		# This needs to be refactored ASAP because it reads like ass.  Maybe
		# implement a method object or some other abstract concept.  Maybe a
		# generator would be a good fit.  Maybe just break into smaller methods
		# Note: this is not yet handling counter radicals like it should in the
		# _cCharge dict
		for metalCharge in metal.charge:
			for metalUnpaired in metal.unpaired:
				for lig in ligands:
					newCombo = Combination()
					newCombo.addMetal(metal, metalCharge, metalUnpaired)
					if not self.isPrevCombo(newCombo, prevCombos):
						if (self.isCounterCharge(newCombo) and
								newCombo.getNumLigands() in self._modes):
							self.combinations.append(newCombo)
					prevCombos = self.addToComboDict(newCombo, prevCombos)
					for charge in lig.charge:
						for cCharge in self._cCharges:
							tmpCombo = None
							ligsToAdd = (newCombo.charge - cCharge) / (-charge)
							if (ligsToAdd > 0 and ligsToAdd in self._modes):
								tmpCombo = self.addLigs(newCombo, lig, ligsToAdd)
								if not self.isPrevCombo(tmpCombo, prevCombos):
									self.combinations.append(tmpCombo)
									prevCombos = self.addToComboDict(tmpCombo, 
																				prevCombos)

	
	def isCounterCharge(self, combination):
		if combination.charge in self._cCharges:
			return True
		return False

	def isPrevCombo(self, combination, combo_dict):
		if combination._hashval in combo_dict:
			return True
		return False

	def addToComboDict(self, combination, combo_dict):
		combo_dict[combination._hashval] = combination
		return combo_dict

	def addLigs(self, combination, ligand, numToAdd):
		for _ in range(numToAdd):
			# Note: change ligand class to only have one charge and one 
			# unpaired.  Otherwise is overcomplicated
			charge = list(ligand.charge)[0]
			unpaired = list(ligand.unpaired)[0]
			combination.addLigand(ligand, charge, unpaired)
		return combination

	def makeMixCombinations(self, scaffold, binding_list, metal, ligands,
									charge, unpaired):
		print("Mixed combinations not implemented yet!")
		sys.exit()

	def matchingModes(self, combo_list, modes_list):
		for combo in combo_list:
			numLigs = combo.getNumLigands()
			for mode in modes_list[numLigs]:
				yield combo, mode

	def getFinalModes(self):
		return self.finalModes

