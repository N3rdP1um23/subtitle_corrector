# Import the required packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
import os
from tkinter.constants import END, LEFT, NW, RAISED, SW, TOP, X
import re

# The following is a class that's used for setting up the application GUI
class assister_application:
    # Create the class specific properties
    operations = [
        'Remove uppercase words',
        'Add space after line starting dash',
    ]
    supported_files = (
        ('MicroDVD/VobSub Subtitle File', '*.sub'),
        ('SubRip File', '*.srt'),
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
        frame = tk.Frame(self.window, bg = 'white', height = 100, pady = 25, padx = 20)

        # Append the header heading and subheadding
        tk.Label(frame, text ='Subtitle Assister', font = 'Helvetica 12 bold', bg = 'white').pack(anchor = NW)
        tk.Label(frame, text = 'Your helping hand when modifying and correcting subtitles!', font = 'Helvetica 12', bg = 'white').pack(anchor = SW)

        # Pack the frame onto the window
        frame.pack(side = TOP, fill = X)

        # # Add the separator for visual separation
        ttk.Separator(self.window, orient = 'horizontal').pack(side = TOP, fill = X)

    # The following function is used to setup the queue side of the display
    def setup_queue(self):
        # Add the file open button label
        tk.Label(self.window, text = 'Open Files', font = 'Helvetica 12 bold').pack(side = LEFT)

        # Add the file open button
        tk.Button(self.window, text = 'Open File(s)', command = self.gather_subtitle_file, width = 25).place(x = 10, y = 150)

        # Add the operation label
        tk.Label(self.window, text = 'Operation', font = 'Helvetica 12 bold').place(x = 10, y = 185)

        # Grab the default option for the dropdown
        self.selected_operation = tk.StringVar(self.window, self.operations[0])

        # Add the dropdown with the available operations
        self.drpOperation = ttk.OptionMenu(self.window, self.selected_operation, self.operations[0], *self.operations)
        self.drpOperation.config(width = 25)
        self.drpOperation.place(x = 10, y = 215)

        # Add the queue label
        tk.Label(self.window, text = 'Queue', font = 'Helvetica 12 bold').place(x = 10, y = 245)

        # Add the queue list
        self.lbxQueue = tk.Listbox(self.window, width = 30, height = 36)
        self.lbxQueue.place(x = 10, y = 275)

        # Add the start and clear buttons
        tk.Button(self.window, text = 'Start', command = self.start_operation, width = 25).place(x = 10, y = 865)
        tk.Button(self.window, text = 'Clear', command = self.clear_application, width = 25).place(x = 10, y = 900)

        # Add the queue label
        tk.Label(self.window, text = 'Progress', font = 'Helvetica 12 bold').place(x = 10, y = 940)

        # Add the overall queue progress bar
        self.pgbQueue = ttk.Progressbar(self.window, orient = 'horizontal', length = 190, mode = 'determinate')
        self.pgbQueue.place(x = 10, y = 970)

        # Add the queue separator
        ttk.Separator(self.window, orient = 'vertical').place(x = 210, y = 100, relheight = 1)

    # The following function is used to handle setting up the viewer and old new sections
    def setup_viewer(self):
        # Add the file viewer label
        tk.Label(self.window, text = 'File Viewer', font = 'Helvetica 12 bold').place(x = 220, y = 120)

        # Create the main input area
        self.txtFileViewer = tk.Text(self.window, wrap = 'none', state = 'disabled')
        self.vsbFileViewer = ttk.Scrollbar(self.window, command = self.txtFileViewer.yview, orient = 'vertical')
        self.hsbFileViewer = ttk.Scrollbar(self.window, command = self.txtFileViewer.xview, orient = 'horizontal')
        self.txtFileViewer.configure(yscrollcommand = self.vsbFileViewer.set, xscrollcommand = self.hsbFileViewer.set)

        # Place the file viewer on the page
        self.txtFileViewer.place(x = 220, y = 150, relwidth = 0.875, relheight = 0.5)
        self.vsbFileViewer.place(x = 1900, y = 150, relheight = 0.5)
        self.hsbFileViewer.place(x = 220, y = 659, relwidth = 0.875)

        # Add the color tags
        self.txtFileViewer.tag_configure('highlight', background="#ffff99")

        # Add the old vs new section separator
        ttk.Separator(self.window, orient = 'horizontal').place(x = 220, y = 690, relwidth = 1)

        # Add the old section label
        tk.Label(self.window, text = 'Old', font = 'Helvetica 12 bold').place(x = 220, y = 700)

        # Add the old viewer section
        self.txtOldSection = tk.Text(self.window, wrap = 'none', state = 'disabled')
        self.txtOldSection.place(x = 220, y = 730, relwidth = 0.45, height = 170)

        # Add the new section label
        tk.Label(self.window, text = 'New', font = 'Helvetica 12 bold').place(x = 1100, y = 700)

        # Add the new viewer section
        self.txtNewSection = tk.Text(self.window, wrap = 'none', state = 'disabled')
        self.txtNewSection.place(x = 1100, y = 730, relwidth = 0.42, height = 170)

        # Add the action area separator
        ttk.Separator(self.window, orient = 'horizontal').place(x = 220, y = 925, relwidth = 1)

        # Add the action buttons to the view
        self.btnEdit = tk.Button(self.window, text = 'Edit', command = self.edit_new_section, width = 15, height = 2, bg = '#4464AD', fg = 'white', font = 'Helvetica 9 bold')
        self.btnEdit.configure(state = 'disabled')
        self.btnEdit.place(x = 1560, y = 950)
        self.btnSkip = tk.Button(self.window, text = 'Skip', command = self.skip_section, width = 15, height = 2, bg = '#FE4A49', fg = 'white', font = 'Helvetica 9 bold')
        self.btnSkip.configure(state = 'disabled')
        self.btnSkip.place(x = 1680, y = 950)
        self.btnApprove = tk.Button(self.window, text = 'Approve', command = self.approve_section, width = 15, height = 2, bg = '#6DA34D', fg = 'white', font = 'Helvetica 9 bold')
        self.btnApprove.configure(state = 'disabled')
        self.btnApprove.place(x = 1800, y = 950)

        # Add the section that shows the matches and current index
        tk.Label(self.window, text = 'Current Match: ', font = 'Helvetica 12 bold').place(x = 220, y = 950)
        self.lblCurrentMatch = tk.Label(self.window, text = str(self.current_index), font = 'Helvetica 12')
        self.lblCurrentMatch.place(x = 350, y = 950)
        tk.Label(self.window, text = 'Total Matches: ', font = 'Helvetica 12 bold').place(x = 220, y = 980)
        self.lblTotalMatched = tk.Label(self.window, text = str(self.total_items), font = 'Helvetica 12')
        self.lblTotalMatched.place(x = 350, y = 980)

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
            self.drpOperation.configure(state = 'disabled')

            # Enable the view buttons
            self.btnEdit.configure(state = 'normal')
            self.btnSkip.configure(state = 'normal')
            self.btnApprove.configure(state = 'normal')

            # Call the function that's used to handle changing the current file pointer
            self.change_file()

    # The following function is used to handle clearing the application
    def clear_application(self):
        # Clear the queue, selected files, inputs, and reset states
        self.lbxQueue.selection_clear(0, END)
        self.lbxQueue.delete(0, END)
        self.selected_files = []
        self.drpOperation.configure(state = 'normal')
        self.current_file_index = -1

        # Call the function that's used for clearing the file viewer items
        self.clear_file_viewer()

        # Disable the view buttons again
        self.btnEdit.configure(state = 'disabled')
        self.btnSkip.configure(state = 'disabled')
        self.btnApprove.configure(state = 'disabled')

        # Reset the progress bar
        self.pgbQueue['value'] = 0

    # The foloowing function is used to handle clearing the file viewer items
    def clear_file_viewer(self):
        # Clear file viewer items
        self.txtFileViewer.configure(state = 'normal')
        self.txtFileViewer.delete(1.0, END)
        self.txtFileViewer.configure(state = 'disabled')
        self.txtOldSection.configure(state = 'normal')
        self.txtOldSection.delete(1.0, END)
        self.txtOldSection.configure(state = 'disabled')
        self.txtNewSection.configure(state = 'normal')
        self.txtNewSection.delete(1.0, END)
        self.txtNewSection.configure(state = 'disabled')
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

    # The following function is used to handle approving the current section
    def approve_section(self):
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

        # Correct the new section text area to not be editable
        self.edit_new_section(disabled = True)

        # Call the function to handle setting up the data on the screen
        self.setup_data()

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
            self.clear_application()

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
            # Load the file contents
            with open(file, 'r', encoding = 'utf-8-sig') as file:
                # Create a dictionary that holds the line number and line number
                line_numbers = dict((line_text.split('\n')[0], line_number) for line_number, line_text in enumerate(file, 1) if line_text.split('\n')[0].isnumeric())

                # Seek back to the start of the file
                file.seek(0)

                # Grab the file content
                file_content = file.read()

                # Split the data into a list
                self.file_data = file_content.split('\n\n') # Split the file based on any double new lines
                self.file_data = [x for x in self.file_data if x != '\n' and x != '\n\n'] # Filter out any remaining new lines or double new lines
                self.file_data = list(filter(None, self.file_data)) # Filter out any empty stings
                self.file_data = [{'index': section.split('\n')[0], 'time': section.split('\n')[1], 'text': section.split('\n')[2:], 'line_number': line_numbers[section.split('\n')[0]]} for section in self.file_data]

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
        if current_operation == 'Remove uppercase words':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(line.isupper() for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)
        elif current_operation == 'Add space after line starting dash':
            # Iterrate over each of the sections in the file
            for section in self.file_data:
                # Check to see if there's a line that needs handling
                if any(re.match(r'\-\S', line) for line in section['text']):
                    # Append the section to the list that will hold the sections that need correcting
                    sections_to_modify.append(section)

        # Update the total matched label with the amount of sections to process
        self.total_items = len(sections_to_modify)
        self.lblTotalMatched['text'] = str(self.total_items)

        # Set the sections to be modified to the class
        self.sections_to_modify = sections_to_modify

    # The following function is used to handle setting up the data to have changes confirmed and modified if needed
    def setup_data(self):
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

        # Grab the text from the current pointer
        text = current_data['text'].copy()

        # Iterate over the lines and correct the ones with the issue
        for index, line in enumerate(current_data['text']):
            # Check to see if the user is removing uppercase sentances
            if current_operation == 'Remove uppercase words':
                # Check to see if the current line is the one that matches
                if line.isupper():
                    # Zero out the line
                    current_data['text'][index] = ''
            elif True:
                # Check to see if the current line is the one that matches
                if re.search(r'^\-\S', line):
                    # Correct the dash with no space
                    current_data['text'][index] = '- ' + current_data['text'][index][1:]

        # Load the modified section into the new viewer
        self.txtNewSection.configure(state = 'normal')
        self.txtNewSection.delete(1.0, END)
        self.txtNewSection.insert(END, current_data['index'] + '\n' + current_data['time'] + '\n' + '\n'.join(current_data['text']))
        self.txtNewSection.configure(state = 'disabled')

        # Update the current pointer and reset the text entry
        current_data['text'] = text

    # The following function is used to handle saving the modifications to file
    def save_modifications(self):
        # Open the file in question and save the modifications
        with open(self.selected_files[self.current_file_index], 'w', encoding = 'utf-8') as file:
            # Create a list holding modified file sections
            modified_sections = []

            # Iterate over the file data
            for section in self.file_data:
                # Append the data to the modified section
                modified_sections.append(section['index'] + '\n' + section['time'] + '\n' + '\n'.join(section['text']))

            # Write the modified sections to the file
            file.write('\n\n'.join(modified_sections).encode('utf-8', 'ignore').decode('utf-8'))

# Call the main
assister_application().display()