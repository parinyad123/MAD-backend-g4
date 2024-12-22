from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from chain import TwoPhaseFinancialAdvisor
from fastapi.responses import StreamingResponse
# import json
from io import StringIO

app = FastAPI()

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

# Placeholder function to simulate chatbot processing with 'cluster' as input
def chatbot_process(data: dict, cluster: str):
    # Example chatbot function: here you can process the data as required by your chatbot
    # Now, the chatbot process uses both data and cluster as inputs
    print(cluster)
    print(data)
    return f"Chatbot received the following data: {data} with cluster: {cluster}"

def load_json_to_dict(file_path: str) -> dict:
    """Load JSON data from a file and return it as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)  # Read JSON file into dictionary
        return data_dict
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        return {}

# POST request to save data to a JSON file
@app.post("/api/financial_data/")
async def save_data(user_data: UserData):
    data_dict = user_data.dict()

    # Print the cluster field
    print(f"Cluster: {user_data.cluster}")

    # Save data to JSON file
    try:
        with open("user_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
        return {"message": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")


@app.get("/")
async def Greeting():
    return {"message": "Hello, welcome to the financial advisor API!"}

    # GET request for initial advice
@app.get("/api/get_initial_advice/")
async def get_initial_advice():
    # """Retrieve initial financial advice based on the financial data loaded from a JSON file"""
    # if advice_type.lower() not in ["red", "yellow"]:
    #     raise HTTPException(status_code=400, detail="Advice type must be 'red' or 'yellow'.")
    
    # Define the path to the JSON file
    file_path = 'user_data.json'  # The path to the user data JSON file
    
    # Load the financial data from the provided JSON file
    # financial_data = load_financial_data_from_json(file_path)
    file_path = 'user_data.json'  # Path to your JSON file
    financial_data = load_json_to_dict(file_path)
    print(financial_data)

    advice_type = financial_data['cluster']
    print(advice_type)

    # Get the initial advice
    try:
        initial_advice = advisor.get_initial_advice(financial_data, advice_type)
        return {"advice": initial_advice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating advice: {str(e)}")
    
        # Get the initial advice
    # try:
    #     initial_advice = advisor.get_initial_advice(financial_data, advice_type)
        
    #     # Convert the response to a stream (use StringIO to simulate a file-like object)
    #     advice_stream = StringIO(initial_advice)
        
    #     # Return StreamingResponse
    #     return StreamingResponse(advice_stream, media_type="text/plain")
    # except Exception as e: