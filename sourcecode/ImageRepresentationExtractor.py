import pdb
import Image
import subprocess
import operator
import PIL.ImageOps 
import ImageFilter
from numpy import *
import numpy
import ImageChops
import os

def helloWorldImage(imagePath):
	Problem1ImageSolver()

def helloWorldImage1(imagePath):
	print "hello world!"
	im = Image.open(imagePath)
	# print im.format, im.size, im.mode
	# print im
	# im.show()

	a2 = Image.open("Representations/Frames/Problem 4/3-4Ans2.png")
	a3 = Image.open("Representations/Frames/Problem 4/3-4Ans3.png")
	a38 = Image.open("Representations/Frames/Problem 10/3-8H.png")
	a23 = Image.blend(a2,a3,0.5)
	# a23.show()
	b = asarray(a23)
	c = a23.crop((0,0,10,10))
	# c.show()
	c1 = asarray(c)
	# print c1
	# print b

	# filepathArray = imagePath.split("/")
	# filepathArray = filepathArray[0:-1]
	# filepath = ""
	# for s in filepathArray:
	# 	filepath = filepath + "/" + s
	# filepath = filepath + "/1.jpg"
	im = im.filter(ImageFilter.FIND_EDGES)
	a38 = a38.filter(ImageFilter.FIND_EDGES)
	a38.show()
	c2 = asarray(im)
	c2 = c2[1:-1]
	c2 = Image.fromarray(c2)
	c2 = c2.rotate(90)
	c2 = asarray(c2)
	c2 = c2[1:-1]
	c2 = Image.fromarray(c2)
	c2 = c2.rotate(-90)
	c2.show()
	print c2.getbbox()
	c2.crop(c2.getbbox()).show()
	# im.show()
	# im.rotate(45).show()
	# im.show()
	# print im.getbbox()
	# print dir(im)
	# im.save("my_new_image.jpg")

	# subprocess.call(('xdg-open', "my_new_image.jpg"))

def Problem1ImageSolver():
	ABC_solver("Representations/Frames/Problem 1/")

	[dirImagesQuestions, dirImagesAnswers] = get_images_for_directory("Representations/Frames/Problem 1/")
	print "Problem 1 Image Questions: \n=================="
	compare_k = dirImagesQuestions.keys()[0]
	compare_v = dirImagesQuestions[compare_k]
	compare_v = ImageChops.invert(compare_v)
	compare_v = findRelevantBoxEdges(compare_v)
	# print compare_k
	for k,v in dirImagesQuestions.iteritems():
		temp_v = ImageChops.invert(dirImagesQuestions[k])
		temp_v = findRelevantBoxEdges(temp_v)
		image_equality = check_shape_equality(compare_v, temp_v)
		equality_string = ""
		if not image_equality:
			equality_string = "different"
		else:
			equality_string = "equal with " + image_equality[1] + " transformation"
		print str(k) + " and " + str(compare_k) + " are " + equality_string

	print "\nProblem 1 Image Answers: \n=================="
	for k,v in dirImagesAnswers.iteritems():
		temp_v = ImageChops.invert(dirImagesAnswers[k])
		temp_v = findRelevantBoxEdges(temp_v)
		# if compare_v.size != temp_v.size:
		# 	print str(compare_k) + " is " + str(compare_v.size) + " but " + str(k) + " is " + str(temp_v.size)
		image_equality = check_shape_equality(compare_v, temp_v)
		equality_string = ""
		if not image_equality:
			equality_string = "different"
		else:
			equality_string = "equal with " + image_equality[1] + " transformation"
		print str(k) + " and " + str(compare_k) + " are " + equality_string

	# qa = Image.open("Representations/Frames/Problem 1/3-1A.png")
	# # qa.show()
	# qaInverted = ImageChops.invert(qa)
	# # qaInverted.show()
	# qb = Image.open("Representations/Frames/Problem 1/3-1B.png")
	# qbInverted = ImageChops.invert(qb)
	# # qbInverted.show()
	# # qb.show()
	# qaBox = findRelevantBoxEdges(qaInverted)
	# # qaBox.show()
	# qbBox = findRelevantBoxEdges(qbInverted)
	# # qbBox.show()

	# ab_equals = check_shape_equality(qaBox, qbBox)

	# diffAB = ImageChops.difference(qaBox, qbBox)
	# # diffAB.show()
	# sumAB = ImageChops.add(qbBox, qaBox)
	# # sumAB.show()
	# # BminusA = ImageChops.subtract(qbBox, qbBox)
	# # BminusA.show()
	# print count_nonzero(asarray(qaBox)) #.count([255,255,255])
	# print count_nonzero(asarray(qbBox)) #.count([255,255,255])
	



def findRelevantBoxEdges(image):
	""" This takes as input a PIL Image """
	# edgesImage = image.filter(ImageFilter.FIND_EDGES)
	# imageArray = asarray(edgesImage)
	# imageArray = imageArray[1:-1] # This removes top and bottom row which are marked as edges because the background is white
	# imageArray = Image.fromarray(imageArray)
	# imageArray = imageArray.rotate(90)
	# imageArray = asarray(imageArray)
	# imageArray = imageArray[1:-1] # This removes left and right row which are marked as edges because the background is white
	# edgesImage = Image.fromarray(imageArray)
	# edgesImage = edgesImage.rotate(-90)

	edgesImage = image

	# edgesImage.show()
	# print edgesImage.getbbox()
	# edgesImage.crop(edgesImage.getbbox()).show()
	edgesImage = edgesImage.crop(edgesImage.getbbox())
	return edgesImage


