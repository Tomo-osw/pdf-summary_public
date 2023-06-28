from django.urls import path
from . import views

app_name = 'pdfs'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('result/', views.ResultView.as_view(), name="result"),
]
