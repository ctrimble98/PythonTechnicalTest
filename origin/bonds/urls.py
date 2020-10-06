from django.urls import path

from .views import BondView


app_name = "bonds"

urlpatterns = [
    path('', BondView.as_view()),
]