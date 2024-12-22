from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

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

# POST request to save data to a JSON file
@app.post("/save_data/")
async def save_data(user_data: UserData):
    data_dict = user_data.dict()

    # Print the cluster field
    print(f"Cluster: {user_data.cluster}")

    # Save data to JSON file
    try:
        with open("user_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
        return {"message": "Data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")
