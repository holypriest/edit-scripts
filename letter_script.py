from manuscript import Manuscript
from author import Author
from letter import Letter

input_file = open('input.txt', 'r')
for line in input_file:
	line = line.strip()
	info = line.split('\t')
	msid = info[0]
	manuscript = Manuscript(msid)
	auth_info = [info[1], info[2], info[3], info[4]]
	author = Author(auth_info)
	letter = Letter(author, manuscript)
	letter.generate()
input_file.close()