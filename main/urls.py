from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('generate-insight', views.generate_insight, name='generate_insight'),
    path('chat/', views.chat, name="chat"),
    path('gemini/', views.GeminiAi, name="gemini-ai"),
]
