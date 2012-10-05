import os

def log(message):
	mfile = open(os.getcwd() + "/log.txt", "a")
	mfile.write(message + "\n")
	mfile.close()