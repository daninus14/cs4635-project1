from sourcecode.Frame import *
import xml.etree.ElementTree as ET
import sys 
from sourcecode.Frame import *
from sourcecode.Analogy import *
from sourcecode.log import *
import copy
# for debugging
import pdb
import pprint

tags = [ "frame", "qframe", "sframe"]


def solve_analogy_many_to_many(frames, solutions, missing):

	# print "missing: " + str(missing)
	
	[frames_by_row, frames_by_column] = get_frames_by_row_and_column(frames)

	# NEED TO ADD DIAGONAL ANALYSIS!

	combination_frames_by_row = get_combinations_of_each_vector(frames_by_row)

	combination_frames_by_column = get_combinations_of_each_vector(frames_by_column)

	
	superrules_by_row = get_super_rules_by_vector(combination_frames_by_row)
	superrules_by_column = get_super_rules_by_vector(combination_frames_by_column)

	# print "superrules_by_row: " + str(superrules_by_row) 
	# print "superrules_by_column: " + str(superrules_by_column) 
	# print "combination_frames_by_row: " + str(combination_frames_by_row)
	# print "combination_frames_by_column: " + str(combination_frames_by_column)
	# print "frames_by_row: " + str(frames_by_row)
	# print "frames_by_column: " + str(frames_by_column)


	solution_values = []
	for sframe in solutions:
		sys.stdout.write("|")
		sys.stdout.flush()
		# print "\n" + str(sframe)
		srow = frames_by_row[missing[0]-1]
		scolumn = frames_by_column[missing[1]-1]
		combinations_srow = get_combinations_of_vector_with_element(srow, sframe)
		combinations_scolumn = get_combinations_of_vector_with_element(scolumn, sframe)

		row_sr = get_super_rule_from_vector(combinations_srow)
		# print "row_sr: " + str(row_sr)
		# print "srow: " + str(srow)
		# print "sframe: " + str(sframe)
		# print "combinations_srow: " + str(combinations_srow)
		column_sr = get_super_rule_from_vector(combinations_scolumn)

		def diff_super_rule(x): return x[0].get_difference_with_super_rule(x[1])
		row_super_rule_combinations = get_combinations_of_vector_with_element(superrules_by_row, row_sr)
		row_sr_value = reduce(lambda x, y: x + y, map(diff_super_rule, row_super_rule_combinations))
		row_sr_change_value = row_sr.get_change_value()
		# print "row_sr.get_change_value(): " + str(row_sr.get_change_value())
		# print "row_super_rule_combinations: " + str(row_super_rule_combinations)
		# print "super_rule_diff: " + str(row_super_rule_combinations[0])
		# print "map(diff_super_rule, row_super_rule_combinations): " + str(map(diff_super_rule, row_super_rule_combinations))
		# print "row_sr_value: " + str(row_sr_value)
		column_super_rule_combinations = get_combinations_of_vector_with_element(superrules_by_column, column_sr)
		column_sr_value = reduce(lambda x, y: x + y, map(diff_super_rule, column_super_rule_combinations))
		column_sr_change_value = column_sr.get_change_value() 
		# print "column_sr_value:" + str(column_sr_value)
		# print "combined: " + str(column_sr_value + row_sr_value)
		final_value = column_sr_value + row_sr_value + column_sr_change_value + row_sr_change_value
		solution_values.append({"row_sr_change_value":row_sr_change_value, "column_sr_change_value":column_sr_change_value, "sframe":sframe, "value": final_value})

	solution_values.sort(key = lambda x: x["value"])
	print solution_values
	pdb.set_trace()
	return solution_values[0]

def get_frames_by_row_and_column(frames):
	frames_dictionary = {}
	for frame in frames:
		frames_dictionary[frame.index] = frame
	rows = []
	columns = []
	for k in frames_dictionary.keys():
		rows.append(k[0])
	for k in frames_dictionary.keys():
		columns.append(k[1])
	rows = max(rows)
	columns = max(columns)

	frames_by_row = []
	for i in range(1, rows+1):
		i_rows_frames = []
		for k in frames_dictionary.keys():
			if k[0] == i:
				i_rows_frames.append(frames_dictionary[k])
		frames_by_row.append(i_rows_frames)

	frames_by_column = []
	for i in range(1, columns+1):
		i_columns_frames = []
		for k in frames_dictionary.keys():
			if k[1] == i:
				i_columns_frames.append(frames_dictionary[k])
		frames_by_column.append(i_columns_frames)


	return [frames_by_row, frames_by_column]

