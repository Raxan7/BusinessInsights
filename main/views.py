import markdown
import google.generativeai as genai
from .forms import BusinessInsightForm

from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os

from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse

GOOGLE_API_KEY = 'AIzaSyAX8YiDkmNyeLhCnGZOZ4Uq_2gJyXvatNs'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def generate_insight(request):
    if request.method == 'POST':
        form = BusinessInsightForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country']

            genai.configure(api_key="AIzaSyAX8YiDkmNyeLhCnGZOZ4Uq_2gJyXvatNs")
            model = genai.GenerativeModel('gemini-pro')

            response = model.generate_content(f"Analyze social media conversations from the past month mentioning "
                                              f"Nike SHoes in {country}. Include sentiment analysis and identify "
                                              f"keywords related to sales decline, product issues, or customer "
                                              f"complaints. Additionally, identify any mentions of alternative "
                                              f"products or brands.")
            insight = markdown.markdown(response.text)

            return render(request, 'main/business_insight.html', {'form': form, 'insight': insight})
    else:
        form = BusinessInsightForm()
    return render(request, 'main/business_insight.html', {'form': form})


def dashboard(request):
    return render(request, 'main/business_dashboard.html')


def GoogleApiCall(userMsg):
    # Craft your prompt here
    response = model.generate_content(f"Analyze social media conversations from the past month mentioning "
                                      f"Nike SHoes in Tanzania. Include sentiment analysis and identify "
                                      f"keywords related to sales decline, product issues, or customer "
                                      f"complaints. Additionally, identify any mentions of alternative "
                                      f"products or brands.")
    prompt = (f"I want all the answers to be tailored to this response {response.text}, but in case what you are "
              f"asked is not in the provided response, then you are free to get your own custom responses. "
              f"And if you are asked what the customers are saying, always take it from a social media perspective "
              f"that is the user wants the social media comments"
              f"But make the "
              f"responses short and easy for the user to interact with: {userMsg}")
    response = model.generate_content(prompt)
    return response.text


def chat(request):
    return render(request, 'main/chat.html')


def GeminiAi(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        # print("Received data:", data)
        response = GoogleApiCall(data)
        return JsonResponse({"message": response})
    return JsonResponse("Invalid")
