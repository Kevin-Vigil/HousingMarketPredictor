import matplotlib.pyplot as plot
import numpy as np
import csv
import datetime
import pandas as pd
import sys
import os

arrXAxis =[]
arrYAxis =[]



#Graph a CSV given an X and Y axis index
def graphXY(filePath, xIndex: int, yIndex: int):
  #Creates example data and runs it. not complete
  df = pd.read_csv("data-finding/data/RDC_Inventory_Core_Metrics_Zip_History_processed_files/75082data.csv")
  df.plot(kind = "scatter", x = "date", y = "median_price")
  plot.show()

#To give an example of what the dataset looks like, and the output of the program, I have put the csv of my childhood zipcode.
#This will be used for all examples. Please keep in mind, this is a complete dataset (July 2016-December 2023).
#Not all datasets are complete

#Turned this into a fuctnion
def linearRegression() -> None:
  #print(os.getcwd())
  df = pd.read_csv("data-finding/data/RDC_Inventory_Core_Metrics_Zip_History_processed_files/75082data.csv")
  df['date'] = pd.to_datetime(df["date"], yearfirst = True)
  #Preprocessing
  cols = ["postal_code", "location_name", "active_listing_count", "median_days_on_market","median_sqft","average_price","total_listing_count","quality_flag"]
  df = df.drop(cols, axis=1)
  df.info()

  #Either drop or create normalized values for null values
  #Dropping because median listing price is important
  df = df.dropna()
  df.info()

  from sklearn.model_selection import train_test_split

  #transfer to usable data


  df.date = pd.to_datetime(df.date)
  x = df.date.values
  # x_temp = dateTransfer(x)
  y = df['median_price'].values
  print(x)
  print(y)
  # x = np.delete(x, 1, axis = 1)

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

  plot.plot(x_train, y_train, 'ro')
  plot.title("Train data")
  plot.show()

  print(x_train)
  print(y_train)

  plot.plot(x_test, y_test, 'ro')
  plot.title("Test data")
  plot.show()
  print(x_test)
  print(y_test)

  from sklearn.linear_model import LinearRegression

  reg = LinearRegression()# Create the model
  x_train = x_train.reshape(-1,1) # Reshape the data to a 2D array as it is currently a 1D array
  y_train = y_train.reshape(-1,1)
  reg.fit(x_train, y_train)#Fit the model and use training data

  y_pred = reg.predict(df.date.values.astype(float).reshape(-1,1)) #Predict off the entire dataset and add prediction to the dataframe
  df['pred'] = y_pred

  ax = df.plot(x='date', y='median_price', color='black', style='.')#Plot the data
  df.plot(x='date', y='pred', color='orange', linewidth=3, ax=ax, alpha = 0.5)
  ax.set_title("Prediction of Zip code 77433")
  ax.set_xlabel("Date")
  ax.set_ylabel("Median Price")
  plot.show()


graphXY("77433data.csv", 0, 4)
linearRegression()


# reg.score(x_train,y_train)