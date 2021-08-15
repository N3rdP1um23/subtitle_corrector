#!/bin/python

#
# N3rdP1um23
# August 15, 2021
# The following script is used to handle removing uppercase words from subtitle files
#

# Import the required packages
import os
import re

# The following function is used to handle displaying the main menu
def menu():
	# Create a vriable that store the current selection
	selection = ''

	# Display the menu
	print('-----------------------------------------')
	print('')
	print('            Uppercase Remover            ')
	print('')
	print('1. Run Script')
	print('2. Exit')
	print('')
	print('-----------------------------------------')
	print('')

	# Loop until the user decides to exit
	while selection == '' or (selection.isdigit() and int(selection) != 2):
		# Ask the user for input
		selection = input('Please choose a number from above: ')

		# Check to see if the user wan't to run the application
		if selection.isdigit() and int(selection) == 1:
			# Call the function that is used to handle running the parser
			run_script()

			# Break to exit
			break
		elif selection.isdigit() and int(selection) == 2:
			# Break to exit
			break
		else:
			# Display an error
			print('Invalid Input. Please try again')
			print('')

			# Update the section pointer
			selection = ''

# The following function is used to handle parsing the subtitles file
def run_script():
	# Ask the user to input the path to the desired file
	path = input('Please enter the path the the subtitles file: ')

	# Check to see if the file exists
	if not os.path.exists(path):
		# Display an error
		print('Path to file doesn\'t exist. Please try again.')

		# Ask again and return
		run_script()
		return

	# Create the required variables
	lines = {}
	caught_lines = {}
	index = 1

	# Open the file pointer to parse the file for the required lines
	with open(path, 'r') as file:

		# Grab the lines from the file
		lines = file.readlines()
		caught_lines = [sentence for sentence in lines if re.search(r'[A-Z]{2,}', sentence)]

	# Open the subtitles file again for modification
	with open(path, 'w') as file:
		# Iterate over each of the formatted lines
		for line in lines:
			# Grab the required variables
			line_number = lines.index(line)
			sentence = line

			# Check to see if the following sentence is in the caught list
			if line in caught_lines:
				print('{} of {}'.format(str(index), len(caught_lines)))
				print('')
				print(str(line_number - 2) + '    ' + lines[line_number - 2].replace('\n', ''))
				print(str(line_number - 1) + '    ' + lines[line_number - 1].replace('\n', ''))
				print('-'*10 + ' The following sentence ' + '-'*10)
				print(str(line_number) + '    ' + sentence.replace('\n', ''))
				print('-'*44)
				print(str(line_number + 1) + '    ' + lines[line_number + 1].replace('\n', ''))
				print(str(line_number + 2) + '    ' + lines[line_number + 2].replace('\n', ''))
				print('')

				# Increment the index
				index = index + 1

				# Ask the user if they'd like to remove the following line
				if input('Would you like to remove the above mentioned line? (y/N): ').lower() != 'y':
					# Print the line back to the file
					file.write(line)
			else:
				# Print the line back to the file
				file.write(line)

	# Display that the operation is complete
	print('')
	print('Finished!!')

# Call the main menu
menu()