def get_combinations_of_vector_with_element(vector_of_elements, element):
	element_combinations = []
	for curr_element in vector_of_elements:
		element_combinations.append([curr_element, element])
	return element_combinations

def get_combinations_of_vector(frames_vector):
	frame_combinations = []
	for i in range(len(frames_vector)):
		for j in range(i+1,len(frames_vector)):
			frame_combinations.append([frames_vector[i], frames_vector[j]])
	return frame_combinations
	

def get_combinations_of_each_vector(frames_by_vector):
	combination_frames_by_vector = []
	for curr_vector_frames in frames_by_vector:
		frame_combinations = get_combinations_of_vector(curr_vector_frames)
		if len(frame_combinations) > 0: combination_frames_by_vector.append(frame_combinations)
	return combination_frames_by_vector

def get_super_rules_by_vector(combination_frames_by_vector):
	superrules_by_vector = []
	for combinations_for_vector in combination_frames_by_vector:
		sr = get_super_rule_from_vector(combinations_for_vector)
		sys.stdout.write(">")
		sys.stdout.flush()
		superrules_by_vector.append(sr)
	return superrules_by_vector

def get_super_rule_from_vector(combinations_for_vector):
	super_rule = None
	for combination in combinations_for_vector:
		sys.stdout.write("+")
		sys.stdout.flush()
		curr_matching = find_closest_frames_matching(combination)
		# print "curr_matching: " + str(curr_matching)
		curr_matching.sort(key = lambda x: x["value"])
		best_matching = curr_matching[0]
		start_rules_index = 0
		if super_rule == None: 
			super_rule = SuperRule(best_matching["rules"][0])
			start_rules_index = 1
		else:
			for rule_index in range(start_rules_index, len(best_matching["rules"])):
				super_rule.combine_with_rule(best_matching["rules"][rule_index])
	return super_rule

def solve_analogy_one_to_one(frames, questionFrames, solutions):
	previous_matching = find_closest_frames_matching(frames) 
	sys.stdout.write(".")
	sys.stdout.flush()
	question_solution_combinations = [[questionFrames[0], sol] for sol in solutions]
	previous_matching_to_solutions = []
	for qs_combo in question_solution_combinations:
		sys.stdout.write(".")
		sys.stdout.flush()
		previous_matching_to_solutions += find_closest_frames_matching(qs_combo)
	best_sol_so_far = previous_matching_to_solutions[0]
		
	rules_list_compare_values = []

	for curr_closest_matching in previous_matching:

			for curr_sol in previous_matching_to_solutions:
				sys.stdout.write(".")
				sys.stdout.flush()
				curr_sol_rules_matching = find_closest_rules_matching(curr_closest_matching["rules"], curr_sol["rules"])
				rules_list_compare_values += [(curr_sol_rules_matching["difference_value"], abs(curr_closest_matching["value"] - curr_sol["value"]), curr_closest_matching, curr_sol)]

				rules_list_compare_values.sort(key = lambda x: x[0] + x[3]["value"])

				curr_sol["difference_value"] = curr_sol_rules_matching["difference_value"]
				curr_sol["rule_matchings"] = curr_sol_rules_matching["rule_matchings"]
				if best_sol_so_far["difference_value"] > curr_sol["difference_value"]:
					best_sol_so_far = curr_sol
	
	best_sol_so_far = rules_list_compare_values[0]
	return [best_sol_so_far[3]]

