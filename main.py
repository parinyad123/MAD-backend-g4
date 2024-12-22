from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from chain import TwoPhaseFinancialAdvisor
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# import json
from io import StringIO

app = FastAPI()

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
    debt_amount: float

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

    
    try:
        # global initial_advice
        initial_advice = advisor.get_initial_advice(financial_data, advice_type)
        # Get the initial advice
        with open("initial_history.json", "w", encoding="utf-8") as json_file:
            json.dump({"advice": initial_advice}, json_file, ensure_ascii=False, indent=4)
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
    # POST request to handle ongoing conversation and keep chat history

# Define the Pydantic model for user input
class UserInput(BaseModel):
    user_input: str

# Function to load initial chat history from the provided JSON file
def load_initial_chat_history(file_path: str) -> List[dict]:
    """Load initial chat history from a JSON file and return it as a list of messages."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            initial_history = json.load(file)  # Read JSON file into a list
        return initial_history
    except Exception as e:
        print(f"Error reading initial chat history: {str(e)}")
        return []

# Function to save chat history back to the JSON file
def save_chat_history(file_path: str, chat_history: List[dict]) -> None:
    """Save the updated chat history to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(chat_history, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")

# POST request to handle ongoing conversation and keep chat history
@app.post("/api/chats/")
async def chats(user_input: UserInput):
    print(user_input)
    """Handle ongoing conversation with the chatbot and keep chat history"""

    
    # Ensure the user input is provided
    if not user_input.user_input:
        raise HTTPException(status_code=400, detail="User input is required.")
    
    try:
        # Load the initial chat history from a file
        # initial_history_file_path = 'initial_history.json'  # Path to the initial chat history JSON file
        # initial_history = load_initial_chat_history(initial_history_file_path)

        # print(initial_history)
        
        # # Start the conversation history with the initial chat history
        # conversation_history = initial_history
        
        # Pass the user input to the `chat` method of the advisor and get the response
        advisor.initial_advice = json.dumps(load_initial_chat_history('initial_history.json'))
        advisor.financial_data = load_json_to_dict('user_data.json')
        response = advisor.chat(user_input.user_input)
        
        # Extract the updated chat history (including initial history and new message)
        # chat_history = advisor.memory.chat_memory
        
        # Combine the initial history with the ongoing conversation
        # chat_history_combined = conversation_history + chat_history
        
        # Save the updated chat history back to the file
        # save_chat_history(initial_history_file_path, chat_history_combined)
        
        # Return the chatbot's response and the updated chat history
        return {
            "chatbot_response": response,
            # "chat_history": chat_history_combined
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")