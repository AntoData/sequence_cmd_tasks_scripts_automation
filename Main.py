import os
import subprocess
import sys

f = None
aliases = {}
withalias = False

def loadAliases():
	"""
	This function loads the aliases we define in our file Aliases in folder files (./files/Aliases). 
	In order for our aliases to work they must have the following format:
	<command>	<module>.<function>
	For instance:
	cd	FoldersUtils.changeFolder
	This means, everytime a command starts with "cd" we will import the module FoldersUtils in folder "files" 
	(if not imported already) and execute the function "changeFolder" from that module.
	IMPORTANT: Don't use classes, use modules and functions. It won't work otherwise
	"""
	try:
		print("Loading aliases")
		print("Opening file Aliases")
		#We load the file Aliases from files which is where we set up which commands we want to replace and using which functions instead
		vConfig = open("./files/Aliases")
		#We just go through every line of that file
		for line  in vConfig:
			#We replace "\n" with nothing so it won't be in the names of our modules/functions
			line = line.replace("\n","")
			#We split that line using "\t"
			vars = line.split("\t")
			#We will have two elements at least, the first one, our command wh
			aliases[vars[0]] = [vars[1:]]
	except Exception as e:
		print("Something went wrong when loading our aliases: {0}".format(e))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	else:
		#Files should always be closed, so if our file was opened
		if(vConfig is not None):
			print("Closing file Aliases")
			#We close it
			vConfig.close()
			print("Success")

def processFile(f,dynamicParameters):
	"""
	This function processes the file where our commands to execute are and executes the commands.
	@param f: File where our commands to execute are
	@param dynamicParameters: Parameter or list of parameters that our user has given when asked through command line. We will replace each <parameter> we find
	in our lines for this dynamic parameters. If it is just one, we will replace all <parameter> for that parameter. If not, we will replace them in order.
	"""
	try:
		print("Process file")
		#We define a variable to control if we are inside a new machine/shell or not. By default we won't, so it is False. This is important
		#as if we connect to other machine, we won't be able to just execute our commands
		inanewshell = None
		#We get the number of dynamic parameters used in our file
		nDynamic = f.read().count("<parameter>")
		#If we provided one that one dynamic parameter through the keyboard, it is because we will replace them in order so we need to check that
		#the number of parameters we provided and the number of dynamic parameters the file expects match
		if(len(dynamicParameters)>1):
			#If the number of parameters we provided and the number of dynamic parameters the file expects don't match we should raise and exception
			#and finish our execution
			if(len(dynamicParameters) != nDynamic):
				raise Exception("The numbers of dynamic parameters provided and dynamic parameters in the config file don't match")
		#We need to rewind our file to the beging now to go line by line
		f.seek(0,0)
		#We get a line (a command) from our file in each iteration
		for line in f:
			#We clean all \n of our line
			line = line.replace("\n","")
			#If we have one or more dynamic parameters to replace
			if(line.count("<parameter>")>0):
				#If we provided more than one dynamic parameter
				if(len(dynamicParameters)>1):
					#For each instance of <parameter> in that line, we remove the first element in our list of dynamic parameters
					#and replace the current instance of <parameter> in the line
					for i in range(0,line.count("<parameter>")):
						dynamicParam = dynamicParameters.pop(0)
						#replace(old_str,new_str,max_count) replaces at most "max_count" instaces of old_str for new_str
						#in our case, we told it to replace just one
						line = line.replace("<parameter>",dynamicParam,1)
				else:
					#If we provided just one dynamic parameter, this means we will use the same parameter for all, so we can just replace it
					line = line.replace("<parameter>",dynamicParameters[0])
	
			print(line)
			#Now we check if our line is to be executed using aliases or is to be execute in our shell directly
			#So by default we say our line has no aliases defined
			withalias = False
			#And now we check if our line starts for that one of our aliases
			for com in aliases:
				if(line.startswith(com)):
					#If it does, we set withalias to True
					withalias = True
					#We load the value linked to our alias and we split it using .
					#That way we get the module and the function to execute
					module,function = aliases[com][0][0].split(".")
					#We import the module
					new_module = __import__(module)
					#We load the function from that module we set up to execute when we get that command in this line
					func = getattr(new_module, function)
					#Now we execute our command. We have two options:
					#We are inside a new machine, docker, shell... so we execute the function we defined for that command (in this case, we shall
					#always use aliases). In this case, we have to provide the object that represents that connection, which we shall return too
					if(inanewshell is not None):
						inanewshell = func(inanewshell,line)
					else:
						#Otherwise, if we are not inside a new machine, shell, docker... we just execute the function we defined, but we have to
						#return None if we are not in a new shell or True or an object representing that connection if we just connected to one
						inanewshell = func(line)
					break
			#If our command does not have an alias
			if(withalias == False):
				#We just execute it in our shell
				process = subprocess.Popen(line.split(" "), stdout=subprocess.PIPE)
				output, error = process.communicate()
				print(output)

	except Exception as e:
		print("Something went wrong when reading our file: {0}".format(e))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

def main():
	"""
	Main function to execute this program.
	"""
	try:
		#We load our aliases storing them in our global dictionary "aliases"
		loadAliases()
		#We ask the user to select which command list in folder files he want to load
		vFile = input("Select the file in folder \"Files\" with the sequence of commands: ")
		#We open the file selected by the user previously
		f = open("./files/"+vFile)
		#We ask the user which list of dynamic parameters he wants to use
		dynamicParametersCommandLine = input("Please, provide here the list of dynamic parameters separated with a blank space (if you provide only one, this will be used in all instances of dynmaic parameters): ")
		#We generate the list of dynamic parameters (splitting the list provided by the user)
		dynamicParameters = dynamicParametersCommandLine.split(" ")
		print(dynamicParameters)
		#We call to method processFile to start executing our commands
		processFile(f,dynamicParameters)
	except Exception as e:
		print("Something went wrong: {0}".format(e))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	else:
		#We always have to close opened files
		if(f is not None):
			f.close()
			print("Connection to file closed")
		print("Goodbye")

if __name__ == '__main__':
	main()
