# Housing market prediction project

This book exists to explain what I did and how I created this project.

## Data Parser

After downloading good data from [realtor.com](https://www.realtor.com/research/data/), I started creating a parser.

- Files are in CSV, must be cleaned and set up for ML models.
- Use a mapper json file to create columns to keep in the dataset. Use this to run through the CSV and prune unneeded data, and condense down to the columns to keep.
- Split data by zip code into multiple files in a seperate folder

#### Cleaning Large CSV File

> In order to clean the file, we must first read the mapper json, then use said mapper to create the columns for the processed file.

1. Create a mapper json file in the assets folder (any locations works as long as you reference to it properly)
2. Open the file using the simple GUI (Created button and set it to open a file selection window to request the file location)
3. Create a file that will run the off the format of the mapper in code. use the mapper to find the index of each column to transfer to the new file.
4. Run through the CSV and add selected columns to line to pass to processed file.

#### Splitting Processed CSV File

> The idea of this is to seperate data and allow ML models to run on specific areas instead of overall data

1. Using a key inputted into the text box, press the split button and open the file (Simple GUI)
2. Using the key, create a folder that will hold multiple files. This is important in the case that there is a large data set that needs to be split into a great number of files.
	- There may be times that a folder already exists (file already split from), in this case, the program will not work. This is intended as this entire file was made for personal use.
3. The key will search through the file (preferably an already processed file) and will append to the file of that key
	- In the case that there is no file, a file will be created.
	- If a file is created, We must add the file writer to a list that we can access later on. This can be in the form of a dictionary.
4. Read the column where the key exists (Check that the column of said key exists) and start writing each line to their respective file.
5. After completion, run through the list to close all files.

## Working with the data

From here, we have all the data in a format that we can work with, including the complete dataset, and the processed dataset. We can use all of this later on for our ML models.

- Predict housing market median prices by month, in this case each dataset is split by zipcode.

