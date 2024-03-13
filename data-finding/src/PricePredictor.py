import matplotlib.pyplot as plot
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import logging
import os

#Takes file path and will open CSV and perform linear regression
def linearRegression(file_path: str, x_axis: str, y_axis: str, *args) -> list:
  """
  
  :param file_path: the relative path to the CSV to be used for the Linear Regression model
  :param x_axis: data column to be used as the x_axis of the Linear Regression model
  :param y_axis: data column to be used as the y_axis of the Linear Regression model
  :param *args: all columns to be dropped from the CSV
  """
  ab_path = os.path.dirname(__file__) #Grabs the location of the file and joins with desired file_path to create absolute path
  desired_path = os.path.join(ab_path, file_path)
  df = pd.read_csv(desired_path)
  df[x_axis] = pd.to_datetime(df[x_axis], yearfirst = True) #Transfer data column to datetime type.

  #Preprocessing
  cols = [i for i in args]
  df = df.drop(cols, axis=1)

  #Either drop or create normalized values for null values
  #Dropping because median listing price is important
  df = df.dropna()

  #transfer to usable data
  x = df[x_axis].values
  y = df[y_axis].values

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)


  reg = LinearRegression()# Create the model
  x_train = x_train.reshape(-1,1) # Reshape the data to a 2D array as it is currently a 1D array
  y_train = y_train.reshape(-1,1)
  reg.fit(x_train, y_train)#Fit the model and use training data

  y_pred = reg.predict(df[x_axis].values.astype(float).reshape(-1,1)) #Predict off the entire dataset and add prediction to the dataframe
  df['pred'] = y_pred

  ax = df.plot(x=x_axis, y=y_axis, color='black', style='.')#Plot the data
  df.plot(x=x_axis, y='pred', color='orange', linewidth=3, ax=ax, alpha = 0.5)
  ax.set_title("Prediction of zip code")
  ax.set_xlabel(x_axis)
  ax.set_ylabel(y_axis)
  pred_score = reg.score(df[x_axis].values.astype(float).reshape(-1,1),df[y_axis].values)
  return [pred_score, ax]

# Example use of linear regression
if __name__ == "__main__":
  log = logging.getLogger()
  log.setLevel(logging.INFO)
  pred_list = linearRegression("../data/RDC_Inventory_Core_Metrics_Zip_History_processed_files/77433data.csv", "date", "median_price", "postal_code", "location_name", "active_listing_count", "median_days_on_market","median_sqft","average_price","total_listing_count","quality_flag")
  score = pred_list[0]
  logging.info(score)
  ax = pred_list[1]
  plot.show()