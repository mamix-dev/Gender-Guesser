from genderize import Genderize as gnd
import matplotlib.pyplot as plt
import tkinter as tk
import csv
import pandas as pd
import datetime as dt
import os


# These are the counters of the number of female and male guesses
M_Freq = 0
F_Freq = 0
M_Color = "#ffffcc"
F_Color = "#d1b3ff"

filepath = os.path.dirname(os.path.realpath(__file__))
REPLACE_ME = filepath + '\hdata.csv'


def color_changer(color):
    """This changes the background color of all the widgets."""
    root.config(bg = color)
    canvas.config(bg = color)
    name_entry.config(bg = color)
    output_text.config(bg = color)
    graph_label.config(bg = color)
    gender_finder_btn.config(bg = color)
    question_text.config(bg = color)
    graph_button.config(bg = color)
    graph_drop_box.config(bg = color)
    save_button.config(bg = color)

def namegender(): # Updates what the text will look like
    """
    This function is a bit of a workhorse...
        It logs whether the guess was a boy or a girl
        It calls for another function to change the background of everything depending on the gender
        And it changes the text to tell about what the API guesses
    """
    # These widgets are current session counters on male vs female count
    global M_Freq
    global F_Freq
    # These are widgets from the form
    global name_entry
    global output_text
    # This disgusting blob gets the entry we need as well as sorts out the response into usable data
    inputted_text = name_entry.get()
    list_of_names = []
    list_of_names.append(inputted_text)
    genderized_init = gnd().get(list_of_names)
    genderized_dict = dict(genderized_init[0])
    # This part finds the percentage version of the probability
    probability = "%" + str(genderized_dict['probability'] * 100)
    gender_init = genderized_dict['gender']
    # This is like if the name is invalid it'll say so
    try:
        gender = gender_init[0]
    except:
        output_text.config(text = "Invalid input")
    # Just cleaning the data here
    gender_final = gender.upper()
    # Logs the gender and changes the background
    if gender_final == "F":
        F_Freq += 1
        global F_Color
        color_changer(F_Color)
    elif gender_final == "M":
        M_Freq += 1
        global M_Color
        color_changer(M_Color)
    else:
        pass
    # Changes the label to the appropriate text.
    final = "Name: " + genderized_dict['name'] + '\nGender prediction: ' + gender_final + '\nConfidence in guess: ' + probability
    output_text.config(text = final)


def Graph_Current():
    """This area graphs the data from the current session in a pie chart and nothing more."""
    global F_Freq
    global M_Freq
    global F_Color
    global M_Color
    # Data to plot
    labels = 'Male', 'Female'
    sizes = [M_Freq, F_Freq]
    colors = [M_Color, F_Color]
    # Deciding on what gets "exploded"
    if M_Freq > F_Freq:
        explode = (0.1, 0)
    elif M_Freq < F_Freq:
        explode = (0, 0.1)
    else:
        explode = (0, 0)
    # Plot
    plt.pie(sizes, labels = labels, colors = colors, shadow = True, startangle = 45, autopct = '%1.1f%%', explode = explode)
    plt.axis('equal')
    plt.show()  


def Graph_Historical():
    global F_Color
    global M_Color
    global REPLACE_ME
    data = pd.read_csv(REPLACE_ME)
    dataframe = pd.DataFrame(data)
    M_Freq_LIST = dataframe[dataframe.columns[1]]
    F_Freq_LIST = dataframe[dataframe.columns[2]]
    MFF = []
    FFF = []
    for item in M_Freq_LIST:
        int(item)
        MFF.append(item)
    for item in F_Freq_LIST:
        int(item)
        FFF.append(item)
    M_Freq_Final = sum(MFF)
    F_Freq_Final = sum(FFF)
    labels = 'Male', 'Female'
    sizes = [M_Freq_Final, F_Freq_Final]
    colors = [M_Color, F_Color]
    if M_Freq_Final > F_Freq_Final:
        explode = (0.1, 0)
    elif M_Freq < F_Freq:
        explode = (0, 0.1)
    else:
        explode = (0, 0)
    plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, autopct = '%1.1f%%', startangle = 45)
    plt.axis('equal')
    plt.show()


def Master_Graph():
    global F_Freq
    global M_Freq
    global graph_drop_box
    graph_select = graph_drop_box_SETUP.get()
    if graph_select == "Current session":
        Graph_Current()
    elif graph_select == "Historical data":
        Graph_Historical()
    # label = "MAKE THIS WORK"
    # size = [1]
    # plt.pie(size, labels = label)
    # plt.show()


def Save_Data():
    """
    This part saves the data into a .csv format for later use
    """
    global F_Freq
    global M_Freq
    global REPLACE_ME
    current_log = [dt.datetime.now(), M_Freq, F_Freq]
    with open(REPLACE_ME, 'a') as i:
        appender = csv.writer(i, lineterminator = '\n') # Lineterminator makes sure the formatting isn't total ass
        appender.writerow(current_log)


# Tkinter begins
root = tk.Tk()

root.title("Genderizer")  # Assigns the name "Genderizer" to the top of the tkinter window
root.geometry("400x300")  # Window size
root.resizable(0,0)       # Can't change the size of the window


canvas = tk.Canvas(root)
canvas.pack()


question_text = tk.Label(canvas, text = "What name do you want to find the gender of?")
question_text.grid(row = 0, column = 0) # Is the text for the question

name_entry = tk.Entry(canvas)
name_entry.grid(row = 1, column = 0) # Is the place for user text input

output_text = tk.Label(canvas, text = "")
output_text.grid(row = 2, column = 0)

gender_finder_btn = tk.Button(canvas, text = "Find the gender", command = namegender)
gender_finder_btn.grid(row = 3, column = 0)

graph_label = tk.Label(canvas, text = '\nSelect the kind of graph you want,\nthen click "graph"')
graph_label.grid(row = 4, column = 0)

graph_drop_box_SETUP = tk.StringVar(canvas)
graph_drop_box_SETUP.set("Choose graph type") # Default value
# This top one is connected to the one beneath it
graph_drop_box = tk.OptionMenu(canvas, graph_drop_box_SETUP, "Current session", "Historical data")
graph_drop_box.grid(row = 5, column = 0)

graph_button = tk.Button(canvas, text = "Graph", command = Master_Graph)
graph_button.grid(row = 6, column = 0)

save_button = tk.Button(canvas, text = "Save data", command = Save_Data)
save_button.grid(row = 7, column = 0)

root.mainloop()
# Tkinter ends    