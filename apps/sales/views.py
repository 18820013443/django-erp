from django.shortcuts import render
from sales.serializers import OrderSerializer, CustomerSerializer, GoodsIssueSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from sales.models import OrdersHeader, Customers,OrdersDetail
import django_filters
from sales.filters import OrderFilter, CustomerFilter
from rest_framework.response import Response
from account.utils.auth import UserAuthentication

# Create your views here.

class MyPageNumberPagination(PageNumberPagination):
    page_size = 10 # 定义每页数据量的大小
    page_size_query_param = 'size' # 定义请求参数中size的关键字
    max_page_size = 50 # 定义每页中最大显示数据
    page_query_param = 'page'  # 定义请求参数中page的关键字

class OrdersView(viewsets.ModelViewSet):
    
    # authentication_classes = [UserAuthentication,]
    serializer_class = OrderSerializer
    queryset = OrdersHeader.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ['date','customer','number', 'issued_all']
    filter_class = OrderFilter

    # def create(self,request,*args,**kwargs):
    #     # print(kwargs.validated_data)
    #     ret = {'code':2000, 'msg':None}
    #     # 获取前端请求返回的数据
    #     data = request.data

    #     print(data)
    #     # 获取创建customer的数据
    #     # order_detail = data.pop('order_detail')
    #     # print(data)
    #     # 创建customer序列化器进行反序列化
    #     c_ser = CustomerSerializer(data=data)
    #     # # 调用序列化器方法is_valid()进行验证
    #     c_ser.is_valid(raise_exception=True)
    #     # 调用序列化器的save方法执行create方法
    #     # c_ser.save()
    #     print(c_ser.validated_data)
    #     order_detail = c_ser.validated_data.pop('order_detail')


    #     customer = Customers.objects.filter(name=data['name']).first()
    #     if not customer:
    #         customer = Customers.objects.create(name=data['name'],address=data['address'],phone=data['phone'])
    #     order_header = OrdersHeader.objects.create(customer=customer)

        
    #     for od in order_detail:
    #         OrdersDetail.objects.create(clothe_num=od['clothe_num'],color=od['color'],amount=od['amount'],price=od['price'],order_header=order_header)

    #     ret['msg'] = '订单创建成功'

    #     return Response(ret)
    


'''
    流程：
        1. 获取queryset
        2. 实例化分页器，获取页面queryset
        3. 将页面queryset序列化
'''

class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customers.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = CustomerFilter



class GoodsIssueView(viewsets.ModelViewSet):
    serializer_class = GoodsIssueSerializer
    queryset = OrdersHeader.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ['date','customer','number', 'issued_all']
    filter_class = OrderFilter

    # def update(self,request,*args,**kwargs):
    #     ret = {'code':2000, 'msg':""}
    #     data = request.data
    #     order_detail = data['order_detail']
    #     # print(data)
    #     pk = data['id']
    #     issue_flg = ""
    #     lst_pending_num = []
    #     order_header = OrdersHeader.objects.get(pk=pk)
    #     # order_detail_lst = order_header.ordersdetail_set.all()
    #     order_detail_lst = OrdersDetail.objects.filter(order_header_id=pk)
    #     print(order_detail_lst)
    #     for odl in order_detail_lst:
    #         for dic in order_detail:
    #             if odl.clothe_num == dic['clothe_num'] and odl.color == dic['color']:
    #                 odl.issued_num = dic['issued_num']
    #                 odl.pending_num = odl.amount - dic['issued_num']
    #                 lst_pending_num.append(odl.pending_num)
    #                 issue_flg += "success"
    #                 odl.save()
    #             else:
    #                 issue_flg += "fail"
    #     print(issue_flg)
    #     if "fail" in issue_flg:
    #         ret['msg'] = "订单发货失败"
    #     else:
    #         ret['msg'] = "订单发货成功"
    #     if len(set(lst_pending_num)) == 1 and lst_pending_num[0] == 0:
    #         order_header.issued_all = True
    #         order_header.issued_partial = False
    #         order_header.save()
    #     else:
    #         order_header.issued_all = False
    #         order_header.issued_partial = True
    #         order_header.save()

    #     return Response(ret)
    