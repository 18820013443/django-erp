from dashboard.serializers import TotalSummarySerializer, PreviousSevenDaysRevenueSerializer\
    , PreviousSevenDaysOrdersCountSerializer, PreviousSevenDaysSalesCountSerializer,\
    PreviousHalfYearsMonthsRevenueSerializer, TopTenCustomersSerializer
from rest_framework.viewsets import ModelViewSet

from sales.models import OrdersHeader


# Create your views here.


class TotalSummaryView(ModelViewSet):
    serializer_class = TotalSummarySerializer
    queryset = OrdersHeader.objects.all()[:1]


class PreviousSevenDaysRevenueView(ModelViewSet):
    serializer_class = PreviousSevenDaysRevenueSerializer
    queryset = OrdersHeader.objects.all()[:1]


class PreviousSevenDaysOrdersCountView(ModelViewSet):
    serializer_class = PreviousSevenDaysOrdersCountSerializer
    queryset = OrdersHeader.objects.all()[:1]


class PreviousSevenDaysSalesCountView(ModelViewSet):
    serializer_class = PreviousSevenDaysSalesCountSerializer
    queryset = OrdersHeader.objects.all()[:1]


class PreviousHalfYearsMonthsRevenueView(ModelViewSet):
    serializer_class = PreviousHalfYearsMonthsRevenueSerializer
    queryset = OrdersHeader.objects.all()[:1]


class TopTenCustomersView(ModelViewSet):
    serializer_class = TopTenCustomersSerializer
    queryset = OrdersHeader.objects.all()[:1]
