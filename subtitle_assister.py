###
#
# N3rdP1um23
# The following file is used to handle modifying and manipulating subtitle files with various actions
#
###

# Import the required packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
from tkinter.constants import BOTH, BOTTOM, DISABLED, END, HORIZONTAL, LEFT, NONE, NORMAL, NW, RIGHT, SW, TOP, VERTICAL, W, X, Y
import regex

# The following is a class that's used for setting up the application GUI
class assister_application:
    # Create the class specific properties
    operations = [
        'Remove full uppercase lines',
        'Remove lines with two or more consecutive uppercase characters',
        'Remove line ending dash',
        'Remove space after three dots and a lowercase word',
        'Remove space after three dots and an uppercase word',
        'Remove space after three dots',
        'Edit full uppercase lines',
        'Edit lines with two or more consecutive uppercase characters',
        'Add space after line starting dash',
        'Add space after line starting dash and lowercase character',
        'Add space after line starting dash and uppercase character',
        'Capitalize, add a period, and space people abbreviations',
        'Sanitize file',
        'Convert vtt to srt',
        'Trim long lines'
    ]
    supported_files = (
        ('SubRip File', '*.srt'),
        ('MicroDVD/VobSub Subtitle File', '*.sub'),
        ('Sub Station Alpha Subtitle File', '*.ssa'),
        ('Text File', '*.txt'),
        ('Web Video Text Tracks File', '*.vtt'),
        ('YouTube Captions File', '*.sbv'),
        ('Any File', '*.*')
    )
    current_file_index = -1
    current_index = 0
    total_items = 0
    sections_to_modify = []

    # The following function is used as a constructor
    def __init__(self):
        # Initialize the various parts of the application
        self.setup_window()
        self.setup_header()
        self.setup_queue()
        self.setup_viewer()

    # The following function is used to handle displaying the actual application
    def display(self):
        # Run the application
        self.window.mainloop()

    ###
    #
    # View setup functions
    #
    ###

    # The following function is used to setup the application window
    def setup_window(self):
        # Initialize the required variables
        self.window = tk.Tk()

        # Set the window specific values
        self.window.title('Subtitle Assister')
        self.window.state('zoomed')

    # The following function is used to handle setting up the application header
    def setup_header(self):
        # Create the top frame that holds the application information
        frame = tk.Frame(self.window, bg = 'white', height = 100, pady = 25, padx = 10)

        # Append the header heading and subheadding
        tk.Label(frame, text ='Subtitle Assister', font = 'Helvetica 12 bold', bg = 'white').pack(anchor = NW)
        tk.Label(frame, text = 'Your helping hand when modifying and correcting subtitles!', font = 'Helvetica 12', bg = 'white').pack(anchor = SW)

        # Pack the frame onto the window
        frame.pack(side = TOP, fill = X)

        # Add the separator for visual separation
        ttk.Separator(self.window, orient = HORIZONTAL).pack(side = TOP, fill = X)

    # The following function is used to setup the queue side of the display
    def setup_queue(self):
        # Create the top frame that holds the queue section
        frame = tk.Frame(self.window, pady = 25, padx = 10)

        # Add the file open button label
        tk.Label(frame, text = 'Open Files', font = 'Helvetica 12 bold').pack(anchor = W)

        # Add the file open button
        tk.Button(frame, text = 'Open File(s)', command = self.gather_subtitle_file).pack(pady = 5, fill = X)

        # Add the operation label
        tk.Label(frame, text = 'Operation', font = 'Helvetica 12 bold').pack(anchor = W, pady = 5)

        # Sort the list of operations
        self.operations.sort()

        # Grab the default option for the dropdown
        self.selected_operation = tk.StringVar(frame, self.operations[0])

        # Add the dropdown with the available operations
        self.drpOperation = ttk.OptionMenu(frame, self.selected_operation, self.operations[0], *self.operations)
        self.drpOperation.pack(pady = 5, fill = X)

        # Add the queue label
        tk.Label(frame, text = 'Queue', font = 'Helvetica 12 bold').pack(anchor = W, pady = 5)

        # Add the queue list
        self.lbxQueue = tk.Listbox(frame)
        self.lbxQueue.pack(fill = BOTH, expand = True)

        # Add the start and clear buttons
        tk.Button(frame, text = 'Start', command = self.start_operation).pack(pady = 5, fill = X)
        tk.Button(frame, text = 'Clear', command = self.clear_application).pack(pady = 5, fill = X)

        # Add the queue label
        tk.Label(frame, text = 'Progress', font = 'Helvetica 12 bold').pack(anchor = W, pady = 5)

        # Add the overall queue progress bar
        self.pgbQueue = ttk.Progressbar(frame, orient = HORIZONTAL, mode = 'determinate')
        self.pgbQueue.pack(fill = X)

        # Pack the frame onto the window
        frame.pack(side = LEFT, fill = BOTH)

        # Add the queue separator
        ttk.Separator(self.window, orient = VERTICAL).pack(side = LEFT, fill = Y)

    # The following function is used to handle setting up the viewer and old new sections
    def setup_viewer(self):
        # Create the top frame that holds the queue section
        frame = tk.Frame(self.window, pady = 25, padx = 10)

        # Add the file viewer label
        tk.Label(frame, text = 'File Viewer', font = 'Helvetica 12 bold').pack(anchor = W)

        # Create the frame to hold the file viewer and also vertical scroll bar
        main_view_frame = tk.Frame(frame)

        # Create the main input area
        self.txtFileViewer = tk.Text(main_view_frame, wrap = NONE, state = DISABLED)
        self.vsbFileViewer = ttk.Scrollbar(main_view_frame, command = self.txtFileViewer.yview, orient = VERTICAL)
        self.hsbFileViewer = ttk.Scrollbar(frame, command = self.txtFileViewer.xview, orient = HORIZONTAL)
        self.txtFileViewer.configure(yscrollcommand = self.vsbFileViewer.set, xscrollcommand = self.hsbFileViewer.set)

        # Place the file viewer on the page
        self.txtFileViewer.pack(side = LEFT, fill = BOTH, expand = True)
        self.vsbFileViewer.pack(side = RIGHT, fill = Y)

        # Pack the main_view_frame onto the frame
        main_view_frame.pack(fill = BOTH, expand = True)

        # Place the horizontal scroll bar
        self.hsbFileViewer.pack(fill = X)

        # Add the color tags
        self.txtFileViewer.tag_configure('highlight', background = "#ffff99")

        # Add the old vs new section separator
        ttk.Separator(frame, orient = HORIZONTAL).pack(fill = X, pady = 10)

        # Create the frame to hold the oldand new viewer
        old_new_view_frame = tk.Frame(frame)

        # Create the frame to hold the old viewer
        old_view_frame = tk.Frame(old_new_view_frame)

        # Add the old section label
        tk.Label(old_view_frame, text = 'Old', font = 'Helvetica 12 bold').pack(anchor = W)

        # Add the old viewer section
        self.txtOldSection = tk.Text(old_view_frame, wrap = NONE, state = DISABLED, height = 10)
        self.txtOldSection.pack(fill = X)

        # Pack the old_view_frame onto the old_new_view_frame
        old_view_frame.pack(side = LEFT, expand = True, fill = BOTH)

        # Create the frame to hold the old viewer
        new_view_frame = tk.Frame(old_new_view_frame, padx = 5)

        # Add the new section label
        tk.Label(new_view_frame, text = 'New', font = 'Helvetica 12 bold').pack(anchor = W)

        # Add the new viewer section
        self.txtNewSection = tk.Text(new_view_frame, wrap = NONE, state = DISABLED, height = 10)
        self.txtNewSection.pack(fill = X)

        # Pack the new_view_frame onto the old_new_view_frame
        new_view_frame.pack(side = LEFT, expand = True, fill = BOTH)

        # Pack the old_new_view_frame onto te frame
        old_new_view_frame.pack(fill = X)

        # Add the action area separator
        ttk.Separator(frame, orient = HORIZONTAL).pack(fill = X, pady = 10)

        pointer_frame = tk.Frame(frame)

        # Create a frame that holds the current pointer
        current_frame = tk.Frame(pointer_frame, pady = 5)

        # Add the section that shows the matches and current index
        tk.Label(current_frame, text = 'Current Match: ', font = 'Helvetica 12 bold').pack(side = LEFT)
        self.lblCurrentMatch = tk.Label(current_frame, text = str(self.current_index), font = 'Helvetica 12')
        self.lblCurrentMatch.pack(side = RIGHT)

        # Place the current pointer
        current_frame.pack(side = TOP, fill = X)

        # Create a frame that holds the current pointer
        total_frame = tk.Frame(pointer_frame)

        # Add the section that shows the matches and current index
        tk.Label(total_frame, text = 'Total Matches: ', font = 'Helvetica 12 bold').pack(side = LEFT)
        self.lblTotalMatched = tk.Label(total_frame, text = str(self.current_index), font = 'Helvetica 12')
        self.lblTotalMatched.pack(side = RIGHT)

        # Place the total pointer
        total_frame.pack(side = BOTTOM, fill = X)

        # Place the pointer frame
        pointer_frame.pack(side = LEFT)

        # Add the action buttons to the view
        self.btnApprove = tk.Button(frame, text = 'Approve', command = self.approve_section, width = 15, height = 2, font = 'Helvetica 9 bold') # , bg = '#6DA34D', fg = 'white',
        self.btnApprove.configure(state = DISABLED)
        self.btnApprove.pack(side = RIGHT)
        self.btnSkip = tk.Button(frame, text = 'Skip', command = self.skip_section, width = 15, height = 2, font = 'Helvetica 9 bold') # , bg = '#FE4A49', fg = 'white'
        self.btnSkip.configure(state = DISABLED)
        self.btnSkip.pack(side = RIGHT, padx = 5)
        self.btnEdit = tk.Button(frame, text = 'Edit', command = self.edit_new_section, width = 15, height = 2, font = 'Helvetica 9 bold') # , bg = '#4464AD', fg = 'white'
        self.btnEdit.configure(state = DISABLED)
        self.btnEdit.pack(side = RIGHT)
        self.btnApproveAll = tk.Button(frame, text = 'Approve All', command = self.approve_all_sections, width = 15, height = 2, font = 'Helvetica 9 bold') # , bg = '#FE4A49', fg = 'white'
        self.btnApproveAll.configure(state = DISABLED)
        self.btnApproveAll.pack(side = RIGHT, padx = 5)
        self.btnSkipAll = tk.Button(frame, text = 'Skip All', command = self.skip_all_sections, width = 15, height = 2, font = 'Helvetica 9 bold') # , bg = '#FE4A49', fg = 'white'
        self.btnSkipAll.configure(state = DISABLED)
        self.btnSkipAll.pack(side = RIGHT)
        self.btnSaveSanitization = tk.Button(frame, text = 'Save Sanitization', command = self.save_sanitization, width = 15, height = 2, font = 'Helvetica 9 bold') # , bg = '#FE4A49', fg = 'white'
        self.btnSaveSanitization.configure(state = DISABLED)
        self.btnSaveSanitization.pack(side = RIGHT, padx = 5)

        # Pack the frame onto the window
        frame.pack(side = LEFT, fill = BOTH, expand = True)

    ###
    #
    # Action functions
    #
    ###

    # The following function is used to handle gathering the files to add to the queue
    def gather_subtitle_file(self):
        # Ask the user to select a file(s)
        self.selected_files = fd.askopenfilenames(title = 'Open Subtitle File(s)', initialdir = '/', filetypes = self.supported_files)

        # Iterare over the selected files and append them to the queue
        for file_name in self.selected_files:
            # Append the file name to the queue list
            self.lbxQueue.insert((self.selected_files.index(file_name) + 1), os.path.basename(file_name))

    # The following operation is used to handle starting the operation on the queue
    def start_operation(self):
        # Check to see if there are item to process
        if self.lbxQueue.size() == 0:
            # Display a notice that there aren't any items to process currently
            mb.showerror(title = 'Queue Empty', message = 'Please add files to the queue before starting.')
        else:
            # Disable the operations dropdown
            self.drpOperation.configure(state = DISABLED)

            # Enable the view buttons
            self.btnEdit.configure(state = NORMAL)
            self.btnSkip.configure(state = NORMAL)
            self.btnSkipAll.configure(state = NORMAL)
            self.btnApprove.configure(state = NORMAL)
            self.btnApproveAll.configure(state = NORMAL)

            # Check if performing the sanitization operation
            if self.selected_operation.get() == 'Sanitize file':
                # Enable the save sanitization button
                self.btnSaveSanitization.configure(state = NORMAL)

            # Call the function that's used to handle changing the current file pointer
            self.change_file()

    # The following function is used to handle clearing the application
    def clear_application(self, clear_queue = True):
        # Check to see if the user would like to clear the queue also
        if clear_queue:
            self.lbxQueue.selection_clear(0, END)
            self.lbxQueue.delete(0, END)
            self.selected_files = []

        # Clear the queue, selected files, inputs, and reset states
        self.drpOperation.configure(state = NORMAL)
        self.current_file_index = -1

        # Call the function that's used for clearing the file viewer items
        self.clear_file_viewer()

        # Disable the view buttons again
        self.btnEdit.configure(state = DISABLED)
        self.btnSkip.configure(state = DISABLED)
        self.btnSkipAll.configure(state = DISABLED)
        self.btnApprove.configure(state = DISABLED)
        self.btnApproveAll.configure(state = DISABLED)
        self.btnSaveSanitization.configure(state = DISABLED)

        # Reset the progress bar
        self.pgbQueue['value'] = 0

    # The foloowing function is used to handle clearing the file viewer items
    def clear_file_viewer(self):
        # Clear file viewer items
        self.txtFileViewer.configure(state = NORMAL)
        self.txtFileViewer.delete(1.0, END)
        self.txtFileViewer.configure(state = DISABLED)
        self.txtOldSection.configure(state = NORMAL)
        self.txtOldSection.delete(1.0, END)
        self.txtOldSection.configure(state = DISABLED)
        self.txtNewSection.configure(state = NORMAL)
        self.txtNewSection.delete(1.0, END)
        self.txtNewSection.configure(state = DISABLED)
        self.current_index = 0
        self.total_items = 0
        self.lblCurrentMatch['text'] = str(self.current_index)
        self.lblTotalMatched['text'] = str(self.total_items)
        self.sections_to_modify = []
        self.file_data = []

    # The following function is used to handle opening the new section for editing
    def edit_new_section(self, disabled = False):
        # Allow the new section to be editable
        self.txtNewSection.configure(state = ('normal' if disabled == False else 'disabled'))

        # Check to see if the function isn't going to disable the text area
        if disabled == False:
            # Set focus to input
            self.txtNewSection.focus_set()

    # The following function is used to handle skipping the current section
    def skip_section(self):
        # Call the function to handle setting up the data on the screen
        self.setup_data()

    # The following function is used to handle skipping all sections
    def skip_all_sections(self):
        # Update the current index to dynamically pass all sections of the current file
        self.current_index = len(self.sections_to_modify)

        # Call the function to handle setting up the data on the screen
        self.setup_data()

    # The following function is used to handle approving the current section
    def approve_section(self, approve_all = False):
        # Grab the current modifications
        current_modifications = self.txtNewSection.get('1.0', END)
        current_modifications = current_modifications.split('\n')
        current_modifications = [x for x in current_modifications if x != '\n' and x != '\n\n']
        current_modifications = list(filter(None, current_modifications))
        current_modifications = {'index': current_modifications[0], 'time': current_modifications[1], 'text': current_modifications[2:]}

        # Grab the current file_data index and update the text section with the new edits
        current_line_index = self.sections_to_modify[self.current_index - 1]['index']
        current_section = [section for section in self.file_data if section['index'] == current_line_index][0]
        current_section['text'] = current_modifications['text']

        # Check to see if the section ends up blank
        if len(current_section['text']) == 0:
            # Remove the current section
            self.file_data = [section for section in self.file_data if section['index'] != current_line_index]

        # Correct the new section text area to not be editable
        self.edit_new_section(disabled = True)

        # Call the function to handle setting up the data on the screen
        self.setup_data(approve_all = approve_all)

    # The following function is used to handle approving all sections
    def approve_all_sections(self):
        # Call the function to handle approving the current section - and passalong that the user wan't to approve all sections
        self.approve_section(approve_all = True)

    # The following function is used to handle approving all sections
    def save_sanitization(self):
        # Call the function to handle saving the modifications to the file
        self.save_modifications()

        # Call the function that's used to handle changing to the next file
        self.change_file()

    ###
    #
    # Logic/Processing functions
    #
    ###

    # The following function is used to handle changing the current file that's being modified
    def change_file(self):
        # Update the file index pointer
        self.current_file_index = self.current_file_index + 1

        # Check to see if all files have been modified
        if self.current_file_index >= len(self.selected_files):
            # Update the current progress to be 100%
            self.pgbQueue['value'] = 100

            # Display a notice to the user
            mb.showinfo(title = 'Queue Complete', message = 'Operation complete successfully!')

            # Call the function to handle clearing the application
            self.clear_application(clear_queue = False)

            # Return to stop further processing
            return

        # Check to see if the current index isn't 0
        if self.current_file_index != 0:
            # Update the progressbar with the current status
            self.pgbQueue['value'] = abs((self.current_file_index / self.lbxQueue.size()) * 100)

        # Select the respective item in the queue
        self.lbxQueue.selection_clear(0, END)
        self.lbxQueue.selection_set(self.current_file_index)

        # Call the function that's used for clearing the file viewer items
        self.clear_file_viewer()

        # Start a new thread to handle user interacting with the modification of the application
        self.modify_file(self.selected_files[self.current_file_index])

    # The following function is used to handle operating & loading the data into the sections and getting user input
    def modify_file(self, file):
        # Call the function to handle loading the data from the file
        if self.load_data(file) == False:
            # Call the function to change to the next file
            self.change_file()

            # Return to stop further processing
            return

        # Call the function to handle checking if the file has any sections to edit based on the operation
        self.parse_file()

        # Call the function that is used to handle setting up the data for confirmation and modification
        self.setup_data()

    # The following function is used to handle loading the data from the file
    def load_data(self, file):
        # Check to see if the file exists
        if not os.path.exists(file):
            # Display an error message
            mb.showerror(title = 'File Missing', message = os.path.basename(file) + ' is missing. Skipping.')

            # Return False as the file wasn't found
            return False
        else:
            # Grab the current operation the user would like to perform
            current_operation = self.selected_operation.get()

            # Load the file contents
            with open(file, 'r', encoding = 'utf-8-sig') as file:
                # Create a dictionary that holds the line number and line number
                line_numbers = dict((line_text.split('\n')[0], line_number) for line_number, line_text in enumerate(file, 1) if line_text.split('\n')[0].isnumeric())

                # Seek back to the start of the file
                file.seek(0)

                # Check to see if converting a vtt to srt file
                if current_operation == 'Convert vtt to srt':
                    # Skip the first three lines of the file as they're header information
                    file.seek(sum([len(line) for line in file.readlines()[0:3]]))

                # Grab the file content
                file_content = file.read()

                # Split the data into a list
                self.file_data = file_content.split('\n\n') # Split the file based on any double new lines
                self.file_data = [x for x in self.file_data if x != '\n' and x != '\n\n'] # Filter out any remaining new lines or double new lines
                self.file_data = list(filter(None, self.file_data)) # Filter out any empty stings
                self.file_data = [x for x in self.file_data if len(list(filter(None, x.split('\n')))) >= 3] # Filter out any lines that have no text
                has_index = list(filter(None, self.file_data[0].split('\n')))[0].isnumeric()
                index = 0
                self.file_data = [{'index': list(filter(None, section.split('\n')))[0] if has_index else str(index := index + 1), 'time': list(filter(None, section.split('\n')))[1 if has_index else 0], 'text': list(filter(None, section.split('\n')))[2:] if has_index else list(filter(None, section.split('\n')))[1:], 'line_number': line_numbers[list(filter(None, section.split('\n')))[0]] if has_index else index} for section in self.file_data]

                # Load the main data into the file viewer
                self.txtFileViewer.configure(state = 'normal')
                self.txtFileViewer.delete(1.0, END)
                self.txtFileViewer.insert(END, file_content)
                self.txtFileViewer.configure(state = 'disabled')

    # The following function is used to handle parsing the respective file
    def parse_file(self):
        # Grab the current operation the user would like to perform
        current_operation = self.selected_operation.get()

        # Create a variable that will handle storing sections that need modifying
        sections_to_modify = []

        # Check to see if the user is removing uppercase sentances
        if current_operation == 'Remove full uppercase lines':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(line.isupper() for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Remove lines with two or more consecutive uppercase characters':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'[[:upper:]]{2,}', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Edit full uppercase lines':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(line.isupper() for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Edit lines with two or more consecutive uppercase characters':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'[[:upper:]]{2,}', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Add space after line starting dash':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'^(\-\w|\<i\>\-\w|\-\<i\>\w)', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Add space after line starting dash and lowercase character':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'^(\-[[:lower:]]|\<i\>\-[[:lower:]]|\-\<i\>[[:lower:]])', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Add space after line starting dash and uppercase character':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'^(\-[[:upper:]]|\<i\>\-[[:upper:]]|\-\<i\>[[:upper:]])', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Capitalize, add a period, and space people abbreviations':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'(?:^|\ |\/)(dr(?:\ |\.|\.\ )|Dr(?:\ |\.)|jr(?:\ |\.|\.\ )|Jr(?:\ |\.)|mr(?:\ |\.|\.\ )|Mr(?:\ |\.)|mrs(?:\ |\.|\.\ )|Mrs(?:\ |\.)|ms(?:\ |\.|\.\ )|Ms(?:\ |\.)|sr(?:\ |\.|\.\ )|Sr(?:\ |\.)|st(?:\ |\.|\.\ )|St(?:\ |\.))[[:upper:]]', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Remove line ending dash':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(line.endswith('-') for line in section['text'] if line == section['text'][-1]):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Remove space after three dots and a lowercase word':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'\.\.\.\ [[:lower:]]', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Remove space after three dots and an uppercase word':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'\.\.\.\ [[:upper:]]', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Remove space after three dots':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(regex.search(r'\.\.\.\ ', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Sanitize file':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Append the section as it needs modification
                sections_to_modify.append(section)
        elif current_operation == 'Trim long lines':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(len(line) > 40 for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Convert vtt to srt':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Append the section to the list that will hold the sections that need correcting
                sections_to_modify.append(section)

        # Update the total matched label with the amount of sections to process
        self.total_items = len(sections_to_modify)
        self.lblTotalMatched['text'] = str(self.total_items)

        # Set the sections to be modified to the class
        self.sections_to_modify = sections_to_modify

    # The following function is used to handle setting up the data to have changes confirmed and modified if needed
    def setup_data(self, approve_all = False):
        # Check to see if the file has been fully modified
        if self.current_index >= len(self.sections_to_modify):
            # Call the function to handle saving the modifications to the file
            self.save_modifications()

            # Call the function that's used to handle changing to the next file
            self.change_file()

            # Return to stop further processing
            return

        # Grab the current data to handle
        current_data = self.sections_to_modify[self.current_index]

        # Call the function to handle highlighting the text and scrolling to it if need be
        self.highlight_and_view(current_data['line_number'], (current_data['line_number'] + (len(current_data) - 2) + len(current_data['text'])))

        # Remove the line_number from the data array
        current_data.pop('line_number')

        # Update the current_data's text to be joined
        current_data['text'] = '\n'.join(current_data['text'])

        # Load the section into the old viewer
        self.txtOldSection.configure(state = 'normal')
        self.txtOldSection.delete(1.0, END)
        self.txtOldSection.insert(END, '\n'.join(current_data.values()))
        self.txtOldSection.configure(state = 'disabled')

        # Update the current_data's text to be in a list again
        current_data['text'] = current_data['text'].split('\n')

        # Call the function that handles modifying the data and displays it in view
        self.modify_section(current_data)

        # Update current match pointer and label
        self.current_index = self.current_index + 1
        self.lblCurrentMatch['text'] = str(self.current_index)

        # Check to see if use has approved all sections
        if approve_all == True:
            # Call the fucntion to approve the section
            self.approve_section(approve_all = approve_all)

    # The following function is used to handle highlighting text and scrolling to it if it's out of view
    def highlight_and_view(self, line_start, line_end):
        # Highlight the text in question
        self.txtFileViewer.tag_add('highlight', "%s.0" % line_start, "%s.0" % line_end)

        # Scroll to the text in question
        self.txtFileViewer.see(str(line_start) + ".0")
        lineinfo = self.txtFileViewer.dlineinfo(str(line_start) + ".0")
        self.txtFileViewer.yview_scroll(lineinfo[1], 'pixels' )

    # The following function is used to handle modifying the data and displaying it in view
    def modify_section(self, current_data):
        # Grab the current operation the user would like to perform
        current_operation = self.selected_operation.get()

        # Create flags to handle iterating over the text based on the current operation
        first_run = True
        process_further = False

        # Iterate only when it's the first run or further processing is needed
        while first_run or process_further:
            # Update the flags
            first_run = False
            process_further = False

            # Grab the time and text from the current pointer
            time = ('%s' % current_data['time'])
            text = current_data['text'].copy()

            # Check to see if the user is performing a function to handle converting the file from vtt to srt
            if current_operation == 'Convert vtt to srt':
                # Update the time setting
                current_data['time'] = ' '.join(current_data['time'].split(' ', 3)[:-1])

            # Iterate over the lines and correct the ones with the issue
            for index, line in enumerate(current_data['text'].copy()):
                # Check to see if the user is removing uppercase sentances
                if current_operation == 'Remove full uppercase lines':
                    # Check to see if the current line is the one that matches
                    if line.isupper():
                        # Zero out the line
                        current_data['text'].remove(line)
                elif current_operation == 'Remove lines with two or more consecutive uppercase characters':
                    # Check to see if the current line is the one that matches
                    if regex.search(r'[[:upper:]]{2,}', line):
                        # Zero out the line
                        current_data['text'].remove(line)
                elif current_operation in ['Edit full uppercase lines', 'Edit lines with two or more consecutive uppercase characters']:
                    # Skip iteration as no modifications need to be performed
                    continue
                elif current_operation in ['Add space after line starting dash', 'Add space after line starting dash and lowercase character', 'Add space after line starting dash and uppercase character']:
                    # Check to see if the current line is the one that matches
                    if (current_operation == 'Add space after line starting dash' and regex.search(r'^(\-\w|\<i\>\-\w|\-\<i\>\w)', line)) or (current_operation == 'Add space after line starting dash and lowercase character' and regex.search(r'^(\-[[:lower:]]|\<i\>\-[[:lower:]]|\-\<i\>[[:lower:]])', line)) or (current_operation == 'Add space after line starting dash and uppercase character' and regex.search(r'^(\-[[:upper:]]|\<i\>\-[[:upper:]]|\-\<i\>[[:upper:]])', line)):
                        # Check to see if the line contains a text modifier
                        if regex.search(r'\<i\>', line):
                            # Check to see if the line starts with with the text modifier
                            if line.startswith('<i>'):
                                # Correct the dash with no space
                                current_data['text'][index] = '<i>- ' + current_data['text'][index].replace('<i>', '').replace('</i>', '')[1:] + '</i>'
                            else:
                                # Correct the dash with no space
                                current_data['text'][index] = '- <i>' + current_data['text'][index].replace('<i>', '').replace('</i>', '')[1:] + '</i>'
                        else:
                            # Correct the dash with no space
                            current_data['text'][index] = '- ' + current_data['text'][index][1:]
                elif current_operation == 'Capitalize, add a period, and space people abbreviations':
                    # Search the string
                    results = regex.findall(r'(?:^|\ |\/)(dr(?:\ |\.|\.\ )|Dr(?:\ |\.)|jr(?:\ |\.|\.\ )|Jr(?:\ |\.)|mr(?:\ |\.|\.\ )|Mr(?:\ |\.)|mrs(?:\ |\.|\.\ )|Mrs(?:\ |\.)|ms(?:\ |\.|\.\ )|Ms(?:\ |\.)|sr(?:\ |\.|\.\ )|Sr(?:\ |\.)|st(?:\ |\.|\.\ )|St(?:\ |\.))[[:upper:]]', line)

                    # Check to see if the current line is the one that matches
                    if results:
                        # Iterate over the matches
                        for match in results:
                            # Update the match
                            match = ''.join(match)

                            # Update the strings
                            current_data['text'][index] = current_data['text'][index].replace(match, match.strip().title() + ('.' if not match.endswith('.') and not match.endswith('. ') else '') + ' ')
                elif current_operation == 'Remove line ending dash':
                    # Check to see if the current line is the last line in the section and ends with a dash
                    if line == current_data['text'][-1] and line.endswith('-'):
                        # Update the strings
                        current_data['text'][index] = current_data['text'][index][:-1]
                elif current_operation == 'Remove space after three dots and a lowercase word':
                    # Search the string
                    results = regex.findall(r'\.\.\.\ [[:lower:]]', line)

                    # Check to see if the current line is the one that matches
                    if results:
                        # Iterate over the matches
                        for match in results:
                            # Update the strings
                            current_data['text'][index] = current_data['text'][index].replace(match, match.replace(' ', ''))
                elif current_operation == 'Remove space after three dots and an uppercase word':
                    # Search the string
                    results = regex.findall(r'\.\.\.\ [[:upper:]]', line)

                    # Check to see if the current line is the one that matches
                    if results:
                        # Iterate over the matches
                        for match in results:
                            # Update the strings
                            current_data['text'][index] = current_data['text'][index].replace(match, match.replace(' ', ''))
                elif current_operation == 'Remove space after three dots':
                    # Search the string
                    results = regex.findall(r'\.\.\.\ ', line)

                    # Check to see if the current line is the one that matches
                    if results:
                        # Iterate over the matches
                        for match in results:
                            # Update the strings
                            current_data['text'][index] = current_data['text'][index].replace(match, match.replace(' ', ''))
                elif current_operation == 'Sanitize file':
                    # Continue as sanatization is already performed
                    continue
                elif current_operation == 'Trim long lines':
                    # Store the current line in perfet shape
                    current_line = current_data['text'][index]

                    # Double check to make sure the current line is greater than 40 characters
                    if len(current_line) > 40:
                        # Grab the last space instance
                        cut_index = 40 - current_line[:40][::-1].index(' ') - 1

                        # Split the line current line and inser the remaining bak into the array
                        current_data['text'][index] = ''.join(current_line[:cut_index]).strip()
                        current_data['text'].insert((index + 1), ''.join(current_line[cut_index:]).strip())

                        # Update the further processing flag
                        process_further = True

        # Load the modified section into the new viewer
        self.txtNewSection.configure(state = 'normal')
        self.txtNewSection.delete(1.0, END)
        self.txtNewSection.insert(END, current_data['index'] + '\n' + current_data['time'] + '\n' + '\n'.join(current_data['text']))
        self.txtNewSection.configure(state = 'disabled')

        # Update the current pointer and reset the time and text entry
        current_data['time'] = time
        current_data['text'] = text

    # The following function is used to handle saving the modifications to file
    def save_modifications(self):
        # Grab the current operation the user would like to perform
        current_operation = self.selected_operation.get()

        # Create a variable that holds the full file path
        file_path = self.selected_files[self.current_file_index]

        # Check to see if the user desires to convert the file
        if current_operation == 'Convert vtt to srt':
            # Change the file extension
            file_path = file_path.replace('vtt', 'str')

        # Open the file in question and save the modifications
        with open(file_path, 'w', encoding = 'utf-8') as file:
            # Create a list holding modified file sections
            modified_sections = []

            # Iterate over the file data
            for index, section in enumerate(self.file_data, 1):
                # Append the data to the modified section
                modified_sections.append(str(index) + '\n' + section['time'] + '\n' + '\n'.join(section['text']))

            # Write the modified sections to the file
            file.write('\n\n'.join(modified_sections).encode('utf-8', 'ignore').decode('utf-8'))

# Call the main
assister_application().display()