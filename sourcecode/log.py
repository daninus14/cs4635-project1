import os


def clean_log():
	mfile = open(os.getcwd() + "/log.txt", "w")
	mfile.write(message + "\n")
	mfile.close()

def log(message):
	mfile = open(os.getcwd() + "/log.txt", "a")
	mfile.write(message + "\n")
	mfile.close()