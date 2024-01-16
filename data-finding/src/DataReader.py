import tkinter as tk 
from tkinter import filedialog

class FileReader():

  initPath = ""

  def setInitPath(self, path):
    self.initPath = path

  def openFile(self):
    file_path = filedialog.askopenfilename(initialdir=self.initPath)
    if type(file_path) == str:
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