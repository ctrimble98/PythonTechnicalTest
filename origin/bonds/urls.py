from django.urls import path

from .views import BondView


app_name = "bonds"

urlpatterns = [
    path('bonds/', BondView.as_view()),
]