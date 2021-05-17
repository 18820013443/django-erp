from django.urls import path,re_path
from documents.views import download_orders_view

urlpatterns = [
    path('orders_download/', download_orders_view),
]