def find_closest_rules_matching(rules_y, rules_x): 
	debug = False

	if len(rules_y) == 0 and len(rules_x) == 0:
		return {"rule_matchings": [], "difference_value": 0} 
	elif len(rules_y) == 0:
		return {"rule_matchings": [(None, rules_x)], "difference_value": len(rules_x)*10} 
	elif len(rules_y) > 0:
		curr_y_rule = rules_y[0]
		possibleRules = []
		for index_x in range(len(rules_x)):
			if index_x == len(rules_x):
				stringToPrint = "deletion case. I am not currently considering this possibility for rules"
				return {"rule_matchings": [], "difference_value": 0} 
				debug = True
			else:
				curr_x_rule = rules_x[index_x]
				rules_y_copy = copy.deepcopy(rules_y)
				rules_x_copy = copy.deepcopy(rules_x)
				rules_y_copy.remove(rules_y_copy[0])
				rules_x_copy.remove(rules_x_copy[index_x])
				best_rule_matching = find_closest_rules_matching(rules_y_copy, rules_x_copy)
				possibleRules.append(
					{	
					"rule_matchings": best_rule_matching["rule_matchings"] + [(curr_y_rule, curr_x_rule)], # [rule_a_b], 
					"difference_value": best_rule_matching["difference_value"] + curr_y_rule.get_difference_with_rule(curr_x_rule) # + curr_y_rule.get_change_value()
					})
		closest_matching = {"difference_value": -1, "rule_matchings": []}
		for pr in possibleRules:
			if closest_matching["difference_value"] == -1:
				closest_matching = pr
			elif closest_matching["difference_value"] > pr["difference_value"]:
				closest_matching = pr

		if debug : print "closest_matching: " + str(closest_matching)

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
		# sys.stdout.write(".")
		# sys.stdout.flush()
		return [{"rules": [], "value": 0} ]
	elif len(a_frame.figures) == 0 or len(b_frame.figures) == 0:
		# sys.stdout.write(".")
		# sys.stdout.flush()
		x_frame_figures = a_frame.figures or b_frame.figures
		created_rules = []
		created_rules_value = 0
		for curr_x_fig in x_frame_figures:
			curr_rule_created = curr_x_fig.get_rule_create_delete()
			created_rules.append(curr_rule_created)
			created_rules_value += curr_rule_created.get_change_value()
		return [{"rules": created_rules, "value": created_rules_value}]

	elif len(a_frame.figures) > 0:
		curr_a_fig = a_frame.figures[0]
		possibleRules = []
		for index_b in range(len(b_frame.figures) + 1):
			if index_b == len(b_frame.figures):
				frames_copy = copy.deepcopy(frames)
				frames_copy[0].figures.remove(frames_copy[0].figures[0])
				previous_possible_rules = find_closest_frames_matching(frames_copy)
				rule_a_delete = curr_a_fig.get_rule_create_delete() 
				for curr_previous_rule in previous_possible_rules:
					possibleRules.append(
								{	"rules": curr_previous_rule["rules"] + [rule_a_delete], 
									"value": curr_previous_rule["value"] + rule_a_delete.get_change_value(),
									"qframe": a_frame.index,
									"sframe": b_frame.index
								}
							)
			else:
				curr_b_fig = b_frame.figures[index_b]
				frames_copy = copy.deepcopy(frames)
				frames_copy[0].figures.remove(frames_copy[0].figures[0])
				frames_copy[1].figures.remove(frames_copy[1].figures[index_b])
				previous_possible_rules = find_closest_frames_matching(frames_copy)
				rule_a_b = curr_a_fig.get_rule_to_match(curr_b_fig) 
				for curr_previous_rule in previous_possible_rules:
					possibleRules.append(
								{	"rules": curr_previous_rule["rules"] + [rule_a_b], 
									"value": curr_previous_rule["value"] + rule_a_b.get_change_value(),
									"qframe": a_frame.index,
									"sframe": b_frame.index
								}
							)
		return possibleRules


def deSerializeXML(problem):
	""" This method is to get the frames, questionFrames, and solutions nodes """
	allFrames = problem.getroot().getchildren()
	missing_frame = ""
	if "missing" in problem.getroot().attrib.keys():
		missing_frame = eval(problem.getroot().attrib["missing"])
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

	return [frames, questionFrames, solutions, missing_frame]