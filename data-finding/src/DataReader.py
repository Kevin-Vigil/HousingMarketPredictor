import tkinter as tk 
from tkinter import filedialog
import re
import json
import csv
import os
import logging

#CleanLine cleans the data to remove certain data points from the CSV based on the format provided by createFormatter
def cleanLine(line):
  output = []
  for i in range(len(formatter)):
    #Must always check if location name is found
    #Must also always check if there are a total len of formmater in each line
    if data_mapper[str(i+1)]["type"] == "date":
      year = line[formatter[i]][0:4]
      month = line[formatter[i]][4:]
      output.append(year + "-" + month + "-" + "1")
    elif data_mapper[str(i+1)]["type"] == "str":
      output.append("\"" + line[formatter[i]] + "\"")
    else:
      output.append(line[formatter[i]])
  return output

def setInitPath(path: str) -> None:
  path = path[::-1]
  search = re.search("/", path) 
  if search:
    path = path[search.span()[1]:]
    path = path[::-1]
  initPath = path

#Runs through the json file and maps each column so it can properly format when using the clean line function
def createFormatter(line: list) -> list:
  name_list = []
  for i in range(len(line)):
    for key in data_mapper.keys():
      if line[i] == data_mapper[key]["name"]:
        formatter.append(i)
        name_list.append(data_mapper[key]["name"])
        break
  return name_list

#Function runs through the csv and will write to it's respective file based on a certain key given
  #EX: if zip_code is given for key, folder will be created with multiple files each created based on the value of the chosen column/key
def split(file_path: str, key: str) -> bool:
  index_counter = 0 #counter to track writers
  with open(file_path, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    #Grab the first line and find the key
    menu = reader.__next__()
    for i in range(len(menu)):
      if key == menu[i]:
        file_index = i
    if file_index == -1:
      logging.error("Unable to find key in CSV file. Operation cancelled.")
      return False 
    #If key found, create a folder as there can be an extreme amount of CSV files
    writer_path = file_path[0:len(file_path)-4] + "_files"
    os.mkdir( writer_path)
    #Run through CSV using key index to split csv into multiple files
    for row in reader:
      #If file not already made, create a file and write to it.
      if row[file_index] not in file_finder:
        file_finder[row[file_index]] = index_counter
        index_counter += 1
        new_file_path = writer_path + "/" + row[file_index] + "data.csv"
        if os.path.exists(new_file_path):
          os.remove(new_file_path)
        file_writers.append(open(new_file_path,"x"))
        file_writers[file_finder[row[file_index]]].write(",".join(menu) + "\n")
      row[2] = "\"" + row[2] + "\""
      file_writers[file_finder[row[file_index]]].write(",".join(row) + "\n")
    #Close all files before exiting
    for i in file_writers:
      i.close()  
  logging.info("complete")
  return True

#Will run through the CSV and cleans based on formatter, or splits based on whether key was passed.
#Parent function that will call multiple helper functions.
def parseCSV(file_path: str, **kwargs) -> bool:
  if "key" in kwargs:
    return split(file_path, kwargs["key"])
  else:
    write_file = filedialog.asksaveasfile()
    if not write_file:
      logging.error("User did not select file")
      return False
    with open(file_path, newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='"')
      formatter_line = reader.__next__()
      menu_line = createFormatter(formatter_line)
      write_file.write(",".join(menu_line) + "\n")
      for row in reader:
        row = cleanLine(row)
        if row:
          write_file.write(",".join(row) + "\n")
    logging.info("Complete")
    write_file.close()
    return True

#depending on what button is pressed, this function is called to handle button presses and will process a file
def openFile(**kwargs) -> None:
  file_path = filedialog.askopenfilename(initialdir=initPath)
  if type(file_path) == str and file_path.endswith('.csv'):
    logging.info("Operation completed: " + parseCSV(file_path, **kwargs))
    setInitPath(file_path)
  elif type(file_path) == str:
    try:
      file = open(file_path,'r')
      logging.info(file.read())
      file.close()
    except FileNotFoundError:
      logging.error("User did not choose a file.\n")
    else:
      setInitPath(file_path)
  else:
    logging.error("User did not choose a file.\n")

def main() -> None:
  keyInput.grid(row=2,column=1, padx=5, pady=10)
  keyLabel.grid(row=2,column=0, padx=5, pady=10)
  button.grid(row=1, column=1, pady=10)
  splitter.grid(row=3, column=1)

  window.mainloop()



file_finder = {}
file_writers = []
file_index = -1

ab_path = os.path.dirname(__file__) #Grabs the location of the file and creates a path to the formatter (json)
desired_path = os.path.join(ab_path, "../assets/mapper.json")
data_mapper = json.load(open(desired_path)) #Load
initPath = ab_path #sets initial path
formatter = []

window = tk.Tk() #Create GUI Root component
button = tk.Button(text="Open file", command=lambda: openFile()) #Create buttons for each operation
splitter = tk.Button(text="Split CSV", command=lambda: openFile(key = keyInput.get())) #Button that will grab input from what is put into input field

keyLabel = tk.Label(window, text="Key") #field to input key
keyInput = tk.Entry(window, bd =5)

if __name__ == "__main__":
  main()