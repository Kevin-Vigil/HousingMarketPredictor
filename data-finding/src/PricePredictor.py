import matplotlib.pyplot as plot
import numpy as np
import csv
import sys
import datetime

#HELPER: Find indexes of given x and y axis
def indexFinder(reader, x, y):
  xIndex = -1
  yIndex = -1
  menu = reader.__next__()
  for i in range(len(menu)):
    if x == menu[i]:
      xIndex = i
    if y == menu[i]:
      yIndex = i
  return (xIndex, yIndex)

#HELPER: create array from csv given index to grab from
def createArray(reader, index: int):
  axis = []
  for row in reader:
    axis.append(row[index])
  return axis



#Run linear regression on an CSV based on given x and y axis
def linearRegression():
  return False

#HELPER: turn string into date
def convertDate(date: str):
  year = date[0:4]
  month = date[4:]
  return datetime.date(int(year),int(month),1)

#Graph a CSV given an X and Y axis index
def graphXY(filePath, xIndex: int, yIndex: int):
  with open(filePath, newline="") as csvFile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    if xIndex != -1 and yIndex != -1:
      arrXAxis = []
      arrYAxis = []
      for row in reader:
        arrXAxis.append(convertDate(row[xIndex]))
        arrYAxis.append(int(row[yIndex]))
      arrXAxis = arrXAxis[::-1]
      arrYAxis = arrYAxis[::-1]
      plot.plot(arrXAxis,arrYAxis, "ro")
      # plot.axis((201600, 202312, 300000,700000))
      plot.show()

if __name__=='__main__':
  # print ('argument list', sys.argv)
  #arg 1: file
  #arg 2: 0
  #arg 3: 4
  graphXY(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))