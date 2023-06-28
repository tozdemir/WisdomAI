# This python script reads a CSV file and plots the data as a line plot
# CSV file is located in a folder called `data` in one folder above the current folder
# The CSV file is called `data.csv`
# This python script will be integrated into FastAPI to create a web app 
# The plot will be displayed on the web app
# The API will be deployed on AWS
# The API will be called by a NextJS web app and the frontend will be deployed on Vercel with Typescript

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

ID = 3

# Define a function with CSV file path as input and the plot as output. 
# As an additional input add the column id to be plotted against the first column, which is assumed to be the date time column.
def plot_data(csv_file_path: str, column_name: str):
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    # Assume you don`t know the column names but first column is date time. Convert first column to datetime
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
    # Set first column as index
    df.set_index(df.columns[0], inplace=True)
    # Plot the data on the column name input against the first column
    df.plot(y=column_name)
    # Save plot as png to data output folder
    plt.savefig(os.path.join(os.path.dirname(__file__),'..','data','output','plot.png'))
    # return the plot file path 
    return os.path.join(os.path.dirname(__file__),'..','data','output', 'plot.png')

# Define a function to return the titles of each column in dataframe.
def get_column_names(csv_file_path):
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    # Return the column names except the first column
    return df.columns[1:]


# Write a main function to test the function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i", type=str, required=True)
    args = parser.parse_args()
    file_path = args.input
    column_names = get_column_names(file_path)
    # print column names with corresponding column ids
    for i in range(len(column_names)):
        print(i+1, column_names[i])

    # Ask user for the column id to be plotted against the first column
    column_id = int(input("Please enter the column id to be plotted against the first column: "))
    # Get column name as string
    column_name = column_names[column_id-1]

    # Call the function
    path = plot_data(file_path, column_name)
    print(path)

if __name__ == '__main__':
    main()

