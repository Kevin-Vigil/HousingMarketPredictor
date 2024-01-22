import tkinter as tk 
from tkinter import filedialog
import re
import json
import csv
import os

class FileReader():

  initPath = ""
  data_mapper = json.load(open(os.getcwd() + "/data-finding/assets/mapper.json"))
  formatter = []

  def setInitPath(self, path):
    path = path[::-1]
    search = re.search("/", path) 
    if search:
      path = path[search.span()[1]:]
      path = path[::-1]
      #print(path)
    # print(search)
    # print(search[-1])
    self.initPath = path

    # print(self.initPath)

  #CleanLine cleans the data to remove certain data points from the CSV based on the format provided by realtor.com
  def cleanLine(self, line):
    output = []
    for i in self.formatter:
      #Must always check if location name is found
      try:
        int(line[i])
      except Exception:
        output.append("\"" + line[i] + "\"")
      else:
        output.append(line[i])
    return output

  #Parser
  #CSVMapper = {}
  #formatter = {}
  #def parseCSV(CSV):
    #open csv
    #for line in csv:
      #clean line
  
  #def cleanLine(Line):
    #line = []
    #if formatter:
      #for i in line:
        #
  def createFormatter(self, line):
    for i in range(len(line)):
      for key in self.data_mapper.keys():
        if line[i] == key:
          self.formatter.append(i)
          break
    #print(self.formatter)



  def parseCSV(self, file_path):
    write_path = file_path[0:len(file_path)-4] + "_processed.csv"

    if os.path.exists(write_path):
      os.remove(write_path)
    write_file = open(write_path,"x")
    with open(file_path, newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='"')
      for row in reader:
        if len(self.formatter) == 0:
          self.createFormatter(row)
        row = self.cleanLine(row)
        if row:
          write_file.write(",".join(row) + "\n")
          print(row)

    write_file.close()
    # print(row)
    # file = open(file_path, 'r')
    # data = dict()
    # id = 0
    
    # print("This is the new write path: " + write_path)

    
    # for i in file:
    #   i = self.cleanLine(i)
    #   data[id] = i
    #   id += 1

    
    # with open("sample.json", "x") as convert_file:
    #   convert_file.write(json.dumps(data))
    # file.close()
    # #write_file.close()
    # print(data)

  
      
def openFile():
  reader = FileReader()
  # print(self.initPath)
  file_path = filedialog.askopenfilename(initialdir=reader.initPath)
  if type(file_path) == str and file_path.endswith('.csv'):
    reader.parseCSV(file_path)
    # print(file_path)
    reader.setInitPath(file_path)
  elif type(file_path) == str:
    try:
      file = open(file_path,'r')
      print(file.read())
      file.close()
    except FileNotFoundError:
      print("User did not choose a file.\n")
    else:
      reader.setInitPath(file_path)
  else:
    print("User did not choose a file.\n")

def main():
  window = tk.Tk()
  button = tk.Button(text="Open", command=openFile)
  button.pack()
  window.mainloop()

  # subprocess.Popen(r'explorer /select')

if __name__ == "__main__":
  main()