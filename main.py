from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from typing import Dict, Optional
import json
from openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI

openai_client = OpenAI(
    api_key=""
)

def get_red_financial_advice(financial_data: Dict) -> str:
    """Get red financial advice focusing on refinancing and debt management"""
    system_prompt = """You are a professional financial advisor in Thailand. Analyze financial situations and provide recommendations in JSON format. Focus on refinancing opportunities and debt management. All monetary values should be in Thai Baht (฿), numbers only without currency symbol in JSON. Round percentages to 2 decimal places.

    For the advisoryMessage in Thai:
    - Start with a friendly, personalized greeting
    - Summarize their current financial situation (using ฿)
    - Explain the key metrics and what they mean
    - Detail why refinancing is or isn't recommended
    - Provide step-by-step action items
    - Include timeline expectations
    - Add words of encouragement
    - Close with an offer for further assistance
    """

    prompt = f"""Analyze these credit cards for optimal payoff strategies:
    Monthly Income: ฿{financial_data['income']}
    Current Savings: ฿{financial_data['saving']}
    Fixed Monthly Expenses: ฿{financial_data['fixed_expense']}
    Variable Monthly Expenses: ฿{financial_data['variable_expense']}
    Total Debt: ฿{financial_data['total_debt']}
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
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

def get_yellow_financial_advice(financial_data: Dict) -> str:
    """Get yellow financial advice focusing on credit card optimization"""
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
    Current Savings: ฿{financial_data['saving']}
    Fixed Monthly Expenses: ฿{financial_data['fixed_expense']}
    Variable Monthly Expenses: ฿{financial_data['variable_expense']}
    Total Debt: ฿{financial_data['total_debt']}
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
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

class TwoPhaseFinancialAdvisor:
    def __init__(self):
        self.api_key = ""
        
        self.client = ChatOpenAI(
            openai_api_key=self.api_key,
            model="gpt-3.5-turbo",
            temperature=0.2
        )
        
        #ใช่ conversational sum memory 
        # explicitly make the chat be seperate key 
        self.memory = ConversationSummaryBufferMemory(
            llm=self.client,
            memory_key="chat_history",
            input_key="human_input",     
            output_key="ai_response",   
            max_token_limit=5000,
            return_messages=True
        )
        
        self.initial_advice = None
        self.advice_type = None
        self.financial_data = None
        self.important_context = {}

    def get_initial_advice(self, financial_data: Dict, advice_type: str) -> str:
        """Get initial red or yellow advice and extract important context"""
        self.financial_data = financial_data
        self.advice_type = advice_type.lower()
        
        if self.advice_type == "red":
            response = get_red_financial_advice(financial_data)
        else:  
            response = get_yellow_financial_advice(financial_data)
            
        self.initial_advice = response
        self._extract_important_context(response)
        return response

    def _extract_important_context(self, advice: str) -> None:
        """Extract and store important context from the initial advice"""
        try:
            advice_data = json.loads(advice)
            
            if self.advice_type == "red":
                self.important_context = {
                    "financial_metrics": advice_data.get("financial_metrics", {}),
                    "refinance_plan": advice_data.get("refinance_plan", {}).get("should_refinance"),
                    "monthly_targets": advice_data.get("action_steps", {}).get("monthly_targets", {})
                }
            else:  
                self.important_context = {
                    "available_for_debt_payment": advice_data.get("available_for_debt_payment"),
                    "recommended_strategy": advice_data.get("recommended_strategy", {}).get("method"),
                    "total_payoff_months": advice_data.get("recommended_strategy", {}).get("faster_payoff_option", {}).get("months_saved")
                }
        except json.JSONDecodeError:
            self.important_context = {"raw_advice": advice}

    def initialize_conversation_agent(self, human_input) -> LLMChain:
        """Initialize the conversation agent with summarized context"""
        #system_template = "You are a Thai financial advisor chatbot. Here's the essential context:  Financial Profile: {{financial_summary}} Key Points from {{advice_type}} Advice: {{important_context}}  Recent Conversation: {{chat_history}} Provide responses that: 1. Are consistent with the initial financial advice 2. Focus on practical, actionable guidance 3. Use Thai language (unless asked for English) 4. Reference specific numbers and recommendations from the initial advice when relevant"
         

        system_template = (
            f"""You are a Thai financial advisor chatbot. Here's the essential context:
            Financial Profile: {self.financial_summary}
            Key Points from {self.advice_type} Advice: {self.important_context}
            Provide responses that are consistent with the initial financial advice, 
            focus on practical, actionable guidance, use Thai language (unless asked for English), 
            and reference specific numbers and recommendations."""
        )

        conversation_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content=human_input),
        ])

        

        return LLMChain(
            llm=self.client,
            prompt=conversation_prompt,
            memory=self.memory,
            output_key="ai_response",   
            verbose=True
        )

    def chat(self, user_input: str) -> str:
        """Handle ongoing conversation with summarized context"""
        
        self.financial_summary = self._create_financial_summary()
        
        self.important_context = json.dumps(self.important_context, indent=2, ensure_ascii=False)
        
        conversation_agent = self.initialize_conversation_agent(user_input)
        

        #print initialize conversation agent 
        response = conversation_agent.run(
        
        human_input=user_input,  
        financial_summary=self.financial_summary,  
        advice_type=self.advice_type,  
        important_context=self.important_context,  
        chat_history=self.memory.chat_memory,  
    )

        
        return response  
    
    def _create_financial_summary(self) -> str:
        """Create a concise summary of financial data"""
        data = self.financial_data
        total_debt = sum(debt['debt_amount'] for debt in data['debts'])
        disposable_income = data['income'] - data['fixed_expenses'] - data['variable_expenses']
        
        summary = f"""
        Monthly Income: ฿{data['income']}
        Disposable Income: ฿{disposable_income}
        Total Debt: ฿{total_debt}
        Debt-to-Income Ratio: {(total_debt / data['income']):.2f}
        """
        return summary
    

def main():
    financial_data = {
        "income": 5000,
        "savings_amount": 10000,
        "fixed_expenses": 2000,
        "variable_expenses": 1000,
        "debts": [
            {
                "card_name": "MasterCard",
                "debt_amount": 4500,
                "interest_rate": 18.0
            },
            {
                "card_name": "Visa",
                "debt_amount": 3000,
                "interest_rate": 15.5
            },
            {
                "card_name": "American Express",
                "debt_amount": 7000,
                "interest_rate": 20.0
            }
        ]
    }

    advisor = TwoPhaseFinancialAdvisor()
    
    advice_type = input("Choose advice type (red/yellow): ").lower()
    initial_advice = advisor.get_initial_advice(financial_data, advice_type)
    # print(f"\nInitial {advice_type.upper()} Advice:")
    # print(initial_advice)
 
    
    # print("\nNow you can chat with the advisor. The advisor will maintain context from the initial advice.")
    while True:
        user_input = input("\nAsk a question (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
            
        response = advisor.chat(user_input)
        print("\nAdvisor Response:")
        print(response)

if __name__ == "__main__":
    main()