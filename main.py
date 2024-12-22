from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from chain import TwoPhaseFinancialAdvisor
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from io import StringIO

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all HTTP headers
)

# Initialize the TwoPhaseFinancialAdvisor
advisor = TwoPhaseFinancialAdvisor()

# Define the Pydantic models for validation
class Debt(BaseModel):
    cardName: str
    cardType: str
    interestRate: float
    minimumPayment: float
    fullPayment: float
    remainingPeriod: int
    debtAmount: float

class UserData(BaseModel):
    income: str
    fixed_expense: str
    variable_expense: str
    total_debt: str
    saving: str
    cluster: str
    debts: List[Debt]

def load_json_to_dict(file_path: str) -> dict:
    """Load JSON data from a file and return it as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        return data_dict
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        return {}

@app.post("/api/financial_data/")
async def save_data(user_data: UserData):
    data_dict = user_data.dict()
    print(f"Cluster: {user_data.cluster}")

    try:
        with open("user_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
        return {"message": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")

@app.get("/")
async def Greeting():
    return {"message": "Hello, welcome to the financial advisor API!"}

@app.get("/api/get_initial_advice/")
async def get_initial_advice():
    file_path = 'user_data.json'
    financial_data = load_json_to_dict(file_path)
    print(financial_data)

    advice_type = financial_data['cluster']
    print(advice_type)

    try:
        initial_advice = advisor.get_initial_advice(financial_data, advice_type)
        return {"advice": initial_advice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating advice: {str(e)}")
