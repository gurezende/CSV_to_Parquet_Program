# Package Imports
import pandas as pd
import pyarrow
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
import os

######### Functions ################

# Function to find the "/" in the file path to separate filename and path
def find(s, ch='/'):
    return [i for i, ltr in enumerate(s) if ltr == ch]

# Function to open the browse window
def browse():
    global filename
    global path
    f = askopenfilename()
    # finding the last "/". After that, it is the file name. Before that character "/", it is the path
    last_sep = find(f)[-1]
    filename = f[last_sep+1:]
    path = f[:last_sep+1]
    lbl_a2["text"] = 'FOLDER SELECTED: ' + path

# Function get the user selected option to convert a single file or a batch
def radio():
    global radio_selected
    radio_selected = v.get()
    print(radio_selected)
    return radio_selected

# Function to convert file when I click the button: CSV to PARQUET
def csv_to_parquet():
    if radio_selected == 1:
        # Load file to Pandas dataframe
        df = pd.read_csv(path + filename)
        # Transform to Parquet File
        df.to_parquet(path + filename[:-3]+ "parquet", engine='pyarrow')
        lbl_c["text"] = 'File successfully converted'
    else:
        # Loop over files and convert them all
        list_files = os.listdir(path)
        list_files = list(filter(lambda f: f.endswith('.csv'), list_files))

        c = 0 #creating counter for the label
        for f in list_files:
            df = pd.read_csv(path + f)
            # Transform to Parquet File
            df.to_parquet(path + f[:-3]+ "parquet", engine='pyarrow')
            lbl_c["text"] = str(c) +' files successfully converted'
            c += 1


# Function to convert file when I click the button: PARQUET to CSV
def parquet_to_csv():
    if radio_selected == 1:
        # Load file to Pandas dataframe
        df = pd.read_parquet(path + filename, engine='pyarrow')
        # Transform to CSV File
        df.to_csv(path + filename[:-7]+ "csv", index=False)
        lbl_c["text"] = 'File successfully converted!'
    else:
        # Loop over files and convert them all
        list_files = os.listdir(path)
        list_files = list(filter(lambda f: f.endswith('.parquet'), list_files))

        c = 1 #creating counter for the label
        for f in list_files:
            # Read file to Pandas dataframe
            df = pd.read_parquet(path + f, engine='pyarrow')
            # Transform to CSV File
            df.to_csv(path + f[:-7]+ "csv", index=False)
            lbl_c["text"] = str(c) +' files successfully converted!'
            c += 1

# Function to close the application
def quit_program():
    window.destroy()

######################################

# Create GUI Window, setting up the size and including the window title
window = tk.Tk()
window.geometry('500x500')
window.title("File Converter CSV <-> PARQUET")


# Creating frames to separate the buttons and texts
# Frame config
frm_config = tk.Frame(master=window,
                      width=400,
                      height=50)

# Label config
lbl_config = tk.Label(master=frm_config,
                      text= 'CONFIGURATIONS',
                      height=1).pack()
lbl_config2 = tk.Label(master=frm_config,
                      text= 'Select an option to convert',
                      height=2).pack()

# Radio Button
v = IntVar()
# Creating each button
radio_btn1 = tk.Radiobutton(master=frm_config,text='Single File',
                            variable=v, command=radio,
                            value=1).pack(side=LEFT)
radio_btn2 = tk.Radiobutton(master=frm_config,text='Multiple Files',
                            variable=v,command=radio,
                            value=2).pack(side=LEFT)


# Empty Label to create space
lbl_space1 = tk.Label(master=frm_config, height=2).pack()

# Frame A: It holds the Browse Button and Label
frm_a = tk.Frame(master=window,
                 width=100,
                 height=50)

#Label A: Browse instructions
lbl_a = tk.Label(master=frm_a,
                 text='Choose a file to be converted',
                 width= 80,
                 height=2).pack()


# Button Browse
btn_browse = tk.Button(master=frm_a,
                  text="Browse",
                  command=browse,
                  width=30,
                  height=3,
                  relief=tk.RAISED,
                  borderwidth=1).pack()

# Label Folder Selected: Show the address of the folder selected by the user
lbl_a2 = tk.Label(master=frm_a,
                  text='...',
                  bg='#8CA7B8',
                  width=80,
                  height=2)
lbl_a2.pack()

# Empty Label to create space
lbl_space2 = tk.Label(master=frm_a, height=2).pack()

# Frame B: It holds the buttons to convert to CSV or Parquet and instrucions label
frm_b = tk.Frame(master=window,
                 width=100,
                 height=50)

#Label B: instructions of this section
lbl_b = tk.Label(master=frm_b,
                 text='Click the Button to convert: CSV to PARQUET or PARQUET to CSV',
                 width= 90,
                 height=2).pack()

# Button Convert CSV to PARQUET
btn_toparquet = tk.Button(master=frm_b,
                  text="Convert CSV to PARQUET",
                  command=csv_to_parquet,
                  width=33,
                  height=3,
                  relief=tk.RAISED,
                  borderwidth=1,
                  bg='#6DBDEE').pack(side=LEFT)

# Button Convert PARQUET to CSV
btn_tocsv = tk.Button(master=frm_b,
                  text="Convert PARQUET TO CSV",
                  command=parquet_to_csv,
                  width=33,
                  height=3,
                  relief=tk.RAISED,
                  borderwidth=1,
                  bg='#3E81A3').pack(side=RIGHT)

# Frame C: Holds the information if the file was converted
frm_c = tk.Frame(master=window,
                 width=100,
                 height=50)

#Label C: Show the message when the file is succesfully converted.
lbl_c = tk.Label(master=frm_c,
                 text='...',
                 width= 90,
                 height=2)
lbl_c.pack()

# Empty Label to create space
lbl_space3 = tk.Label(master=frm_c, height=2).pack()

# Frame Quit Program
frm_quit = tk.Frame(master=window)
#Button Quit
btn_quit = tk.Button(master=frm_quit,
                     text='Quit',
                     command=quit_program,
                     width=30,
                     height=3,
                     relief=tk.RAISED,
                     borderwidth=1,
                     bg='#4188AB').pack()


# Packing the Frames
frm_config.pack()
frm_a.pack()
frm_b.pack()
frm_c.pack()
frm_quit.pack()

# Run the event loop
window.mainloop()

