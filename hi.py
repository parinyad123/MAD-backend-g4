import openai
from openai import OpenAI

client = OpenAI(
    api_key=""
)

def get_red_financial_advice(financial_data):
    system_prompt = """You are a professional financial advisor in Thailand. Analyze financial situations and provide recommendations in JSON format. Focus on refinancing opportunities and debt management. All monetary values should be in Thai Baht (฿), numbers only without currency symbol in JSON. Round percentages to 2 decimal places.

For the advisoryMessage in Thai:
- Start with a friendly, personalized greeting
- Summarize their current financial situation (using ฿ for currency)
- Explain the key metrics and what they mean
- Detail why refinancing is or isn't recommended
- Provide step-by-step action items
- Include timeline expectations
- Add words of encouragement
- Close with an offer for further assistance
"""

    prompt = f"""Analyze these credit cards for optimal payoff strategies:
Monthly Income: ฿{financial_data['income']}
Current Savings: ฿{financial_data['savings_amount']}
Fixed Monthly Expenses: ฿{financial_data['fixed_expenses']}
Variable Monthly Expenses: ฿{financial_data['variable_expenses']}
Credit Cards:
{financial_data['debts']}

Provide financial advice in this exact JSON structure:
{{
    "financial_metrics": {{
        "disposable_income": (number in Baht),
        "debt_to_income_ratio": (number),
        "monthly_cash_flow": (number in Baht)
    }},
    "refinance_plan": {{
        "should_refinance": (boolean),
        "reasons": [(string in Thai)],
        "estimated_savings": (number in Baht)
    }},
    "action_steps": {{
        "immediate": [(string in Thai)],
        "monthly_targets": {{
            "debt_payment": (number in Baht),
            "savings": (number in Baht)
        }}
    }},
    "advisoryMessage": (comprehensive message in Thai following this structure:
        - คำทักทาย: Friendly greeting
        - สถานะการเงินปัจจุบัน: Current financial status summary (use ฿)
        - การวิเคราะห์: Analysis of their situation
        - แผนการชำระหนี้: Debt payment plan
        - คำแนะนำเพิ่มเติม: Additional recommendations
        - กำลังใจ: Words of encouragement
        - ข้อเสนอความช่วยเหลือ: Offer for further assistance)
}}"""

    try:
        response = client.chat.completions.create(  
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.2
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        return f"Error generating response: {str(e)}"


def get_yellow_financial_advice(financial_data):
    system_prompt = """You are a financial advisor in Thailand specializing in credit card debt optimization. Analyze each credit card debt separately and provide two payoff strategies: by card balance (smallest to largest) and by interest rate (highest to lowest). Calculate specific timelines for each card. All monetary values should be in Thai Baht (฿), numbers only without currency symbol in JSON.

For the advisoryMessage in Thai:
- Start with a warm, professional greeting
- Summarize total debt situation across all cards (using ฿)
- Explain both strategic approaches (balance-based vs interest-based)
- Detail the recommended strategy with clear reasoning
- Provide monthly payment recommendations
- Include specific timeline for becoming debt-free
- Add motivational encouragement
- Close with offer for additional guidance
"""

    prompt = f"""Analyze these credit cards for optimal payoff strategies:
Monthly Income: ฿{financial_data['income']}
Current Savings: ฿{financial_data['savings_amount']}
Fixed Monthly Expenses: ฿{financial_data['fixed_expenses']}
Variable Monthly Expenses: ฿{financial_data['variable_expenses']}
Credit Cards:
{financial_data['debts']}

Provide credit card specific payoff strategies in this JSON structure:
{{
    "available_for_debt_payment": (number in Baht),
    "credit_card_analysis": [{{
        "card_name": (string),
        "debt_amount": (number in Baht),
        "interest_rate": (number),
        "monthly_interest": (number in Baht)
    }}],
    "balance_based_strategy": {{
        "order": [{{
            "priority": (number),
            "card_name": (string),
            "months_to_payoff": (number),
            "monthly_payment": (number in Baht),
            "total_interest_paid": (number in Baht)
        }}],
        "total_payoff_months": (number),
        "total_interest_paid": (number in Baht)
    }},
    "interest_based_strategy": {{
        "order": [{{
            "priority": (number),
            "card_name": (string),
            "months_to_payoff": (number),
            "monthly_payment": (number in Baht),
            "total_interest_paid": (number in Baht)
        }}],
        "total_payoff_months": (number),
        "total_interest_paid": (number in Baht)
    }},
    "recommended_strategy": {{
        "method": (string in Thai),
        "reason": (string in Thai),
        "faster_payoff_option": {{
            "monthly_payment": (number in Baht),
            "months_saved": (number),
            "additional_interest_saved": (number in Baht)
        }},
        "longer_payoff_option": {{
            "monthly_payment": (number in Baht),
            "additional_months": (number),
            "extra_interest_cost": (number in Baht)
        }}
    }},
    "advisoryMessage": (comprehensive message in Thai following this structure:
        - คำทักทาย: Warm greeting
        - ภาพรวมหนี้บัตรเครดิต: Credit card debt overview (use ฿)
        - การวิเคราะห์กลยุทธ์: Analysis of both strategies
        - แผนที่แนะนำ: Recommended strategy explanation
        - แผนการชำระรายเดือน: Monthly payment plan
        - ระยะเวลาการปลดหนี้: Timeline to become debt-free
        - คำแนะนำเพิ่มเติม: Additional advice
        - กำลังใจ: Encouragement
        - ข้อเสนอความช่วยเหลือ: Offer for further assistance)
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.2
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        return f"Error generating response: {str(e)}"

# financial_data = {
#     "income": 5000,
#     "savings_amount": 10000,
#     "fixed_expenses": 2000,
#     "variable_expenses": 1000,
#     "debts": [
#         {
#             "card_name": "MasterCard",
#             "debt_amount": 4500,
#             "interest_rate": 18.0
#         },
#         {
#             "card_name": "Visa",
#             "debt_amount": 3000,
#             "interest_rate": 15.5
#         },
#         {
#             "card_name": "American Express",
#             "debt_amount": 7000,
#             "interest_rate": 20.0
#         }
#     ]
# }

# red_advice = get_red_financial_advice(financial_data)
# yellow_advice = get_yellow_financial_advice(financial_data)

# print("Red Alert Advice:")
# print(red_advice)
# print("\nYellow Alert Advice:")
# print(yellow_advice)