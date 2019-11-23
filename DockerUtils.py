#We import the module docker to handle the connections to docker containers
import docker
import os
import sys

def getDockerConnectionByContainerName(line):
	"""
	This function handles the connection to the first docker container. In this case, as this is designed for Emergya's dockers, the first one is the one we shall log
	and we return that object
	@param line: Line with our command, alias plus container name. It has to be a word for the aliases, a blank space and the name
	@return requested container
	"""
	try:
		#First we get the name of the container we want to connect to
		containerName = line.split(" ")[1]
		#We get the client to connect to docker
		client = docker.from_env()
		#We login as root
		client.login('root')
		#We get the list of containers in our system
		lContainers = client.containers.list()
		#We go container by container, if we find one whose name is the same as the container we requested, we return that object container
		for container in lContainers:
			print(container.name)
			if(container.name==containerName):
				return container
	except Exception as e:
		print("Something went wrong when connecting our docker: {0}".format(e))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

def getDockerConnectionByContainerID(line):
	"""
	This function handles the connection to the first docker container. In this case, as this is designed for Emergya's dockers, the first one is the one we shall log
	and we return that object
	@param line: Line with our command, alias plus container ID. It has to be a word for the aliases, a blank space and the ID
	@return the first container
	"""
	try:
		#First we get the name of the container we want to connect to
		containerID = line.split(" ")[1]
		#We get the client to connect to docker
		client = docker.from_env()
		#We login as root
		client.login('root')
		vContainer = None
		#We get the list of containers in our system
		lContainers = client.containers.list()
		#We go container by container, if we find one whose ID is the same as the container we requested, we return that object container
		for container in lContainers:
			print(container.id)
			if(container.id.startswith(containerID)):
				return container
	except Exception as e:
		print("Something went wrong when connecting our docker: {0}".format(e))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

def stopDockerConnection(*args):
	"""
	This method handles the disconnection from our docker machine
	@param *args: Just to comply with the restrictions of these kind of methods in our script
	@return None so we exit the part of the main flow designed to execute command inside a new shell, docker, machine...
	"""
	try:
		#We get the client to connect to docker
		client = docker.from_env()
		#We close the connection
		client.close()
		return None
	except Exception as e:
		print("Something went wrong when disconnecting from our docker: {0}".format(e))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

def execute_command(dockerContainer,command):
	"""
	This method executes the command in the parameter "command" in the docker container in "dockerContainer"
	@param dockerContainer: Docker container where we want to execute our command
	@param command: Command to execute
	@return dockerContainer to comply with the restrictions of these kind of methods in our script
	"""
	try:
		#We execute the command in our docker and get the output of our command
		exit_code, outputcommand = dockerContainer.exec_run(command)
		#We print the output of our command
		print(outputcommand)
		#We have to return our dockerContainer to comply with the restrictions of our script
		return dockerContainer
	except Exception as e:
		print("Something went wrong when executing a command in our docker: {0}".format(e))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
