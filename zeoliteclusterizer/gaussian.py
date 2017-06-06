
from abc import ABCMeta, abstractmethod
import string
import os

class GaussianInput(object):
	'''
	An abstract class containing useful base methods for handling
	and parsing Gaussian input files (Specifically G09-type)
	'''
	
	__metaclass__ = ABCMeta

	@abstractmethod
	def getLoc():
		'''Return absolute file location'''
		pass

	def readHeader(self, line_list):
		# Need to read in header information and parse out extraneous stuff
		# (chk, etc.)

		header = []
		title_index = 0
		charge = 0
		mult = 0
		unpaired_e = 0

		for index, line in enumerate(line_list):
			if 'Title Card Required' in line:
				title_index = index
				break
			if '%' in line:
				continue
			header.append(line.rstrip())

		# Need to get rid of extra line between head and title card
		header.pop()
		header = str(*header)

		# Need to gather charges and unpaired electrons
		charge_mult = line_list[title_index+2].split()
		charge = int(charge_mult[0])
		mult = int(charge_mult[1])
		unpaired_e = mult - 1

		atom_start = title_index + 3

		return header, charge, unpaired_e, atom_start

	def readAtoms(self, start_ind, lines):
		# Returns a list of atomtype, frozen(y/n), x, y, z coordinates

		atom_list = []

		for index, line in enumerate(lines[start_ind:]):
			atomtype = None
			frozen = None
			x, y, z = None, None, None

			split_line = list(line.split())

			if self.startsWithLetter(split_line) == False:
				break
			elif self.frozenIsSpecified(split_line) == False:
				self.addSplit(split_line, atom_list, frozen='0')
			else:
				self.addSplit(split_line, atom_list)

		return atom_list
	
	def addSplit(self, split_line, atom_list, frozen=None):
		# Helper function for splitting atom lines into components.  If frozen
		# is default, parses like normal.  Otherwise utilizes the provided
		# value for frozen

		atomtype = None
		x, y, z = None, None, None

		if frozen == None:
			atom_list.append(split_line)
		else:
			atomtype = split_line[0]
			x, y, z = split_line[1], split_line[2], split_line[3]
			result = [atomtype, frozen, x, y, z]
			atom_list.append(result)

	def frozenIsSpecified(self, atom_line):
		# Returns boolean of whether or not a frozen/non-frozen coordinate
		# is specified within a gaussian input line

		if atom_line[1] == '0' or atom_line[1] == '-1':
			return True
		return False

	def startsWithLetter(self, atom_line):
		# Return boolean of whether or not the provided input line begins
		# with a letter, primarily for identifying atom lines

		if atom_line == []:
			return False
		elif atom_line[0][0] in string.ascii_letters:
			return True
		return False

class OutputTest(object):
	def write(self, num, mode):
		with open('tests/test%s.com' % num, 'w') as outfile:
			for line in mode.scaffold.head_lines:
				outfile.write(''.join(line))
			outfile.write('\n\nTest\n\n0 1\n')
			for line in mode.scaffold.atom_list:
				outfile.write(' '.join(line))
				outfile.write('\n')
			for line in mode.conformations:
				outfile.write(' '.join(line))
				outfile.write('\n')

class Output(object):
	'''
	Abstract base class for all output file formats
	'''

	__metaclass__ = ABCMeta

	@abstractmethod
	def writeAllModes():
		pass
	@abstractmethod
	def write():
		pass

	def __init__(self, disp_frozen, atom_width, frozen_width, 
					coord_width, coord_digits):
		self.frozen = disp_frozen
		self.atom_width = atom_width
		self.frozen_width = frozen_width
		self.coord_width = coord_width
		self.coord_digits = coord_digits

class G09Output(Output):
	'''
	For writing final binding modes to disk in a G09 compatible fashion
	'''

	def __init__(self, dir):
		super(G09Output, self).__init__(True, 5, 5, 7, 5)
		self.dir = os.path.abspath(dir)

	def writeAllModes(self, absModes, header=None, footer=None, makedirs=False):
		'''
		Write all conformations for the provided AbstractModes into the provided
		directory.  Use hash table to iterate conformation number.  See write
		method for more details.
		'''
		# Note: writeAllModes is not properly set up to handle the mixed
		# conformations that would exists as mixed ligand sets in 
		# mode.conformations.
		hashtable = {}

		for mode in absModes:
			hval = mode.combo._hashval
			if hval not in hashtable:
				hashtable[hval] = 0
			hashtable[hval] += 1
			conf = hashtable[hval]

			name = [s for s in mode.combo._strings]
			charge = str(mode.combo.charge + mode.scaffold.charge)
			unpaired = (mode.combo.unpaired + mode.scaffold.unpaired) % 2
			mult = str(unpaired+1)
			unpaired = str(unpaired)
			name.append('_charge%s_%set_conf%d' % (charge, mult, conf))
			name = ''.join(name)
			
			name = os.path.join(self.dir, name)
			if makedirs == True:
				os.makedirs(name)
				name = os.path.join(name, os.path.basename(name))

			self.write(mode, name, charge=charge, mult=mult)
	
	def write(self, mode, name, charge='0', mult='1', header=None, footer=None):
		'''
		Write a single file.  Name should have the absolute path prepended to the
		.com filename.  If alternative headers and footers are provided, write
		those instead of what's provided in the ScaffoldRing.  The header should
		exclude the Title Card Required line because it will be added in by the
		method.
		'''
		if header == None:
			header = mode.scaffold.head_lines

		with open(name + '.com', 'w') as comfile:
			check = '%chk=' + os.path.basename(name) + '.chk' + '\n'
			comfile.write(check)
			comfile.write(header.rstrip('\n') + '\n')
			
			comfile.write('\nAutomatically Generated by ZeoliteClusterizer\n\n')
			comfile.write('%s %s\n' % (charge, mult))

			# Refactor these for loops as some point
			for line in mode.scaffold.atom_list:
				# Think of a way to make this not look like garbage
				params = (self.atom_width, line[0], self.frozen_width, line[1], 
							self.coord_digits, float(line[2]), self.coord_digits, 
							float(line[3]), self.coord_digits, float(line[4]))
				comfile.write('%-*s %-*s %-*f %-*f %-*f\n' % params)

			for line in mode.conformations:
				params = (self.atom_width, line[0], self.frozen_width, line[1],
                     self.coord_digits, float(line[2]), self.coord_digits,
                     float(line[3]), self.coord_digits, float(line[4]))
				comfile.write('%-*s %-*s %-*f %-*f %-*f\n' % params)

			comfile.write('\n')
			if footer != None:
				comfile.write(footer)

			comfile.write('\n\n\n')
