import cv
import pdb
import cv2
import numpy as np

def get_frames():
	imgPath = "/home/daniel/Dropbox/Georgia Tech/Classes/CS 4635/cs4635-project3/Representations/1/qframe_1-1.png"
	imgPath2 = "/home/daniel/Dropbox/Georgia Tech/Classes/CS 4635/cs4635-project3/Representations/6/sframe_4.png"
	single = '/home/daniel/Dropbox/Georgia Tech/Classes/CS 4635/cs4635-project3/Representations/6/qframe_1-1.png'
	im = cv.LoadImageM(imgPath, cv.CV_LOAD_IMAGE_GRAYSCALE)
	im2 = cv.LoadImageM(imgPath2, cv.CV_LOAD_IMAGE_GRAYSCALE)
	triangle = cv.LoadImageM(single, cv.CV_LOAD_IMAGE_GRAYSCALE)
	# (keypoints, descriptors) = cv.ExtractSURF(im, None, cv.CreateMemStorage(), (0, 30000, 3, 1))
	# print len(keypoints), len(descriptors)
	# print "descriptors: " + str(descriptors)
	# print "keypoints: " + str(keypoints)
	extractFeatures(single)

def extractFeatures(imagePath):
	img = cv.LoadImageM(imagePath, cv.CV_LOAD_IMAGE_GRAYSCALE)
	eig_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
	temp_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
	for (x,y) in cv.GoodFeaturesToTrack(img, eig_image, temp_image, 10, 0.04, 1.0, useHarris = True):
		print "good feature at", x,y
	print cv.GoodFeaturesToTrack(img, eig_image, temp_image, 10, 0.04, 1.0, useHarris = True)

	# contours2 = cv.FindContours(im2, cv.CreateMemStorage())
	# contours = cv.FindContours(im, cv.CreateMemStorage())
	
	# # print "count: " + str(count)
	# # print "count2: " + str(count2)
	# print "contours: " + str(contours)
	# print "contours2: " + str(contours2)
	# allContours = [contours]
	# temp = contours
	# for i in range(5):
	# 	if temp:
	# 		temp = temp.h_next()
	# 		allContours.append(contours)
	# for c in allContours:
	# 	print c

	# print "match_shape"
	# match_shape()
	# b = a.h_next()
	# c = a.h_next()
	# match1 = cv.MatchShapes(c,b, 1)
	

	# pdb.set_trace()

def match_shape():

	# Load the images
	img =cv2.imread('/home/daniel/Dropbox/Georgia Tech/Classes/CS 4635/cs4635-project3/Representations/6/sframe_4.png')

	# Convert them to grayscale
	imgg =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# SURF extraction
	# surf = cv2.SURF()
	# kp, descritors = surf.detect(imgg,None,useProvidedKeypoints = False)
	surf_detector = cv2.FeatureDetector_create("SURF")
	surf_descriptor = cv2.DescriptorExtractor_create("SURF")
	kp = surf_detector.detect(imgg)
	kp, descritors = surf_descriptor.compute(imgg, kp)

	# Setting up samples and responses for kNN
	samples = np.array(descritors)
	responses = np.arange(len(kp),dtype = np.float32)

	# kNN training
	knn = cv2.KNearest()
	knn.train(samples,responses)

	# Now loading a template image and searching for similar keypoints
	template = cv2.imread('/home/daniel/Dropbox/Georgia Tech/Classes/CS 4635/cs4635-project3/Representations/6/qframe_1-1.png')
	templateg= cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
	# keys,desc = surf.detect(templateg,None,useProvidedKeypoints = False)
	keys = surf_detector.detect(templateg)
	keys,desc = surf_descriptor.compute(templateg, keys)

	for h,des in enumerate(desc):
	    des = np.array(des,np.float32).reshape((1,128))
	    retval, results, neigh_resp, dists = knn.find_nearest(des,1)
	    res,dist =  int(results[0][0]),dists[0][0]

	    if dist<0.1: # draw matched keypoints in red color
	        color = (0,0,255)
	    else:  # draw unmatched in blue color
	        print dist
	        color = (255,0,0)

	    #Draw matched key points on original image
	    x,y = kp[res].pt
	    center = (int(x),int(y))
	    cv2.circle(img,center,2,color,-1)

	    #Draw matched key points on template image
	    x,y = keys[h].pt
	    center = (int(x),int(y))
	    cv2.circle(template,center,2,color,-1)

	cv2.imshow('img',img)
	cv2.imshow('tm',template)
	cv2.waitKey(0)
	cv2.destroyAllWindows()