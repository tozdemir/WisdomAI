from fastapi import FastAPI
from wai_preprocess import plot_data, get_column_names
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


@app.get("/plot_data")
async def plot_data_api(file_path: str, column_name: str):
    return plot_data(file_path, column_name)

# To run the API locally, run the following command in the terminal:
# uvicorn wai-preprocess_api:app --reload
# To run the API on AWS, run the following command in the terminal:
# uvicorn wai-preprocess_api:app --host



