import xml.etree.ElementTree as ET
import sys 
from sourcecode.Frame import *
from sourcecode.Analogy import *
from sourcecode.log import *
from sourcecode.ImageRepresentationExtractor import *
import copy
# for debugging
import pdb
import pprint
import time

""" 
	============================
	NEW TO DO
	create image library
	cretae method to find contiguous shapes
	consider how to do super imposed shapes...
	create way of identifying shapes (comparing) with the library and input. Property changes (filled, unfilled)? rotation? reflection?

	create representation for identified shapes
	============================


	Deleting and Adding figures from a frame 

	Matching of a rule to another rule - finish find_closest_rules_matching!

	No Need to add relationships between figures to the algorithm

	Consider all the rules! not just the best a->b rule, but rather loop through all of them
	and choose the one that has the least difference_value for the rules!

"""

def main():
	if "-log" in sys.argv:
		clean_log()
	# solve_project_4()
	helloWorldImage("Representations/Frames/Problem 4/3-4Ans2.png")

def solve_project_4():
	problem1XML = ET.parse("Representations/4-1.txt")
	problem2XML = ET.parse("Representations/4-2.txt")
	problem3XML = ET.parse("Representations/4-3.txt")
	problem4XML = ET.parse("Representations/4-4.txt")
	problem5XML = ET.parse("Representations/4-5.txt")
	problem6XML = ET.parse("Representations/4-6.txt")
	problem7XML = ET.parse("Representations/4-7.txt")
	problem8XML = ET.parse("Representations/4-8.txt")


	if "-1" in sys.argv:
		print_many_to_many_solution_project3(problem1XML, "1")
	if "-2" in sys.argv:
		print_many_to_many_solution_project3(problem2XML, "2")
	if "-3" in sys.argv:
		print_many_to_many_solution_project3(problem3XML, "3")
	if "-4" in sys.argv:
		print_many_to_many_solution_project3(problem4XML, "4")
	if "-5" in sys.argv:
		print_many_to_many_solution_project3(problem5XML, "5")
	if "-6" in sys.argv:
		print_many_to_many_solution_project3(problem6XML, "6")
	if "-7" in sys.argv:
		print_many_to_many_solution_project3(problem7XML, "7")
	if "-8" in sys.argv:
		print_many_to_many_solution_project3(problem8XML, "8")


	if len(sys.argv) == 1:
		print_many_to_many_solution_project3(problem1XML, "1")
		print_many_to_many_solution_project3(problem2XML, "2")
		print_many_to_many_solution_project3(problem3XML, "3")
		print_many_to_many_solution_project3(problem4XML, "4")
		print_many_to_many_solution_project3(problem5XML, "5")
		print_many_to_many_solution_project3(problem6XML, "6")
		print_many_to_many_solution_project3(problem7XML, "7")
		print_many_to_many_solution_project3(problem8XML, "8")



def solve_project_3():
	problem1XML = ET.parse("Representations/3-1.txt")
	problem2XML = ET.parse("Representations/3-2.txt")
	problem3XML = ET.parse("Representations/3-3.txt")
	problem4XML = ET.parse("Representations/3-4.txt")
	problem5XML = ET.parse("Representations/3-5.txt")
	problem6XML = ET.parse("Representations/3-6.txt")
	problem7XML = ET.parse("Representations/3-7.txt")
	problem8XML = ET.parse("Representations/3-8.txt")


	if "-1" in sys.argv:
		print_many_to_many_solution_project3(problem1XML, "1")
	if "-2" in sys.argv:
		print_many_to_many_solution_project3(problem2XML, "2")
	if "-3" in sys.argv:
		print_many_to_many_solution_project3(problem3XML, "3")
	if "-4" in sys.argv:
		print_many_to_many_solution_project3(problem4XML, "4")
	if "-5" in sys.argv:
		print_many_to_many_solution_project3(problem5XML, "5")
	if "-6" in sys.argv:
		print_many_to_many_solution_project3(problem6XML, "6")
	if "-7" in sys.argv:
		print_many_to_many_solution_project3(problem7XML, "7")
	if "-8" in sys.argv:
		print_many_to_many_solution_project3(problem8XML, "8")


	if len(sys.argv) == 1:
		print_many_to_many_solution_project3(problem1XML, "1")
		print_many_to_many_solution_project3(problem2XML, "2")
		print_many_to_many_solution_project3(problem3XML, "3")
		print_many_to_many_solution_project3(problem4XML, "4")
		print_many_to_many_solution_project3(problem5XML, "5")
		print_many_to_many_solution_project3(problem6XML, "6")
		print_many_to_many_solution_project3(problem7XML, "7")
		print_many_to_many_solution_project3(problem8XML, "8")


