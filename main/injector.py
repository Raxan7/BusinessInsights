from .models import Sales
import markdown
import google.generativeai as genai


GOOGLE_API_KEY = 'AIzaSyAX8YiDkmNyeLhCnGZOZ4Uq_2gJyXvatNs'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def Call(userMsg):
    monthly_sales = [i.amount for i in Sales.objects.all()]
    
    prompt = f"""**Input:**

    * List of monthly sales figures for the past year (can be all 12 months or a specific timeframe). Provide the data as a comma-separated list (e.g., 10000, 12000, 8000, ...).
    * Industry of the business (e.g., e-commerce, retail, software development).
    * Any relevant business goals or challenges mentioned by the manager during the chat (optional).

    **Task:**

    1. Analyze the provided monthly sales data to identify trends and patterns.
    2. Generate concise and insightful responses that offer business advice to the manager based on the analysis.
    3. Consider the manager's industry and any specific goals/challenges mentioned to tailor the advice.
    4. Maintain a professional and informative tone while keeping responses short and to the point.
    5. Find out *{userMsg}*

    **Examples of Insights:**

    * Identify months with significant sales growth or decline.
    * Suggest potential reasons for these trends (e.g., seasonality, marketing campaigns, competitor activity).
    * Recommend actions based on the analysis (e.g., adjust marketing strategies, optimize product offerings).
    * Provide relevant industry benchmarks or comparisons for context.

    **Output:**

    * Text responses delivered in a conversational style, offering actionable business advice based on the analyzed data and manager's context."""



    # Define the industry (optional)
    industry = "E-commerce"

    # Define any business goals/challenges (optional)
    goals_challenges = "Increase overall sales by 15% next quarter"  # Replace with actual goals

    # Construct the full prompt with data
    full_prompt = prompt + f"\n* Monthly Sales: {','.join(str(sale) for sale in monthly_sales)}"
    if industry:
        full_prompt += f"\n* Industry: {industry}"
    if goals_challenges:
        full_prompt += f"\n* Goals/Challenges: {goals_challenges}"

    # Generate response using Gemini API
    response = model.generate_content(full_prompt)
    # response = model.generate_content(prompt)
    # print(markdown.markdown(response.text))
    parsed_response = markdown.markdown(response.text)
    return parsed_response


import markdown

def is_valid_user_msg(userMsg):
    # Define criteria for valid userMsg. 
    # This example checks for specific keywords but can be expanded as needed.
    valid_keywords = ["analyze", "insights", "trends", "sales", "weekly", "recommendations", "business"]
    return any(keyword in userMsg.lower() for keyword in valid_keywords)

def CallWeekly(userMsg):
    # Validate the user message
    if not is_valid_user_msg(userMsg):
        return "The input message provided is invalid. Please provide a relevant message asking for sales analysis insights."

    # Fetch sales data from the database
    monthly_sales = [i.amount for i in Sales.objects.all()]

    # Validate the sales data
    if not monthly_sales or any(not isinstance(sale, (int, float)) for sale in monthly_sales):
        return "The sales data provided is invalid. Please provide a valid list of numeric sales figures."

    # Define the industry and goals/challenges (optional)
    industry = "E-commerce"
    goals_challenges = "Increase overall sales by 15%"  # Replace with actual goals

    # Construct the prompt
    prompt = f"""
    You are an AI providing business insights based on weekly sales data. 

    **Input:**
    * List of daily sales figures for the current week (comma-separated, e.g., 10000, 12000, 8000).
    * Industry of the business (e.g., e-commerce, retail, software development).
    * Any relevant business goals or challenges (optional).

    **Constraints:**
    1. Ensure the sales data is a list of numeric values.
    2. If the sales data is invalid or nonsensical, respond with "The sales data provided is invalid. Please provide a valid list of numeric sales figures."
    3. If the sales data is valid, proceed to analyze the data and generate business insights.

    **Task:**
    1. Analyze the provided weekly sales data to identify trends and patterns.
    2. Generate concise and insightful responses that offer business advice to the manager based on the analysis.
    3. Consider the manager's industry and any specific goals/challenges mentioned to tailor the advice.
    4. Maintain a professional and informative tone while keeping responses short and to the point.
    5. Find out *{userMsg}*

    **Output:**
    * Provide concise, professional insights and recommendations based on the analyzed data.
    """

    # Construct the full prompt with data
    full_prompt = prompt + f"\n* Weekly Sales: {', '.join(str(sale) for sale in monthly_sales)}"
    if industry:
        full_prompt += f"\n* Industry: {industry}"
    if goals_challenges:
        full_prompt += f"\n* Goals/Challenges: {goals_challenges}"

    try:
        # Generate response using Gemini API
        response = model.generate_content(full_prompt)
        parsed_response = markdown.markdown(response.text)
        return parsed_response
    except Exception as e:
        return f"An error occurred while generating insights: {e}"

# # Example usage
# user_message = "Analyze the sales data to provide insights on weekly trends."
# print(CallWeekly(user_message))




# def CallWeekly(userMsg):
#     monthly_sales = [i.amount for i in Sales.objects.all()]
    
#     prompt = f"""**Input:**

#     * List of daily sales figures for the current week (can be all 7 days or a specific timeframe). Provide the data as a comma-separated list (e.g., 10000, 12000, 8000, ...).
#     * Industry of the business (e.g., e-commerce, retail, software development).
#     * Any relevant business goals or challenges mentioned by the manager during the chat (optional).

#     **Task:**

#     1. Analyze the provided weekly sales data to identify trends and patterns.
#     2. Generate concise and insightful responses that offer business advice to the manager based on the analysis.
#     3. Consider the manager's industry and any specific goals/challenges mentioned to tailor the advice.
#     4. Maintain a professional and informative tone while keeping responses short and to the point.
#     5. Find out *{userMsg}*

#     **Examples of Insights:**

#     * Identify days with significant sales growth or decline.
#     * Suggest potential reasons for these trends (e.g., seasonality, marketing campaigns, competitor activity).
#     * Recommend actions based on the analysis (e.g., adjust marketing strategies, optimize product offerings).
#     * Provide relevant industry benchmarks or comparisons for context.

#     **Output:**

#     * Text responses delivered in a conversational style, offering actionable business advice based on the analyzed data and manager's context."""



#     # Define the industry (optional)
#     industry = "E-commerce"

#     # Define any business goals/challenges (optional)
#     goals_challenges = "Increase overall sales by 15%"  # Replace with actual goals

#     # Construct the full prompt with data
#     full_prompt = prompt + f"\n* Weekly Sales: {','.join(str(sale) for sale in monthly_sales)}"
#     if industry:
#         full_prompt += f"\n* Industry: {industry}"
#     if goals_challenges:
#         full_prompt += f"\n* Goals/Challenges: {goals_challenges}"

#     # Generate response using Gemini API
#     response = model.generate_content(full_prompt)
#     # response = model.generate_content(prompt)
#     # print(markdown.markdown(response.text))
#     parsed_response = markdown.markdown(response.text)
#     return parsed_response

