import os
import sys
import FnF


def listfiles():
	files = FnF.listfiles()
	files.sort()
	return files


if __name__ == "__main__":
	print('This program will print the version of python running, ' 
		'the current working directory and the files within that directory'
	)
	print('')
	print('python version: ', sys.version)
	print('cwd: ', os.getcwd())
	print('')
	files = listfiles()
	print(files)
