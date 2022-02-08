from django.db.models import fields
import django_filters
from sales.models import OrdersHeader, Customers

class OrderFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFilter(field_name='order_date')
    date_lte = django_filters.DateFilter(field_name='order_date', lookup_expr='lte')
    date_gte = django_filters.DateFilter(field_name='order_date', lookup_expr='gte')
    issued_all = django_filters.BooleanFilter(field_name='issued_all')
    # number = django_filters.CharFilter(field_name='ordersheader__ordersdetail__clothe_num')
    customer = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    class Meta:
        model = OrdersHeader
        # fields = ['date','customer','number', 'issued_all']
        fields = ['date','customer', 'issued_all']


class CustomerFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='startswith')
    class Meta:
        model = Customers
        fields = ['name','address','phone']