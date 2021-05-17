from django.shortcuts import render
from sales.models import OrdersDetail, OrdersHeader
import xlwings as xw

# Create your views here.


def download_orders_view(request):
    wk = xw.Book()
    wk.sheets[0].name = "客户订单"
    lst_data = []
    orders_list = OrdersHeader.objects.all()
    for order in orders_list:
        pass
    pass
    



def generate_excel():
    pass