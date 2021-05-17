from .views import AuthView, UserView
from django.urls import path

urlpatterns = [
    path('login/', AuthView.as_view()),
    path('user/', UserView.as_view({'get':'list'})),
]