from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesViewSet

router = DefaultRouter()
router.register(r'sales', SalesViewSet)

app_name = "main"
urlpatterns = [
    path('api/', include(router.urls)),

    path('yearly-insights', views.DashboardView.as_view(), name='dashboard'),
    path('generate-insight', views.generate_insight, name='generate_insight'),
    path('chat/', views.chat, name="chat"),
    
    path('gemini/', views.GeminiAi, name="gemini-ai"),
    path('gemini-weekly/', views.GeminiAi_Weekly, name="gemini-ai"),
    
    path('enter_sales_data/', views.enter_data_view, name='enter_sales_data'),

    path('', views.weekly_insights, name='weekly_insights')
]
