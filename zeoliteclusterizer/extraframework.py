import sys
import string

class Properties(object):
	'''
	A base class for ligands, metals, etc., that contains some basic
	chemical properties.  Charges and number of unpaired electrons can
	be provided as a list if multiple states are phyiscally accessible, as is
	often the case with metals
	'''
	def __init__(self, charge_list, unpaired_list):
		try:
			self.charge = set(charge_list)
			unpaired_list = [each % 2 for each in unpaired_list]
			self.unpaired = set(unpaired_list)
		except:
			print("You probably gave me an int when it should have been an iterable",
					sys.exc_info()[0])
			raise


class Metal(Properties):
	'''
	A class for metals to contain physical properties.
	'''
	def __init__(self, name, charges, unpaired):
		super(Metal, self).__init__(charges, unpaired)
		self.name = str(name)

class Ligand(Metal):
	'''
	A class for handling ligands which can consist of more than one atom and
	could potentially have multiple charge and multiplicity states, although
	this latter possibility would be rare.

	atom_list should consist of a string and three numbers, e.g.:
		[['H', 0.0, 0.0, 1.0], ...]
	'''
	def __init__(self, name, atom_list, charges, unpaired, 
						headInd=0, tailInd=None):
		super(Ligand, self).__init__(name, charges, unpaired)

		self._head, self._headIndex = None, None
		self._tail, self._tailIndex = None, None

		# Will defer final print to Gaussian output handler
		self.atom_list = self.convertToFloats(atom_list)

		# Need to set the connecting atom; can be changed by user
		self.setHead(headInd)
		if tailInd == None:
			if len(self.atom_list) > 1:
				self.setTail(1)
			else:
				self.setTail(0)
		else:
			self.setTail(tailInd)

	def convertToFloats(self, atom_list):
		'''
		It is conceivable that a user might read in coordinates from a file,
		thus it's important that the resulting strings be converted into floats
		to maintain the ability to easily transform coordinates, and control
		final output printing
		'''
		newList = []
		for element in atom_list:
			# Want to ignore elemental string and examine rest
			tmp = [element[0]]
			for i in range(1, 4):
				element[i] = float(element[i])
				tmp.append(element[i])
			newList.append(tmp)

		return newList

	def setHead(self, index):
		'''
		The head atom is the atom connecting directly to the metal.  It is the
		gateway into the rest of the ligand.  The head and tail are different
		only when the ligand is greater than 1 atom
		'''
		self._head = self.atom_list[index]
		self._headIndex = index
	
	def setTail(self, index):
		'''
		The tail is the second atom used to form a vector between the head and
		the tail that is utilized for geometric transformations
		'''
		self._tail = self.atom_list[index]
		self._tailIndex = index

	def getHead(self):
		return self._head

	def getTail(self):
		return self._tail

	def getHeadIndex(self):
		return self._headIndex

	def getTailIndex(self):
		return self._tailIndex 

class Combination(object):
	'''
	'''
	def __init__(self):
		self.metal = None
		self.ligands = []
		self._hashval = None
		self._strings = []
		self.charge = 0
		self.unpaired = 0

	def isMetal(self, metal):
		if type(metal) == Metal:
			return True
		return False

	def isLigand(self, lig):
		if type(lig) == Ligand:
			return True
		return False

	def addMetal(self, metal, charge, unpaired):
		self.metal = metal
		self._strings.append(metal.name)
		self.updateHashVal(charge, unpaired)

	def addLigand(self, lig, charge, unpaired):
		self.ligands.append(lig)
		self._strings.append(lig.name)
		self.updateHashVal(charge, unpaired)

	def updateHashVal(self, charge, unpaired):
		# Implement binary insertion at some point or implement custom char
		# order ignorant hashing scheme (e.g. h = sum(c*x^2)) to avoid the
		# O(n log n) sort and O(n) join
		self.updateElectrons(charge, unpaired)
		self._strings = sorted(self._strings)
		tmp = [ string for string in self._strings ]
		tmp.append( '(%d)(%d)' % (self.charge, self.unpaired))
		self._hashval = ''.join(tmp)
		#self._hashval = self._hashval.join(tmp)

	def updateElectrons(self, charge, unpaired):
		self.charge += charge
		self.unpaired = (self.unpaired + unpaired) % 2

	def getNumLigands(self):
		return len(self.ligands)
	
	
'''
Some common ligands are listed below
'''
hydroxide_pos = [
            ['O', 0.00000000, 0.00000000, 0.00000000],
            ['H', 0.00000000, 0.00000000, -1.00000000]
         ]
hydroxide = Ligand('OH', hydroxide_pos, [-1], [0])

hydride_pos = [ ['H', 0.0, 0.0, 0.0] ]
hydride = Ligand('Hydride', hydride_pos, [-1], [0])

oxide_pos = [ ['O', 0.0, 0.0, 0.0] ]
oxide = Ligand('Oxide', oxide_pos, [-2], [0])