def print_many_to_many_solution_project3(problem, problem_id):
	t0 = time.clock()
	[pframes, pqframes, psolutions, missing] = deSerializeXML(problem)
	# print pframes
	# print pframes[2].figures
	# print pqframes
	# print psolutions
	# print missing
	# pdb.set_trace()
	psolution = solve_analogy_many_to_many(pframes, psolutions, missing)
	print "\nProblem " + str(problem_id) + ": " + str(psolution['sframe'].index) + " took " + str(time.clock()-t0) + " time"

def solve_project_2():
	problem1XML = ET.parse("Representations/2-1.txt")
	problem2XML = ET.parse("Representations/2-2.txt")
	problem3XML = ET.parse("Representations/2-3.txt")
	problem4XML = ET.parse("Representations/2-4.txt")
	problem5XML = ET.parse("Representations/2-5.txt")
	problem6XML = ET.parse("Representations/2-6.txt")
	problem7XML = ET.parse("Representations/2-7.txt")
	problem8XML = ET.parse("Representations/2-8.txt")


	if "-1" in sys.argv:
		print_many_to_many_solution(problem1XML, "1")
	if "-2" in sys.argv:
		print_many_to_many_solution(problem2XML, "2")
	if "-3" in sys.argv:
		print_many_to_many_solution(problem3XML, "3")
	if "-4" in sys.argv:
		print_many_to_many_solution(problem4XML, "4")
	if "-5" in sys.argv:
		print_many_to_many_solution(problem5XML, "5")
	if "-6" in sys.argv:
		print_many_to_many_solution(problem6XML, "6")
	if "-7" in sys.argv:
		print_many_to_many_solution(problem7XML, "7")
	if "-8" in sys.argv:
		print_many_to_many_solution(problem8XML, "8")


	if len(sys.argv) == 1:
		print_many_to_many_solution(problem1XML, "1")
		print_many_to_many_solution(problem2XML, "2")
		print_many_to_many_solution(problem3XML, "3")
		print_many_to_many_solution(problem4XML, "4")
		print_many_to_many_solution(problem5XML, "5")
		print_many_to_many_solution(problem6XML, "6")
		print_many_to_many_solution(problem7XML, "7")
		print_many_to_many_solution(problem8XML, "8")

def solve_project_1():
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
	if len(sys.argv) == 1:
		printSolution(problem1XML, "1")
		printSolution(problem2XML, "2")
		printSolution(problem3XML, "3")
		printSolution(problem4XML, "4")


def printSolution(problem, problem_id):
	[pframes, pqframes, psolutions, missing] = deSerializeXML(problem)
	psolution = solve_analogy_one_to_one(pframes, pqframes, psolutions)
	if len(psolution) == 1:
		print "\nProblem " + str(problem_id) + ": " + psolution[0]['sframe']
		# print "Problem " + str(problem_id) + ": " + str(psolution)
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

def print_many_to_many_solution(problem, problem_id):
	t0 = time.clock()
	[pframes, pqframes, psolutions, missing] = deSerializeXML(problem)
	psolution = solve_analogy_many_to_many(pframes, psolutions, missing)
	print "\nProblem " + str(problem_id) + ": " + str(psolution['sframe'].index) + " took " + str(time.clock()-t0) + " time"




if __name__ == '__main__':
	main()