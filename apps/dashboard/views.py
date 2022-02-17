from dashboard.serializers import TotalSummarySerializer, PreviousSevenDaysRevenueSerializer\
    , PreviousSevenDaysOrdersCountSerializer, PreviousSevenDaysSalesCountSerializer,\
    PreviousHalfYearsMonthsRevenueSerializer, TopTenCustomersSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from sales.models import OrdersHeader


# Create your views here.


# class TotalSummaryView(ModelViewSet):
#     serializer_class = TotalSummarySerializer
#     queryset = OrdersHeader.objects.all()[:1]
#
#     def list(self, request, *args, **kwargs):
#         qs = OrdersHeader.objects.all().first()
#         serializer = TotalSummarySerializer(instance=qs)
#         return Response(serializer.data)

class TotalSummaryView(APIView):

    def get(self, request):
        qs = OrdersHeader.objects.all().first()
        serializer = TotalSummarySerializer(instance=qs)
        return Response(serializer.data)


# class PreviousSevenDaysRevenueView(ModelViewSet):
#     serializer_class = PreviousSevenDaysRevenueSerializer
#     queryset = OrdersHeader.objects.all()[:1]

class PreviousSevenDaysRevenueView(APIView):
    def get(self, request):
        qs = OrdersHeader.objects.all().first()
        serializer = PreviousSevenDaysRevenueSerializer(instance=qs)
        return Response(serializer.data)


# class PreviousSevenDaysOrdersCountView(ModelViewSet):
#     serializer_class = PreviousSevenDaysOrdersCountSerializer
#     queryset = OrdersHeader.objects.all()[:1]

class PreviousSevenDaysOrdersCountView(APIView):
    def get(self, request):
        qs = OrdersHeader.objects.all().first()
        serializer = PreviousSevenDaysOrdersCountSerializer(instance=qs)
        return Response(serializer.data)


# class PreviousSevenDaysSalesCountView(ModelViewSet):
#     serializer_class = PreviousSevenDaysSalesCountSerializer
#     queryset = OrdersHeader.objects.all()[:1]

class PreviousSevenDaysSalesCountView(APIView):
    def get(self, request):
        qs = OrdersHeader.objects.all().first()
        serializer = PreviousSevenDaysSalesCountSerializer(instance=qs)
        return Response(serializer.data)


# class PreviousHalfYearsMonthsRevenueView(ModelViewSet):
#     serializer_class = PreviousHalfYearsMonthsRevenueSerializer
#     queryset = OrdersHeader.objects.all()[:1]

class PreviousHalfYearsMonthsRevenueView(APIView):
    def get(self, request):
        qs = OrdersHeader.objects.all().first()
        serializer = PreviousHalfYearsMonthsRevenueSerializer(instance=qs)
        return Response(serializer.data)


# class TopTenCustomersView(ModelViewSet):
#     serializer_class = TopTenCustomersSerializer
#     queryset = OrdersHeader.objects.all()[:1]

class TopTenCustomersView(APIView):
    def get(self, request):
        qs = OrdersHeader.objects.all().first()
        serializer = TopTenCustomersSerializer(instance=qs)
        return Response(serializer.data)
