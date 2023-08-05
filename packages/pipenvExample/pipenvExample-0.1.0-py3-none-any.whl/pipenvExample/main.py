import sys
import FnF


def listfiles():
	files = FnF.listfiles()
	files = files.sort()
	return files


if __name__ == "__main__":
	print(sys.version)
	files = listfiles()
	print(files)
