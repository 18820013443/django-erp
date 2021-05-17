from django.urls import path,re_path
from warehouse.views import InventoryView,IncomeView

urlpatterns = [
    path('inventory/', InventoryView.as_view({'get':'list','post':'create'})),
    re_path(r'^inventory/(?P<pk>\d+)/$', InventoryView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    path('income/', IncomeView.as_view({'get':'list','post':'create'})),
    re_path(r'^income/(?P<pk>\d+)/$', IncomeView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
]