#We import the module os to handle the change of folder
import os
#We import re so we can perform operations with regular expression
import re
#We import sys so we can end our execution if we get an exception
import sys

def isChangeDirectory(command):
	"""
	This function checks if our command is a cd command
	@param command: The command we want to check
	@return:  True if cd command, False if not
	"""
	if command.startswith("cd"):
		return True
	else:
		return False

def environmentVariablesPattern(command):
	"""
	This function searchs for environment variables in our path
	@param command: Command where we want to find environment variables
	@return: a list with all the environment variables used in this command
	"""
	#We define a pattern that searchs for string that start with $ and end or not with /
	pattern = r"\$[^/]+[ |/]?"
	#We compile our regular expression
	regexp = re.compile(pattern)
	#We return all the environment variables used in a list
	return re.findall(pattern,command)

def getPathEnvironment(command):
	"""
	This method replaces environment variables for their current value
	@param command: Command where we want to replace environment variable for their current value
	@return: the command where the environment variables have been replaced
	"""
	#We get the environment variables used in the command in order
	envVars = environmentVariablesPattern(command)
	#We define an empty path to our folder	
	pathFolder = ""
	#We replace each enviromment variable in our command variable by variable
	for envVar in envVars:
		#We clean all $ and / off our variable
		envVar1 = envVar.replace('$','')
		envVar1 = envVar1.replace('/','')
		#We get the value of this environment variable
		path = os.environ.get(envVar1)
		#We replace our environment variable
		command = command.replace(envVar,path+"/")
	#We return our command with their environment variables replaced
	return command


def changeFolder(command):
	"""
	This function changes the current folder to the one we set in command
	@param command: cd command
	"""
	#We clean all \n off our command
	command = command.replace("\n","")
	#We replace all the environment variables in our path
	varCom = getPathEnvironment(command)
	#We erase "cd " from our command as we are not going to use it
	varCom = varCom.replace("cd ","")	
	try:
		#We try to change our current folder
		os.chdir(varCom)
	except:
		print("The folder {0} does not exist".format(varCom))
		sys.exit()
