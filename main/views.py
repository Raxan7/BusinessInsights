from typing import Any
import markdown
import google.generativeai as genai
from .forms import BusinessInsightForm

from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
import google.generativeai as genai

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse

from .forms import SalesDataForm
from .models import Sales
from .serializers import SalesSerializer

GOOGLE_API_KEY = 'AIzaSyAX8YiDkmNyeLhCnGZOZ4Uq_2gJyXvatNs'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


def generate_insight(request):
    if request.method == 'POST':
        form = BusinessInsightForm(request.POST)
        if form.is_valid():
            # form.save()
            return redirect("main:dashboard")
    else:
        form = BusinessInsightForm()
    return render(request, 'main/business_insight.html', {'form': form})


# def dashboard(request):
#     data = Sales.objects.all()
#     return render(request, 'main/business_dashboard.html')


class DashboardView(TemplateView):
    template_name = 'main/business_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = [
            {
                'amount': obj.amount,
                'month': obj.date.month,
            }
            for obj in Sales.objects.all()
        ]
        return context


def GoogleApiCall(userMsg):
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


def chat(request):
    return render(request, 'main/chat.html')


def GeminiAi(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        # print("Received data:", data)
        response = GoogleApiCall(data)
        return JsonResponse({"message": response})
    return JsonResponse("Invalid")


def enter_data_view(request):
    if request.method == "POST":
        form = SalesDataForm(request.POST)
        form.save()
        return redirect('main:enter_sales_data')
    else:
        form = SalesDataForm()
    context = {
        'form': form,
    }
    return render(request, "main/enter_data.html", context)
