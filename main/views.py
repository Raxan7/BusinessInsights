from typing import Any
import markdown
from .forms import BusinessInsightForm

from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
import google.generativeai as genai

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import JsonResponse

from .forms import SalesDataForm
from .models import Sales
from .serializers import SalesSerializer
from .injector import *


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
    

def weekly_insights(request):
    context = {}
    return render(request, 'main/business_weekly.html', context)


def chat(request):
    return render(request, 'main/chat.html')


def GeminiAi(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        # print("Received data:", data)
        response = Call(data)
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


# Weekly

def GeminiAi_Weekly(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        # print("Received data:", data)
        response = CallWeekly(data)
        return JsonResponse({"message": response})
    return JsonResponse("Invalid")
