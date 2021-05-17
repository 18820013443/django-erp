from django.urls import path,re_path
from sales.views import OrdersView, CustomerView, GoodsIssueView

urlpatterns = [
    re_path(r'^orders/$', OrdersView.as_view({'get':'list','post':'create'})),
    re_path(r'^orders/(?P<pk>\d+)/$', OrdersView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    re_path(r'^customers/$', CustomerView.as_view({'get':'list','post':'create'})),
    re_path(r'^customers/(?P<pk>\d+)/$',CustomerView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    re_path(r'^orders/issued/$', GoodsIssueView.as_view({'get':'list','post':'create'})),
    re_path(r'^orders/issued/(?P<pk>\d+)/$', GoodsIssueView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
]