def get_images_for_directory(myDir):
	""" Given a path in the form of a string, returns an array of Images """
	dirImagesQuestions = {}
	dirImagesAnswers = {}
	for r,d,f in os.walk(myDir):
	    for files in f:
	        if files.endswith(".png") or files.endswith(".jpg") or files.endswith(".jpeg") :
	             # print os.path.join(r,files) + " has mode " + Image.open(os.path.join(r, files)).mode
	             curr_image = Image.open(os.path.join(r, files))
	             curr_image = curr_image.convert("RGBA")
	             if "Ans" in files:
	             	dirImagesAnswers[files] = curr_image
	             else:
	             	dirImagesQuestions[files] = curr_image
	return [dirImagesQuestions, dirImagesAnswers]

def check_shape_equality(image_a, image_b):
	""" This method assumes the images passed to it are contiguous shapes and have no inner shapes """
	curr_a = image_a
	curr_b = image_b
	if curr_a.size != curr_b.size:
		max_size = max(curr_a.size[0], curr_a.size[1], curr_b.size[0], curr_b.size[1])
		curr_a = Image.new(image_a.mode, (max_size,max_size))
		# curr_a = ImageChops.add(image_a, curr_a)
		curr_a.paste(image_a, (0,0))
		curr_b = Image.new(image_b.mode, (max_size,max_size))
		# print curr_b
		# curr_b = ImageChops.add(curr_b, image_b)
		# print curr_b
		# pdb.set_trace()
		curr_b.paste(image_b,(0,0))
		# FOUND PROBLEM. MODES ARE NOT THE SAME! WHY, WHO KNOWS. CAN WE CHANGE THEM INTO ALL BEING RGBA?

		# need to make a method add images together that converts them into an array, deep copies, and then copies relevant 
		# non black pixels from one image to another...then this avoids the issue presented here by ImageChops.add which
		# takes two images, and when adding them, only retains the size of the smallest!
	difference_acceptance = 0.05
	a_pixels = count_nonzero(asarray(curr_a))
	b_pixels = count_nonzero(asarray(curr_b))
	# pdb.set_trace()
	if (abs(0.0 + a_pixels-b_pixels)/max(a_pixels, b_pixels)) < difference_acceptance:
		best_rotation = find_best_rotation(curr_a, curr_b)
		return best_rotation
	else: return False

def find_best_rotation(image_a, image_b):
	""" 
	This method assumes the images passed to it are contiguous shapes and have no inner shapes 
	It further assumes that the images provided are the cropped bboxes of the shapes

	"""
	# image.rotate(angle, NEAREST, False)
	# image.transpose() FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90, ROTATE_180, or ROTATE_270
	# transforms = [Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270, ]
	rotations = [None, Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270]
	reflections = [None, Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM]
	transform_names = {Image.FLIP_LEFT_RIGHT: "Image.FLIP_LEFT_RIGHT", Image.FLIP_TOP_BOTTOM: "Image.FLIP_TOP_BOTTOM", 
						Image.ROTATE_90:"Image.ROTATE_90", Image.ROTATE_180:"Image.ROTATE_180", Image.ROTATE_270:"Image.ROTATE_270",
						None: "None"}
	
	diff_ab = ImageChops.difference(image_a, image_b)
	curr_best_diff = count_nonzero(asarray(diff_ab))
	curr_best_transform = (None, None)
	transforms_values = [curr_best_diff]
	transforms_values_dic = {}

	for rot in rotations:
		if rot != None:
			temp_image_b_rot = image_b.transpose(rot)
		else:
			temp_image_b_rot = ImageChops.duplicate(image_b)
		for ref in reflections:
			if ref != None:
				temp_image_b_rot_ref = temp_image_b_rot.transpose(ref)
			else:
				temp_image_b_rot_ref = ImageChops.duplicate(temp_image_b_rot)

			temp_diff_ab = ImageChops.difference(image_a, temp_image_b_rot_ref)
			transforms_values += [count_nonzero(asarray(temp_diff_ab))]
			transforms_values_dic[(rot,ref)] = [count_nonzero(asarray(temp_diff_ab))]

			if count_nonzero(asarray(temp_diff_ab)) < curr_best_diff:
				curr_best_diff = count_nonzero(asarray(temp_diff_ab))
				diff_ab = temp_diff_ab
				curr_best_transform = (rot,ref)

	return [curr_best_transform, transform_names[curr_best_transform[0]] + " and " + transform_names[curr_best_transform[1]], curr_best_diff]


# def non_equal_sized_image_add(image_a, image_b):
# 	array_a = asarray(image_a)
# 	array_b = asarray(image_b)
# 	max_size = max(image_a.size[0], image_a.size[1], image_b.size[0], image_b.size[1])
# 	my_new_image = Image.new(image_b.mode, (max_size,max_size))
# 	my_new_image_array = asarray(my_new_image)
# 	for i in range(size())

def ABC_solver(images_path):
	print "hello!"