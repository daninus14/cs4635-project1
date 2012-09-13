import xml.etree.ElementTree as ET
import sys 
from Frame import *
import copy
# for debugging
import pdb

tags = [ "frame", "qframe", "sframe"]

""" 
	Deleting and Adding figures from a frame 

	Matching of a rule to another rule

	Need to add relationships between figures to the algorithm

"""

def main():
	print "Deserialising"
	Example1XML = ET.parse("examples/example-based-on-1-1.xml")
	# problem1XML = ET.parse("1-1.xml")
	# problem2XML = ET.parse("1-2.xml")
	# problem3XML = ET.parse("1-3.xml")
	# problem4XML = ET.parse("1-4.xml")

	[e1frames, e1qframes, e1solutions] = deSerializeXML(Example1XML)
	solution = solve_analogy(e1frames, e1qframes, e1solutions)
	print "\n\n\n\nExample 1: " + solution



def solve_analogy(frames, questionFrames, solutions):
	""" Search exhaustively the rules space

		For example, if there is one shape in each of two frames, let them be semi-circles.
		Let the second semi-circle be larger. Then, there are 2 possible mathings.

		4 you say! 4 I say! there is the A to B, delete A and add B

		If there are 2 figures in A, and 2 in B, then there are
		delete both +1 , delete one +2 * choose target to be addedd * 2, transform both +2 = 1 + 4 + 2 = 7 ways
	"""
	# print "solveAnalogy"
	# print "questionFrames: " + str(questionFrames)
	# print "frames: " + str(frames)
	# print "solutions: " + str(solutions)
	closest_matching = find_closest_matching(frames) 

	question_solution_combinations = [[questionFrames[0], sol] for sol in solutions]
	closest_matching_to_solutions = []
	for qs_combo in question_solution_combinations:
		closest_matching_to_solutions.append(find_closest_matching(qs_combo))

	# print "\n\n\nclosest_matching_to_solutions: " + str(closest_matching_to_solutions)

	# Now we have to compare the current question -> solutions rules matchings to the best closets matching of A->B (call it r_ab) 
	# and choose the one that is least different to our r_ab
	# We must do a matching between rules r_{1,j} and rules r_{2,i} to minimize the possible difference
	# Once we have a best matching for 2 sets of rules, we compare all sets of rules and choose the one with the lowest difference
	# to our r_ab set of rules. Note that now the shape is not nearly as important as before, and it can be weighted much closer
	# to other rules (like location) than before

	# since right now we only have sets of 1 rules, proceed
	best_sol_so_far = closest_matching_to_solutions[0]
	for  curr_sol in closest_matching_to_solutions:
		curr_sol["difference_value"] = closest_matching["rules"][0].get_difference_with_rule(curr_sol["rules"][0])
		if best_sol_so_far["difference_value"] > curr_sol["difference_value"]:
			best_sol_so_far = curr_sol

	# print "curr_sol: " + str(curr_sol) + " is the best answer!"

	# pdb.set_trace()
	# print closest_matching
	# or find list of possible matchings for A - B considering rules and number of changes and possible matchings of figures
	# find the rules also from C - X
	# now compare rules from A - B to those from C - X
	return str(best_sol_so_far) # "still, nothing yet"

def find_closest_matching(frames):
	""" This is a recursive function! 
		this method will get the first figure on frame A and match it to n (# figures in frame B) + 1 possible choices
		for frame B, which are a match between any 2, and 1 for deletion. Or actually, just n*2 because whenever deleted, 
		must decide with which of n other figures to match to.

		Then, it calls the same for the C - X frames, and then when it has the best rules for those, it compares each one
		to the best from A-B and then whichever one is the most similar, it selects it and returns its index

		This calls a get_rule_to_match method, from the Figure class, which creates (or finds the best of many) rule to 
		convert this figure to another. Must find out if shape transform is possible (it seems it is not!).

		As of now this method is searching for exact rules to transform frame A to frame B, however, the exactness of
		such matching depends on how well different rules work with the possible solutions for C to X.
	"""
	result = False
	a_frame = frames[0]
	b_frame = frames[1]

	if len(a_frame.figures) == 0 and len(b_frame.figures) == 0:
		print "Decide what to return here. Should this ever be evaluated?"
		return {"rules": [], "value": 0} 
	elif len(a_frame.figures) == 0:
		# consider the case when there are no more figures remaining in a_frame, but there are some figures
		# remaining in b_frame. This case calls for a rule of adding one figure and matching it. there are len(b_frame.figures)!
		# turns to do this, but they are all really equivalent, then we can do this in just one turn by creating rules.
		# note that even though this case should always be evaluated, since the addition has a +10 weight, it should never be 
		# preferred over some transformation of a_frame.figures, unless none of those were deleted previously.
		print "I am not currently considering deletion and/or addition cases"
		print b_frame.figures
		return {"rules": [], "value": 0} 
	elif len(a_frame.figures) > 0:
		curr_a_fig = a_frame.figures[0]
		possibleRules = []
		for index_b in range(len(b_frame.figures) + 1):
			if index_b == len(b_frame.figures):
				# consider deletion case for curr_a_fig
				print "deletion case. I am not currently considering this possibility"
			else:
				# consider matching of curr_a_fig to b_frame.figures[index_b]
				# pdb.set_trace()
				curr_b_fig = b_frame.figures[index_b]
				frames_copy = copy.deepcopy(frames)
				# frames_copy[0].figures.remove(curr_a_fig)
				frames_copy[0].figures.remove(frames_copy[0].figures[0])
				# frames_copy[1].figures.remove(curr_b_fig)
				frames_copy[1].figures.remove(frames_copy[1].figures[index_b])
				# print "\n\nClosest Matching Called"
				best_rule = find_closest_matching(frames_copy)
				# print "best_rule: " + str(best_rule)
				rule_a_b = curr_a_fig.get_rule_to_match(curr_b_fig) 
				# print "rule_a_b: " + str(rule_a_b)
				# print "rules: " + str(best_rule["rules"] + [rule_a_b])
				# print "value: " + str(best_rule["value"] + rule_a_b.get_change_value())
				possibleRules.append(
							{	"rules": best_rule["rules"] + [rule_a_b], 
								"value": best_rule["value"] + rule_a_b.get_change_value(),
								"qframe": a_frame.index,
								"sframe": b_frame.index
							}
						)
		closest_matching = {"value": -1, "rules": [], "qframe": a_frame.index, "sframe": b_frame.index}
		for pr in possibleRules:
			# print "pr: " + str(pr)
			if closest_matching["value"] == -1:
				closest_matching = pr
			elif closest_matching["value"] > pr["value"]:
				closest_matching = pr

		# print "closest_matching: " + str(closest_matching)

		return closest_matching

	return "find_closest_matching() has failed to find a matching rule"

def deSerializeXML(problem):
	""" This method is to get the frames, questionFrames, and solutions nodes """
	allFrames = problem.getroot().getchildren()
	frames = []
	questionFrames = []
	solutions = []

	for frame in allFrames:
		if frame.tag == tags[0]:
			frames.append(Frame.deSerializeXML(frame))
		elif frame.tag == tags[1]:
			questionFrames.append(Frame.deSerializeXML(frame))
		elif frame.tag == tags[2]:
			solutions.append(Frame.deSerializeXML(frame))
		else:
			print "frame tag " + str(frame.tag) + " is not recognized"

	return [frames, questionFrames, solutions]


if __name__ == '__main__':
	main()