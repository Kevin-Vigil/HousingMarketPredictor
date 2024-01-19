import tkinter as tk 
from tkinter import filedialog
import re
import json
import csv
import os

class FileReader():

  initPath = ""

  def setInitPath(self, path):
    path = path[::-1]
    search = re.search("/", path) 
    if search:
      path = path[search.span()[1]:]
      path = path[::-1]
      print(path)
    # print(search)
    # print(search[-1])
    self.initPath = path

    # print(self.initPath)

  def cleanLine(self, line):
    return line

  

  def parseCSV(self, file_path):
    write_path = file_path[0:len(file_path)-4] + "_processed.csv"
    if os.path.exists(write_path):
      os.remove(write_path)
    write_file = open(write_path,"x")
    with open(file_path, newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='"')
      for row in reader:
        print(len(row))
        row = self.cleanLine(row)
        write_file.write(",".join(row) + "\n")

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
    return False

  def openFile(self):
    # print(self.initPath)
    file_path = filedialog.askopenfilename(initialdir=self.initPath)
    if type(file_path) == str and file_path.endswith('.csv'):
      self.parseCSV(file_path)
      # print(file_path)
      self.setInitPath(file_path)
    elif type(file_path) == str:
      try:
        file = open(file_path,'r')
        print(file.read())
        file.close()
      except FileNotFoundError:
        print("User did not choose a file.\n")
      else:
        self.setInitPath(file_path)
    else:
      print("User did not choose a file.\n")
      

def main():
  reader = FileReader()
  window = tk.Tk()
  button = tk.Button(text="Open", command=reader.openFile)
  button.pack()
  window.mainloop()

  # subprocess.Popen(r'explorer /select')

if __name__ == "__main__":
  main()