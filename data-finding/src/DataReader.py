import tkinter as tk 
from tkinter import filedialog
import re
import json
import csv
import os
import datetime

class FileReader:

  initPath = ""
  data_mapper = json.load(open(os.getcwd() + "/data-finding/assets/mapper.json"))
  formatter = []

  def setInitPath(self, path):
    path = path[::-1]
    search = re.search("/", path) 
    if search:
      path = path[search.span()[1]:]
      path = path[::-1]
    self.initPath = path

    # print(self.initPath)

  #CleanLine cleans the data to remove certain data points from the CSV based on the format provided by realtor.com
  def cleanLine(self, line):
    output = []
    for i in range(len(self.formatter)):
      #Must always check if location name is found
      #Must also always check if there are a total len of formmater in each line
      if self.data_mapper[str(i+1)]["type"] == "date":
        year = line[self.formatter[i]][0:4]
        month = line[self.formatter[i]][4:]
        output.append(year + "-" + month + "-" + "1")
      elif self.data_mapper[str(i+1)]["type"] == "str":
        output.append("\"" + line[self.formatter[i]] + "\"")
      else:
        output.append(line[self.formatter[i]])
    return output

  def createFormatter(self, line):
    name_list = []
    for i in range(len(line)):
      for key in self.data_mapper.keys():
        if line[i] == self.data_mapper[key]["name"]:
          self.formatter.append(i)
          name_list.append(self.data_mapper[key]["name"])
          break
    return name_list



  def parseCSV(self, file_path):
    write_path = file_path[0:len(file_path)-4] + "_processed.csv"

    if os.path.exists(write_path):
      os.remove(write_path)
    write_file = open(write_path,"x")
    with open(file_path, newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='"')
      formatter_line = reader.__next__()
      menu_line = self.createFormatter(formatter_line)
      write_file.write(",".join(menu_line) + "\n")
      for row in reader:
        row = self.cleanLine(row)
        if row:
          write_file.write(",".join(row) + "\n")
          # print(row)
    print("Complete")
    write_file.close()



class FileSplitter:
  initPath = ""
  file_finder = {}
  file_writers = []
  file_index = -1

  def getWD(self, path):
    path = path[::-1]
    search = re.search("/", path) 
    if search:
      path = path[search.span()[1]:]
      path = path[::-1]
      print(path)
    return path

  def setInitPath(self, path):
    self.initPath = self.getWD(path)
  
  #This function will split a csv into multiple files based on a certain key
  def split(self, file_path, key):
    
    index_counter = 0 #counter to track writers
    with open(file_path, newline='') as csv_file:
      reader = csv.reader(csv_file, delimiter=',', quotechar='"')
      #Grab the first line and find the key
      menu = reader.__next__()
      for i in range(len(menu)):
        if key == menu[i]:
          self.file_index = i
      if self.file_index == -1:
        print("Unable to find key in CSV file. Operation cancelled.")
        return False 
      #If key found, create a folder as there can be an extreme amount of CSV files
      writer_path = file_path[0:len(file_path)-4] + "_files"
      os.mkdir( writer_path)
      #Run through CSV using key index to split csv into multiple files
      for row in reader:
        #If file not already made, create a file and write to it.
        if row[self.file_index] not in self.file_finder:
          self.file_finder[row[self.file_index]] = index_counter
          index_counter += 1
          new_file_path = writer_path + "/" + row[self.file_index] + "data.csv"
          if os.path.exists(new_file_path):
            os.remove(new_file_path)
          self.file_writers.append(open(new_file_path,"x"))
          self.file_writers[self.file_finder[row[self.file_index]]].write(",".join(menu) + "\n")
        row[2] = "\"" + row[2] + "\""
        self.file_writers[self.file_finder[row[self.file_index]]].write(",".join(row) + "\n")
      #Close all files before exiting
      for i in self.file_writers:
        i.close()  
    print("complete")  
    
def openFile():
  reader = FileReader()
  file_path = filedialog.askopenfilename(initialdir=reader.initPath)
  if type(file_path) == str and file_path.endswith('.csv'):
    reader.parseCSV(file_path)
    reader.setInitPath(file_path)
  elif type(file_path) == str:
    try:
      file = open(file_path,'r')
      print(file.read())
      file.close()
    except FileNotFoundError:
      print("User did not choose a file.\n")
      del reader
      return False
    else:
      reader.setInitPath(file_path)
  else:
    print("User did not choose a file.\n")
    del reader
    return False
  del reader
  return True

def splitFile():
  splitter = FileSplitter()
  splitKey = keyInput.get()
  file_path = filedialog.askopenfilename(initialdir=splitter.initPath)
  if type(file_path) == str and file_path.endswith('.csv'):
    splitter.split(file_path, splitKey)
    splitter.setInitPath(file_path)
  elif type(file_path) == str:
    try:
      file = open(file_path,'r')
      print(file.read())
      file.close()
    except FileNotFoundError:
      print("User did not choose a file.\n")
      del splitter
      return False
    else:
      splitter.setInitPath(file_path)
  else:
    print("User did not choose a file.\n")
    del splitter
    return False
  del splitter
  return True

def main():
  keyInput.grid(row=2,column=1, padx=5, pady=10)
  keyLabel.grid(row=2,column=0, padx=5, pady=10)
  button.grid(row=1, column=1, pady=10)
  splitter.grid(row=3, column=1)

  window.mainloop()


  # subprocess.Popen(r'explorer /select')

window = tk.Tk()
button = tk.Button(text="Open file", command=openFile)
splitter = tk.Button(text="Split CSV", command=splitFile)

keyLabel = tk.Label(window, text="Key")
keyInput = tk.Entry(window, bd =5)



if __name__ == "__main__":
  main()