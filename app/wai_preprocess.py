# This python script reads a CSV file and plots the data as a line plot
# CSV file is located in a folder called `data` in one folder above the current folder
# The CSV file is called `data.csv`
# This python script will be integrated into FastAPI to create a web app 
# The plot will be displayed on the web app
# The API will be deployed on AWS
# The API will be called by a NextJS web app and the frontend will be deployed on Vercel with Typescript

# Import libraries
import pandas as pd
import argparse
import boto3
from io import BytesIO
import awswrangler as wr

ID = 3
try:
    session_upload = boto3.Session(profile_name='default')
except Exception:
    session_upload = boto3.Session()
s3_upload = session_upload.client('s3')
out_bucket = 'csv-s3-bucket-waipreprocess-output'
in_bucket = 'csv-s3-bucket-waipreprocess'

# Define a function with CSV file path as input and the plot as output. 
# As an additional input add the column id to be plotted against the first column, which is assumed to be the date time column.
def plot_data_and_save_to_S3(file_bucket_name: str, column_name: str):
    # Read CSV file
    # get the csv file from S3 bucket
    out_key = 'plot.png'
    df = wr.s3.read_csv(path=f's3://{in_bucket}/{file_bucket_name}',boto3_session=session_upload)
    # Assume you don`t know the column names but first column is date time. Convert first column to datetime
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
    # Set first column as index
    df.set_index(df.columns[0], inplace=True)
    # Plot the data on the column name input against the first column
    img_data = BytesIO()
    df.plot(y=column_name).get_figure().savefig(img_data, format='png', dpi=300, bbox_inches='tight', pad_inches=0.2)
    img_data.seek(0)
    # put plot in S3 bucket
    bucket = session_upload.resource('s3').Bucket(out_bucket)
    bucket.put_object(Body=img_data, ContentType='image/png', Key=out_key)
    # return the plot file path 
    return out_key

# Define a function to return the titles of each column in dataframe.
def get_column_names(file_bucket_name):
    # Read CSV file
    #df = pd.read_csv(csv_file_path)
    df = wr.s3.read_csv(path=f's3://{in_bucket}/{file_bucket_name}',boto3_session=session_upload)
    # Return the column names except the first column
    return df.columns[1:]

# define a function to upload a csv file to AWS S3 bucket.
def upload_csv_to_s3(csv_file_path):
    # Specify a unique file name for the csv file in the bucket
    file_name = 'data.csv'
    #bucket = boto3.resource('s3').Bucket(in_bucket)
    #bucket.put_object(Key=file_name, Body=csv_file_path)
    s3_upload.upload_file(csv_file_path, in_bucket, file_name)
    return file_name

# Write a main function to test the function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i", type=str, required=True)
    args = parser.parse_args()
    file_path = args.input
    s3_file_name = upload_csv_to_s3(file_path)
    column_names = get_column_names(s3_file_name)
    # print column names with corresponding column ids
    for i in range(len(column_names)):
        print(i+1, column_names[i])

    # Ask user for the column id to be plotted against the first column
    column_id = int(input("Please enter the column id to be plotted against the first column: "))
    # Get column name as string
    column_name = str(column_names[column_id-1])

    # Call the function
    plot_data_and_save_to_S3(s3_file_name,column_name)
    print("Plot saved to S3 bucket")

if __name__ == '__main__':
    main()

