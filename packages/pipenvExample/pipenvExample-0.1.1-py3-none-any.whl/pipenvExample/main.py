import os
import sys
import FnF


def listfiles():
	files = FnF.listfiles()
	files.sort()
	return files


if __name__ == "__main__":
	print(sys.version)
	print(os.getcwd())
	files = listfiles()
	print(files)
