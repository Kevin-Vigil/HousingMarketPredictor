import matplotlib.pyplot as plot
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import logging
import os

#Graph a CSV given an X and Y axis index
def graphXY(filePath, xIndex: int, yIndex: int) -> None:
  #Creates example data and runs it. not complete
  df = pd.read_csv("data-finding/data/RDC_Inventory_Core_Metrics_Zip_History_processed_files/75082data.csv")
  df.plot(kind = "scatter", x = "date", y = "median_price")
  plot.show()

#To give an example of what the dataset looks like, and the output of the program, I have put the csv of my childhood zipcode.
#This will be used for all examples. Please keep in mind, this is a complete dataset (July 2016-December 2023).
#Not all datasets are complete

#Takes file path and will open CSV and perform linear regression
def linearRegression(file: str, *args,**kwargs) -> list:
  ab_path = os.path.dirname(__file__) #Grabs the location of the file and joins with desired file to create absolute path
  desired_path = os.path.join(ab_path, file)
  # logging.debug(desired_path) #Extra info for debugging
  df = pd.read_csv(desired_path)
  df[kwargs['x_axis']] = pd.to_datetime(df[kwargs['x_axis']], yearfirst = True) #Transfer data column to datetime type.

  #Preprocessing
  #Commented code for all cols that I will be droppings, utilizing args to now drop all cols
  # cols = ["postal_code", "location_name", "active_listing_count", "median_days_on_market","median_sqft","average_price","total_listing_count","quality_flag"]
  cols = [i for i in args]
  # logging.debug(cols)
  df = df.drop(cols, axis=1)
  # df.info() #Extra info for debugging

  #Either drop or create normalized values for null values
  #Dropping because median listing price is important
  df = df.dropna()
  # df.info() #Extra info for debugging



  #transfer to usable data
  x = df[kwargs['x_axis']].values
  y = df[kwargs['y_axis']].values
  # logging.info(x)
  # logging.info(y)

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

  # Extra data for debugging
  # plot.plot(x_train, y_train, 'ro')
  # plot.title("Train data")
  # plot.show()

  # logging.info(x_train)
  # logging.info(y_train)

  # Extra data for debugging
  # plot.plot(x_test, y_test, 'ro')
  # plot.title("Test data")
  # plot.show()

  # logging.info(x_test)
  # logging.info(y_test)


  reg = LinearRegression()# Create the model
  x_train = x_train.reshape(-1,1) # Reshape the data to a 2D array as it is currently a 1D array
  y_train = y_train.reshape(-1,1)
  reg.fit(x_train, y_train)#Fit the model and use training data

  y_pred = reg.predict(df[kwargs['x_axis']].values.astype(float).reshape(-1,1)) #Predict off the entire dataset and add prediction to the dataframe
  df['pred'] = y_pred

  ax = df.plot(x=kwargs['x_axis'], y=kwargs['y_axis'], color='black', style='.')#Plot the data
  df.plot(x=kwargs['x_axis'], y='pred', color='orange', linewidth=3, ax=ax, alpha = 0.5)
  ax.set_title("Prediction of zip code")
  ax.set_xlabel(kwargs['x_axis'])
  ax.set_ylabel(kwargs['y_axis'])
  pred_score = reg.score(df[kwargs['x_axis']].values.astype(float).reshape(-1,1),df[kwargs['y_axis']].values)
  return [pred_score, ax]


# graphXY("77433data.csv", 0, 4)

# Example use of linear regression
if __name__ == "__main__":
  log = logging.getLogger()
  log.setLevel(logging.NOTSET)
  pred_list = linearRegression("../data/RDC_Inventory_Core_Metrics_Zip_History_processed_files/75082data.csv","postal_code", "location_name", "active_listing_count", "median_days_on_market","median_sqft","average_price","total_listing_count","quality_flag", x_axis="date", y_axis="median_price")
  score = pred_list[0]
  print(score)
  ax = pred_list[1]
  plot.show()


# reg.score(x_train,y_train)