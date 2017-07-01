import os
import sys

def main():
	if len(sys.argv) < 2:
		print("Enter the name of the Source file to compile")
		exit(0)
	finalcode = ''
	found = False #found a comment

	with open(sys.argv[1], 'r') as f:
		for line in f:
			i = 0
			while i < len(line)-1:
				ch = line[i]
				nextc = line[i + 1]
				
				if(ch == '/' and nextc == '*'):
					found = True
					i += 2
					continue

				elif (found and (ch != '*' or nextc != '/')):
					i += 1
					continue

				elif found and ch == '*' and nextc == '/':
					found = False
					i += 2
					continue
				
				elif ch == '/' and nextc == '/':
					break

				finalcode += ch
				i+=1
			finalcode += line[len(line)-1]

	with open(sys.argv[1], 'w') as f:
		f.write(finalcode)


if __name__ == '__main__':
	main()