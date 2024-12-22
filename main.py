from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from hi import get_red_financial_advice, get_yellow_financial_advice 

app = FastAPI()

# Global variables
savings = 0.0
income = 0.0
savings_amount = 0.0
fixed_expenses = 0.0
variable_expenses = 0.0
debts = []  # List to store credit card debts

net_income = 0.0
total_debt = 0.0
debt_repayment_capacity = 0.0
avalanche_method_result = []
snowball_method_result = []

# Define the model for each credit card debt, including the interest rate
class CreditCardDebt(BaseModel):
    card_name: str  # Credit card name or issuer
    debt_amount: float  # Debt amount for this card
    interest_rate: float  # Interest rate for this card (as a percentage)

class FinancialData(BaseModel):
    savings: float  # เงินเก็บ
    income: float  # รายได้
    savings_amount: float  # เงินออม
    fixed_expenses: Optional[float] = None  # Fixed รายจ่าย (optional)
    variable_expenses: Optional[float] = None  # Variable รายจ่าย (optional)
    debts: Optional[List[CreditCardDebt]] = None  # List of credit card debts with interest

# Snowball Method: Sort by debt amount (ascending order)
def snowball_method():
    debts_sorted_by_debt_amount = debts.copy()
    """
    Sort the global debts list by debt amount in ascending order (smallest debt first).
    """
    debts_sorted_by_debt_amount.sort(key=lambda x: x["debt_amount"])  # Sort by debt amount (ascending)
    return debts_sorted_by_debt_amount  # Return the sorted list (smallest debt first)

# Avalanche Method: Sort by interest rate (descending order)
def avalanche_method():
    debts_sorted_by_interest_rate = debts.copy()
    """
    Sort the global debts list by interest rate in descending order (highest interest first).
    """
    # global debts
    debts_sorted_by_interest_rate.sort(key=lambda x: x["interest_rate"], reverse=True)  # Sort by interest rate (descending)
    return debts_sorted_by_interest_rate  # Return the sorted list (highest interest rate first)

# Calculate Debt Repayment Capacity
def calculate_debt_repayment_capacity(debts: List[CreditCardDebt], net_income: float) -> float:
    """
    Calculate Debt Repayment Capacity as the total debt divided by income.
    """
    global total_debt
    if net_income == 0:
        return 0
    else:
        total_debt = sum(debt["debt_amount"] for debt in debts)
        return total_debt / net_income  # Debt Repayment Capacity = Total Debt / net_income

# Save all the relevant variables to a JSON file
def save_to_json_file():
    global savings, income, savings_amount, fixed_expenses, variable_expenses, debts, net_income, total_debt, debt_repayment_capacity, snowball_method_result, avalanche_method_result
    data = {
        "savings": savings,
        "income": income,
        "savings_amount": savings_amount,
        "fixed_expenses": fixed_expenses,
        "variable_expenses": variable_expenses,
        "debts": debts,
        "net_income": net_income,
        "total_debt": total_debt,
        "debt_repayment_capacity": debt_repayment_capacity,
        "snowball_method": snowball_method_result,
        "avalanche_method_result": avalanche_method_result
    }

    # Remove the existing JSON file before saving new data
    if os.path.exists("financial_data.json"):
        os.remove("financial_data.json")  # Remove the old file

    # Save the data to a new JSON file
    with open("financial_data.json", "w") as file:
        json.dump(data, file)

# Load data from JSON file and update global variables
def load_from_json_file():
    global savings, income, savings_amount, fixed_expenses, variable_expenses, debts, net_income, total_debt, debt_repayment_capacity, snowball_method_result, avalanche_method_result
    try:
        with open("financial_data.json", "r") as file:
            data = json.load(file)

        # Update global variables with values from the JSON file
        savings = data["savings"]
        income = data["income"]
        savings_amount = data["savings_amount"]
        fixed_expenses = data["fixed_expenses"]
        variable_expenses = data["variable_expenses"]
        debts = data["debts"]
        net_income = data["net_income"]
        total_debt = data["total_debt"]
        debt_repayment_capacity = data["debt_repayment_capacity"]
        snowball_method_result = data["snowball_method"]
        avalanche_method_result = data["avalanche_method_result"]
    except FileNotFoundError:
        return {"error": "Financial data file not found. Please submit financial data first."}


