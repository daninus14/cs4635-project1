import xml.etree.ElementTree as ET
import sys 
from sourcecode.Frame import *
from sourcecode.Analogy import *
import copy
# for debugging
import pdb
import pprint

""" 
	Deleting and Adding figures from a frame 

	Matching of a rule to another rule - finish find_closest_rules_matching!

	No Need to add relationships between figures to the algorithm

	Consider all the rules! not just the best a->b rule, but rather loop through all of them
	and choose the one that has the least difference_value for the rules!

"""

def main():
	problem1XML = ET.parse("Representations/1-1.txt")
	problem2XML = ET.parse("Representations/1-2.txt")
	problem3XML = ET.parse("Representations/1-3.txt")
	problem4XML = ET.parse("Representations/1-4.txt")

	if "-1" in sys.argv:
		printSolution(problem1XML, "1")
	if "-2" in sys.argv:
		printSolution(problem2XML, "2")
	if "-3" in sys.argv:
		printSolution(problem3XML, "3")
	if "-4" in sys.argv:
		printSolution(problem4XML, "4")


def printSolution(problem, problem_id):
	[pframes, pqframes, psolutions] = deSerializeXML(problem)
	psolution = solve_analogy(pframes, pqframes, psolutions)
	if len(psolution) == 1:
		print "Problem " + str(problem_id) + ": " + psolution[0]['sframe']
		print "Problem " + str(problem_id) + str(psolution)
	else:
		print "\nProblem " + str(problem_id) + " had the following " + str(len(psolution)) + " solutions:"
		for sol_index in range(len(psolution)):
			print "\t" + str(sol_index) + ". " + str(psolution[sol_index])

		if len(psolution) >= 4:
			for i in [1,3]:
				print "\n\n\n\n\n" + str(i) + ":"
				pprint.pprint(psolution[i])
				print "\n\n\n"
				p_rule_matchings = psolution[i]['rule_matchings']
				for rm in p_rule_matchings:
					pprint.pprint(rm)
					pprint.pprint(str(rm[0]) + " : " + str(rm[0].get_change_value()))
					pprint.pprint(str(rm[1]) + " : " + str(rm[1].get_change_value()))
					pprint.pprint(rm[0].get_difference_with_rule(rm[1]))
	# pprint.pprint()
	# pdb.set_trace()

if __name__ == '__main__':
	main()