from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),  # перенаправляемся на единственное представление
    # IndexView, которое описано в соответствующем файле views.py
]
