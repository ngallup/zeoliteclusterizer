from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get description
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='zeoliteclusterizer',
	version='0.1.1',
	description='A python module built for rapid computational screening of catalysts on rigid structures',
	url='https://github.com/ngallup/zeoliteclusterizer',

	author='Nathan Gallup',
	author_email='gallup@chem.ucla.edu',

	license='Free for non-commercial use',

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Chemistry',
		'License :: Free for non-commercial use',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3'
	],

	keywords='chemistry quantum mechanics zeolites mofs catalysis gaussian',

	packages=find_packages(exclude=['*tests/tests/*']),
)
