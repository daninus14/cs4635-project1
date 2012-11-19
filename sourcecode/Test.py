import xml.etree.ElementTree as ET
import sys 
from Frame import *
from Analogy import *
from log import *
import copy
# for debugging
import pdb
import pprint


def main():
	test_step_by_step()

def test_step_by_step(frames, solutions, missing):
	print "frames: \n"
	pprint.pprint(frames)
	[frames_by_row, frames_by_column] = get_frames_by_row_and_column(frames)

	# NEED TO ADD DIAGONAL ANALYSIS!

	combination_frames_by_row = get_combinations_of_each_vector(frames_by_row)

	combination_frames_by_column = get_combinations_of_each_vector(frames_by_column)

	
	superrules_by_row = get_super_rules_by_vector(combination_frames_by_row)
	superrules_by_column = get_super_rules_by_vector(combination_frames_by_column)

if __name__ == '__main__':
	main()