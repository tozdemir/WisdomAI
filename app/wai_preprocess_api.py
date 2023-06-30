from fastapi import FastAPI
from wai_preprocess import upload_csv_to_s3,plot_data_and_save_to_S3, get_column_names
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/get_column_names")
async def get_column_names_api(file_path: str):
    # convert the column names to a list of strings
    return list(get_column_names(file_path))

@app.get("/plot_data_and_save_to_s3")
async def plot_data_and_save_to_S3_api(file_name: str, column_name: str):
    return plot_data_and_save_to_S3(file_name, column_name)

@app.get("/upload_csv_to_s3")
async def upload_csv_to_s3_api(file_path: str):
    return upload_csv_to_s3(file_path)

# To run the API locally, run the following command in the terminal:
# uvicorn wai_preprocess_api:app --reload
# To run the API on AWS, run the following command in the terminal:
# uvicorn wai_preprocess_api:app --host



