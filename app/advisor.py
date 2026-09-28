import os

def build_prompt(income, expenses, savings_goal=0):
    total_income = sum(x["amount"] for x in income)
    total_expenses = sum(x["amount"] for x in expenses)
    savings = total_income - total_expenses
    return f"""
You are a personal finance assistant. Give practical, non-judgmental educational guidance.
Income: ₹{total_income:.2f}
Expenses: ₹{total_expenses:.2f}
Current surplus: ₹{savings:.2f}
Savings goal: ₹{savings_goal:.2f}
Expense categories: {expenses}
Return:
1. A simple budget suggestion.
2. Three spending observations.
3. Three savings actions.
4. One emergency-fund suggestion.
Avoid guarantees and risky investment recommendations.
""".strip()

def get_advice(income, expenses, savings_goal=0):
    # Optional Gemini integration. The app remains usable without an API key.
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                contents=build_prompt(income, expenses, savings_goal)
            )
            if response.text:
                return response.text
        except Exception:
            pass

    total_income = sum(x["amount"] for x in income)
    total_expenses = sum(x["amount"] for x in expenses)
    surplus = total_income - total_expenses
    if total_income <= 0:
        return "Add your income first so the advisor can generate a personalized budget."
    ratio = total_expenses / total_income
    if ratio > 0.8:
        level = "Your current spending is relatively high compared with your income."
    elif ratio > 0.5:
        level = "Your spending is moderate; review the largest categories regularly."
    else:
        level = "Your current spending leaves a useful surplus for savings or goals."

    categories = {}
    for e in expenses:
        categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]
    top = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
    top_text = ", ".join(f"{k} (₹{v:.0f})" for k, v in top) or "No expenses recorded"

    return f"""### Personal Finance Advisor

**Summary:** Income ₹{total_income:.0f} | Expenses ₹{total_expenses:.0f} | Surplus ₹{surplus:.0f}

**Budget suggestion**
- Essentials: about 50–60%
- Wants: about 20–30%
- Savings/goals: about 20% or more when practical

**Spending analysis**
- {level}
- Largest recorded categories: {top_text}
- Review recurring or non-essential expenses before increasing discretionary spending.

**Savings actions**
1. Set a fixed monthly savings target.
2. Keep an emergency fund goal and build it gradually.
3. Review your dashboard at the end of each month.

*Educational guidance only; not financial advice or a guarantee of returns.*
"""
