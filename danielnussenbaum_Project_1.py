import xml.etree.ElementTree as ET
import sys 
from Frame import *
import copy
# for debugging
import pdb
import pprint

tags = [ "frame", "qframe", "sframe"]

""" 
	Deleting and Adding figures from a frame 

	Matching of a rule to another rule - finish find_closest_rules_matching!

	No Need to add relationships between figures to the algorithm

	Consider all the rules! not just the best a->b rule, but rather loop through all of them
	and choose the one that has the least difference_value for the rules!

"""

def main():
	print "Deserialising"
	example1XML = ET.parse("examples/example-based-on-1-1.xml")
	problem1XML = ET.parse("problems/1-1.xml")
	problem2XML = ET.parse("problems/1-2.xml")
	problem3XML = ET.parse("problems/1-3.xml")
	# problem4XML = ET.parse("1-4.xml")

	[e1frames, e1qframes, e1solutions] = deSerializeXML(example1XML)
	e1solution = solve_analogy(e1frames, e1qframes, e1solutions)
	# pdb.set_trace()
	if len(e1solution) == 1:
		print "Example 1: " + e1solution[0]['sframe']
		print "Example 1: " + str(e1solution)
	else:
		print "\nExample 1 had the following " + str(len(e1solution)) + " solutions:"
		for sol_index in range(len(e1solution)):
			print "\t" + str(sol_index) + ". " + str(e1solution[sol_index])

	[p1frames, p1qframes, p1solutions] = deSerializeXML(problem1XML)
	p1solution = solve_analogy(p1frames, p1qframes, p1solutions)
	if len(p1solution) == 1:
		print "Problem 1: " + p1solution[0]['sframe']
		print "Problem 1: " + str(p1solution)
	else:
		print "\nProblem 1 had the following " + str(len(p1solution)) + " solutions:"
		for sol_index in range(len(p1solution)):
			print "\t" + str(sol_index) + ". " + str(p1solution[sol_index])

	[p2frames, p2qframes, p2solutions] = deSerializeXML(problem2XML)
	p2solution = solve_analogy(p2frames, p2qframes, p2solutions)
	if len(p2solution) == 1:
		print "Problem 2: " + p2solution[0]['sframe']
		print "Problem 2: " + str(p2solution)
	else:
		print "\nProblem 2 had the following " + str(len(p2solution)) + " solutions:"
		for sol_index in range(len(p2solution)):
			print "\t" + str(sol_index) + ". " + str(p2solution[sol_index])


	[p3frames, p3qframes, p3solutions] = deSerializeXML(problem3XML)
	p3solution = solve_analogy(p3frames, p3qframes, p3solutions)
	if len(p3solution) == 1:
		print "Problem 3: " + p3solution[0]['sframe']
		print "Problem 3: " + str(p3solution)
	else:
		print "\nProblem 3 had the following " + str(len(p3solution)) + " solutions:"
		for sol_index in range(len(p3solution)):
			print "\t" + str(sol_index) + ". " + str(p3solution[sol_index])

		if len(p3solution) >= 4:
			for i in [1,3]:
				print "\n\n\n\n\n" + str(i) + ":"
				pprint.pprint(p3solution[i])
				print "\n\n\n"
				p3_rule_matchings = p3solution[i]['rule_matchings']
				for rm in p3_rule_matchings:
					pprint.pprint(rm)
					pprint.pprint(str(rm[0]) + " : " + str(rm[0].get_change_value()))
					pprint.pprint(str(rm[1]) + " : " + str(rm[1].get_change_value()))
					pprint.pprint(rm[0].get_difference_with_rule(rm[1]))
	# pprint.pprint()
	# pdb.set_trace()



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
	closest_matching = find_closest_frames_matching(frames) 

	question_solution_combinations = [[questionFrames[0], sol] for sol in solutions]
	closest_matching_to_solutions = []
	for qs_combo in question_solution_combinations:
		closest_matching_to_solutions.append(find_closest_frames_matching(qs_combo))

	# print "\n\n\nclosest_matching_to_solutions: " + str(closest_matching_to_solutions)

	# Now we have to compare the current question -> solutions rules matchings to the best closets matching of A->B (call it r_ab) 
	# and choose the one that is least different to our r_ab
	# We must do a matching between rules r_{1,j} and rules r_{2,i} to minimize the possible difference
	# Once we have a best matching for 2 sets of rules, we compare all sets of rules and choose the one with the lowest difference
	# to our r_ab set of rules. Note that now the shape is not nearly as important as before, and it can be weighted much closer
	# to other rules (like location) than before

	# since right now we only have sets of 1 rules, proceed
	best_sol_so_far = [closest_matching_to_solutions[0]]
	for  curr_sol in closest_matching_to_solutions:
		# pdb.set_trace()
		# curr_sol["difference_value"] = closest_matching["rules"][0].get_difference_with_rule(curr_sol["rules"][0])
		curr_sol_rules_matching = find_closest_rules_matching(closest_matching["rules"], curr_sol["rules"])
		curr_sol["difference_value"] = curr_sol_rules_matching["difference_value"]
		curr_sol["rule_matchings"] = curr_sol_rules_matching["rule_matchings"]
		if best_sol_so_far[0]["difference_value"] > curr_sol["difference_value"]:
			best_sol_so_far = [curr_sol]
		elif best_sol_so_far[0]["difference_value"] == curr_sol["difference_value"]:
			best_sol_so_far.append(curr_sol)

	# print "curr_sol: " + str(curr_sol) + " is the best answer!"

	# pdb.set_trace()
	# print closest_matching
	# or find list of possible matchings for A - B considering rules and number of changes and possible matchings of figures
	# find the rules also from C - X
	# now compare rules from A - B to those from C - X
	return best_sol_so_far
	# return closest_matching_to_solutions











