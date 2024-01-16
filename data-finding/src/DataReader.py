import tkinter as tk 
from tkinter import filedialog
import re
import json

class FileReader():

  initPath = ""

  def setInitPath(self, path):
    search = re.finditer("/", path)
    # print(search)
    # print(search[-1])
    self.initPath = path

    # print(self.initPath)

  def parseCSV(self, file_path):
    file = open(file_path, 'r')
    data = dict()
    id = 0
    #write_file = open("./sample.json","x")
    for i in file:
      data[id] = i
      id += 1

    with open("sample.json", "x") as convert_file:
      convert_file.write(json.dumps(data))
    file.close()
    #write_file.close()
    print(data)

  def openFile(self):
    print(self.initPath)
    file_path = filedialog.askopenfilename(initialdir=self.initPath)
    if type(file_path) == str and file_path.endswith('.csv'):
      self.parseCSV(file_path)
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