# Define the POST request endpoint to submit financial data
@app.post("/submit-financial-data/")
async def submit_financial_data(data: FinancialData):
    global savings, income, savings_amount, fixed_expenses, variable_expenses, debts

    # Assign values to global variables
    savings = data.savings
    income = data.income
    savings_amount = data.savings_amount
    fixed_expenses = data.fixed_expenses if data.fixed_expenses is not None else 0.0
    variable_expenses = data.variable_expenses if data.variable_expenses is not None else 0.0
    
    # If the user provided credit card debts, store them in the global variable
    if data.debts is not None:
        debts = [{"card_name": debt.card_name, "debt_amount": debt.debt_amount, "interest_rate": debt.interest_rate} for debt in data.debts]
    else:
        debts = []

    global snowball_method_result, avalanche_method_result
    # Run the Snowball Method and Avalanche Method, storing the results in variables
    snowball_method_result = snowball_method()  # Sort debts by debt amount (smallest first)
    avalanche_method_result = avalanche_method()  # Sort debts by interest rate (highest first)

    # Calculate Net Income and Debt Repayment Capacity
    global net_income, debt_repayment_capacity
    net_income = income - fixed_expenses - variable_expenses
    debt_repayment_capacity = calculate_debt_repayment_capacity(debts, net_income)

    print('debt_repayment_capacity: ', debt_repayment_capacity)

    if debt_repayment_capacity < 0.4:
        print("Good")
    elif debt_repayment_capacity >= 0.4 and debt_repayment_capacity < 0.8:
        print("Calm down")
    else:
        print("So Bad")

    # Save the global variables to a JSON file
    save_to_json_file()

    # Return a response with the sorted results stored in the variables
    return {
        "message": "Financial data received successfully",
        "net_income": net_income,
        "debt_repayment_capacity": debt_repayment_capacity,
        "snowball_method": snowball_method_result,  # Sorted by smallest debt first
        "avalanche_method": avalanche_method_result  # Sorted by highest interest first
    }


# Define the GET request endpoint to return global variables from the JSON file
# @app.get("/get-global-variables/")
# async def get_global_variables():
#     # Read the JSON file to get the global variables
#     try:
#         with open("financial_data.json", "r") as file:
#             data = json.load(file)
#         return data
#     except FileNotFoundError:
#         return {"error": "Financial data file not found. Please submit financial data first."}
    

# Define the GET request endpoint to return global variables from the JSON file
@app.get("/get-global-variables/")
async def get_global_variables():
    # Load data from the JSON file to update the global variables
    load_from_json_file()

    financial_data = {
    "income": income,
    "savings_amount": savings_amount,
    "fixed_expenses": fixed_expenses,
    "variable_expenses": variable_expenses,
    "debts": snowball_method_result
    }
# print(snowball_method_result)
    print('debt_repayment_capacity: ', debt_repayment_capacity)
    if debt_repayment_capacity < 0.4:
        print("Good")
    elif debt_repayment_capacity >= 0.4 and debt_repayment_capacity < 0.8:
        recommend = get_yellow_financial_advice(financial_data)
        print("Yello:") 
        print(recommend)

    else:
        recommend = get_red_financial_advice(financial_data)
        print("Red:")
        print(recommend)


    # Return the updated global variables
    return {
        "savings": savings,
        "income": income,
        "savings_amount": savings_amount,
        "fixed_expenses": fixed_expenses,
        "variable_expenses": variable_expenses,
        "debts": debts,
        "net_income": net_income,
        "total_debt": total_debt,
        "debt_repayment_capacity": debt_repayment_capacity,
        "snowball_method": snowball_method_result,
        "avalanche_method_result": avalanche_method_result
    }