def find_closest_rules_matching(rules_y, rules_x): # instead of rules, return a list of 2-tuples of figures (rules) matched!

	if len(rules_y) == 0 and len(rules_x) == 0:
		# print "Decide what to return here. Should this ever be evaluated?" TODO
		return {"rule_matchings": [], "difference_value": 0} 
	elif len(rules_y) == 0:
		# print "I am not currently considering deletion and/or addition cases" TODO
		# print rules_x TODO
		# 10 is the penalty for objects created from scracth. This should be a constant and not hard coded! change later!
		return {"rule_matchings": [(None, rules_x)], "difference_value": len(rules_x)*10} 
	# elif len(rules_x) == 0:
	# 	print "should I be doing this? will this ever happen? It seems that if it does, before, it would just return" 
	# 	print "the closest_matching below with value -1...and hence not be accepted anyway. Figure it out!" 
	elif len(rules_y) > 0:
		curr_y_rule = rules_y[0]
		possibleRules = []
		for index_x in range(len(rules_x) + 1):
			if index_x == len(rules_x):
				stringToPrint = "deletion case. I am not currently considering this possibility for rules"
				# print stringToPrint TODO
			else:
				curr_x_rule = rules_x[index_x]
				rules_y_copy = copy.deepcopy(rules_y)
				rules_x_copy = copy.deepcopy(rules_x)
				rules_y_copy.remove(rules_y_copy[0])
				rules_x_copy.remove(rules_x_copy[index_x])
				best_rule_matching = find_closest_rules_matching(rules_y_copy, rules_x_copy)
				# rule_a_b = curr_y_rule.get_rule_to_match(curr_x_rule) 
				possibleRules.append(
					{	
					"rule_matchings": best_rule_matching["rule_matchings"] + [(curr_y_rule, curr_x_rule)], # [rule_a_b], 
					"difference_value": best_rule_matching["difference_value"] + curr_y_rule.get_difference_with_rule(curr_x_rule)
					})
		closest_matching = {"difference_value": -1, "rule_matchings": []}
		for pr in possibleRules:
			if closest_matching["difference_value"] == -1:
				closest_matching = pr
			elif closest_matching["difference_value"] > pr["difference_value"]:
				closest_matching = pr

		return closest_matching

	return "find_closest_rules_matching() has failed to find a matching rule"











def find_closest_frames_matching(frames):
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
	a_frame = frames[0]
	b_frame = frames[1]

	if len(a_frame.figures) == 0 and len(b_frame.figures) == 0:
		# print "Decide what to return here. Should this ever be evaluated?" # This is just the terminal case
		return {"rules": [], "value": 0} 
	elif len(a_frame.figures) == 0 or len(b_frame.figures) == 0:
		# consider the case when there are no more figures remaining in a_frame, but there are some figures
		# remaining in b_frame. This case calls for a rule of adding one figure and matching it. there are len(b_frame.figures)!
		# turns to do this, but they are all really equivalent, then we can do this in just one turn by creating rules.
		# note that even though this case should always be evaluated, since the addition has a +10 weight, it should never be 
		# preferred over some transformation of a_frame.figures, unless none of those were deleted previously.
		x_frame_figures = a_frame.figures or b_frame.figures
		created_rules = []
		created_rules_value = 0
		for curr_x_fig in x_frame_figures:
			curr_rule_created = curr_x_fig.get_rule_create_delete()
			created_rules.append(curr_rule_created)
			created_rules_value += curr_rule_created.get_change_value()

		# print "I am not currently considering deletion and/or addition cases"
		# print b_frame.figures
		# print "I am now considering addition and deletion cases, and the result is this: " + str(created_rules_value)
		return {"rules": created_rules, "value": created_rules_value} 
	elif len(a_frame.figures) > 0:
		curr_a_fig = a_frame.figures[0]
		possibleRules = []
		for index_b in range(len(b_frame.figures) + 1):
			if index_b == len(b_frame.figures):
				# consider deletion case for curr_a_fig
				# stringToPrint = "deletion case. I am not currently considering this possibility"
				# print stringToPrint
				# pdb.set_trace()
				frames_copy = copy.deepcopy(frames)
				frames_copy[0].figures.remove(frames_copy[0].figures[0])
				best_rule = find_closest_frames_matching(frames_copy)
				rule_a_delete = curr_a_fig.get_rule_create_delete() 
				possibleRules.append(
							{	"rules": best_rule["rules"] + [rule_a_delete], 
								"value": best_rule["value"] + rule_a_delete.get_change_value(),
								"qframe": a_frame.index,
								"sframe": b_frame.index
							}
						)
			else:
				# consider matching of curr_a_fig to b_frame.figures[index_b]
				# pdb.set_trace()
				curr_b_fig = b_frame.figures[index_b]
				frames_copy = copy.deepcopy(frames)
				frames_copy[0].figures.remove(frames_copy[0].figures[0])
				frames_copy[1].figures.remove(frames_copy[1].figures[index_b])
				# print "\n\nClosest Matching Called"
				best_rule = find_closest_frames_matching(frames_copy)
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