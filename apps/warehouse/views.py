from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Color, Income
from warehouse.serializers import InventorySerializer, IncomeSerializer
from sales.views import MyPageNumberPagination
import django_filters
# Create your views here.


class InventoryFilter(django_filters.rest_framework.FilterSet):
    number = django_filters.CharFilter(field_name='product__clothe_num')
    class Meta:
        model = Color
        fields = ['number', 'color']

class InventoryView(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Color.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = InventoryFilter

class IncomeFilter(django_filters.rest_framework.FilterSet):
    number = django_filters.CharFilter(field_name='clothe_num')
    class Meta:
        model = Income
        fields = ['date', 'number','color']

class IncomeView(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = IncomeFilter