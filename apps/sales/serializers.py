from django.db.models import fields
from sales.models import Customers, OrdersHeader, OrdersDetail
from rest_framework import serializers
from warehouse.models import Color

class OrderDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrdersDetail
        exclude = ['issued_num', 'pending_num']

class OrderDetailIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersDetail
        exclude = ['price','total_price']


class OrderSerializer(serializers.ModelSerializer):
    # customers
    name = serializers.CharField(source='customer.name')
    phone = serializers.CharField(source='customer.phone')
    address = serializers.CharField(source='customer.address')
    
    # order detail
    # order = serializers.SerializerMethodField()
    order_detail = OrderDetailSerializer(many=True,read_only=False,source='ordersdetail_set')


    class Meta:
        model = OrdersHeader
        fields = ['id','order_date','order_num','name','phone','address','order_detail','order_price','issued_all']

    
    def create(self, validated_data):
        print(validated_data)
        order_details = validated_data.pop('ordersdetail_set')
        # print(validated_data)
        validated_data = validated_data.get('customer')
        customer = Customers.objects.filter(name=validated_data['name']).first()
        if not customer:
            customer = Customers.objects.create(**validated_data)
        order_header = OrdersHeader.objects.create(customer=customer)
        # print(order_details)
        for order_detail in order_details:
            OrdersDetail.objects.create(order_header=order_header,**order_detail)
        return order_header

    def update(self, instance, validated_data):
        print(validated_data)
        order_detail = validated_data.pop('ordersdetail_set')
        customer = validated_data.pop('customer')
        # order_header = validated_data.pop('order_header')
        order_detail_lst = OrdersDetail.objects.filter(order_header=instance)
        instance.customer.name = customer['name']
        instance.customer.phone = customer['phone']
        instance.customer.address = customer['address']
        instance.customer.save()
        # instance.customer.update(**customer)
        # instance.update(**order_header)
        order_detail_lst = OrdersDetail.objects.filter(order_header=instance)
        for odl in order_detail_lst:
            for dic in order_detail:
                if odl.clothe_num == dic['clothe_num'] and odl.color == dic['color']:
                    odl.clothe_num = dic['clothe_num']
                    odl.color = dic['color']
                    odl.amount = dic['amount']
                    odl.price = dic['price']
                    # odl.issued_num = dic['issued_num']
                    # odl.pending_num = odl.amount - dic['issued_num']
                    odl.save()
        return instance

            
class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customers
        fields = '__all__'

# class DeliverSerializers(serializers.ModelSerializer):
    
#     class Meta:
#         model = DeliverGoods
#         fields = '__all__'
    
class GoodsIssueSerializer(serializers.ModelSerializer):

    # customers
    name = serializers.CharField(source='customer.name')
    phone = serializers.CharField(source='customer.phone')
    address = serializers.CharField(source='customer.address')

    order_detail = OrderDetailIssueSerializer(many=True,read_only=False,source='ordersdetail_set')
    # order_detail = OrderDetailIssueSerializer(required=True)

    class Meta:
        model = OrdersHeader
        fields = ['id','order_date','order_num','name','phone','address','order_detail','issued_all','issued_partial']

    def update(self, instance, validated_data):
        order_detail = validated_data.pop('ordersdetail_set')
        issue_flg = ""
        lst_pending_num = []
        order_detail_lst = OrdersDetail.objects.filter(order_header=instance)
        for odl in order_detail_lst:
            for dic in order_detail:
                if odl.clothe_num == dic['clothe_num'] and odl.color == dic['color']:
                    pre_issued_num = odl.issued_num
                    odl.issued_num = dic['issued_num']
                    odl.pending_num = odl.amount - dic['issued_num']
                    # 减少库存数量
                    p = Color.objects.filter(product__clothe_num=dic['clothe_num'],color=dic['color']).first()
                    p.amount = p.amount + pre_issued_num - dic['issued_num']
                    # p.amount -= dic['issued_num']
                    print(p.amount)
                    if p.amount < 0:
                        odl.issued_num = p.amount
                    p.save()
                    # 减少库存数量
                    lst_pending_num.append(odl.pending_num)
                    issue_flg += "success"
                    odl.save()
                else:
                    issue_flg += "fail"
        print(issue_flg)
        if len(set(lst_pending_num)) == 1 and lst_pending_num[0] == 0:
            instance.issued_all = True
            instance.issued_partial = False
            instance.save()
        else:
            instance.issued_all = False
            instance.issued_partial = True
            instance.save()
        return instance



