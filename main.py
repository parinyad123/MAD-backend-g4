from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
from chain import TwoPhaseFinancialAdvisor
from fastapi.responses import StreamingResponse
from io import StringIO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

def chatbot_process(data: dict, cluster: str):
    print(cluster)
    print(data)
    return f"Chatbot received the following data: {data} with cluster: {cluster}"

def load_json_to_dict(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        return data_dict
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        return {}

# POST request to save data to a JSON file
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

@app.get("/api/get_initial_advice/")
async def get_initial_advice():
    file_path = 'user_data.json'
    financial_data = load_json_to_dict(file_path)
    print(financial_data)
    advice_type = financial_data.get('cluster', 'unknown')
    print(advice_type)
    try:
        initial_advice = advisor.get_initial_advice(financial_data, advice_type)
        with open("initial_history.json", "w", encoding="utf-8") as json_file:
            json.dump({"advice": initial_advice}, json_file, ensure_ascii=False, indent=4)
        return {"advice": initial_advice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating advice: {str(e)}")

class UserInput(BaseModel):
    user_input: str

def load_initial_chat_history(file_path: str) -> List[dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            initial_history = json.load(file)
        return initial_history
    except Exception as e:
        print(f"Error reading initial chat history: {str(e)}")
        return []

def save_chat_history(file_path: str, chat_history: List[dict]) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(chat_history, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")

@app.post("/api/chats/")
async def chats(user_input: UserInput):
    print(user_input)
    if not user_input.user_input:
        raise HTTPException(status_code=400, detail="User input is required.")
    try:
        advisor.initial_advice = json.dumps(load_initial_chat_history('initial_history.json'))
        advisor.financial_data = load_json_to_dict('user_data.json')
        response = advisor.chat(user_input.user_input)
        return {
            "chatbot_response": response,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")
