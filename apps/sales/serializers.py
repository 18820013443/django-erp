from django.db.models import fields
from sales.models import Customers, OrdersHeader, OrdersDetail
from rest_framework import serializers
from warehouse.models import Color


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersDetail
        exclude = ['issued_num', 'pending_num']


class OrderDetailIssueSerializer(serializers.ModelSerializer):
    inventory_num = serializers.SerializerMethodField()
    class Meta:
        model = OrdersDetail
        exclude = ['price', 'total_price']

    def get_inventory_num(self, obj):
        inventory_num = 0
        inventory_num_lst = Color.objects.filter(product__clothe_num=obj.clothe_num, color=obj.color)
        if len(inventory_num_lst) > 0:
            inventory_num = inventory_num_lst[0].amount
        return inventory_num


class OrderSerializer(serializers.ModelSerializer):
    # customers
    name = serializers.CharField(source='customer.name')
    phone = serializers.CharField(source='customer.phone')
    address = serializers.CharField(source='customer.address')

    # order detail
    # order = serializers.SerializerMethodField()
    order_detail = OrderDetailSerializer(many=True, read_only=False, source='ordersdetail_set')


    class Meta:
        model = OrdersHeader
        fields = ['id', 'order_date', 'order_num', 'name', 'phone', 'address', 'order_detail', 'order_price',
                  'issued_all']

    def create(self, validated_data):
        # print(validated_data)
        order_details = validated_data.pop('ordersdetail_set')
        # print(validated_data)
        order_date = validated_data.pop('order_date')
        validated_data = validated_data.get('customer')
        customer = Customers.objects.filter(name=validated_data['name']).first()
        if not customer:
            customer = Customers.objects.create(**validated_data)
        print(order_date)
        order_header = OrdersHeader.objects.create(customer=customer, order_date=order_date)
        # print(order_details)
        for order_detail in order_details:
            OrdersDetail.objects.create(order_header=order_header, **order_detail)
        return order_header

    def update(self, instance, validated_data):
        # print(validated_data)
        order_date = validated_data.get('order_date')
        instance.order_date = order_date
        instance.save()
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

        detail_lst, od_lst = [], []
        for o in order_detail_lst:
            detail = []
            detail.append(o.clothe_num)
            detail.append(o.color)
            detail_lst.append(detail)

        for d in order_detail:
            od = []
            od.append(d['clothe_num'])
            od.append(d['color'])
            od_lst.append(od)
        # print(detail_lst)

        for odl in order_detail_lst:
            db_lst = []
            db_lst.append(odl.clothe_num)
            db_lst.append(odl.color)

            if not db_lst in od_lst and len(db_lst) > 0:  # 数据库中有，但是request提交的数据没有，要删除
                odl.delete()

        order_detail_lst = OrdersDetail.objects.filter(order_header=instance)

        if len(order_detail_lst) == 0:
            for dic in order_detail:
                OrdersDetail.objects.create(order_header=instance, clothe_num=dic['clothe_num'], color=dic['color'],
                                            amount=dic['amount'], price=dic['price'])
            return instance

        for odl in order_detail_lst:  # 数据库的值
            for dic in order_detail:
                request_lst = []
                if odl.clothe_num == dic['clothe_num'] and odl.color == dic['color']:  # 数据库和request提交的数据都有，要修改
                    odl.clothe_num = dic['clothe_num']
                    odl.color = dic['color']
                    odl.amount = dic['amount']
                    odl.price = dic['price']
                    # odl.issued_num = dic['issued_num']
                    # odl.pending_num = odl.amount - dic['issued_num']
                    odl.save()
                else:
                    request_lst.append(dic['clothe_num'])
                    request_lst.append(dic['color'])
                    # print(request_lst)
                    if not request_lst in detail_lst:  # request提交的数据有，数据库中没有，要创建
                        OrdersDetail.objects.create(order_header=instance, clothe_num=dic['clothe_num'],
                                                    color=dic['color'], amount=dic['amount'], price=dic['price'])
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

    order_detail = OrderDetailIssueSerializer(many=True, read_only=False, source='ordersdetail_set')
    # order_detail = OrderDetailIssueSerializer(required=True)

    class Meta:
        model = OrdersHeader
        fields = ['id', 'order_date', 'order_num', 'name', 'phone', 'address', 'order_detail', 'issued_all',
                  'issued_partial']

    def update(self, instance, validated_data):
        order_detail = validated_data.pop('ordersdetail_set')
        issue_flg = ""
        issuedAll, issuedPartial = True, True
        lst_pending_num = []
        order_detail_lst = OrdersDetail.objects.filter(order_header=instance)
        for odl in order_detail_lst:
            isInventoryShorted = False
            for dic in order_detail:
                if odl.clothe_num == dic['clothe_num'] and odl.color == dic['color']:
                    pre_issued_num = odl.issued_num
                    odl.issued_num = dic['issued_num']
                    odl.pending_num = odl.amount - dic['issued_num']
                    # 减少库存数量
                    p = Color.objects.filter(product__clothe_num=dic['clothe_num'], color=dic['color']).first()
                    if not p:
                        isInventoryShorted = True
                        issuedAll = False
                        issuedPartial = False
                        continue
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
        if len(set(lst_pending_num)) == 1 and lst_pending_num[0] == 0 and isInventoryShorted == False:
            instance.issued_all = True
            instance.issued_partial = False
            instance.save()
        else:
            instance.issued_all = False
            instance.issued_partial = True
            instance.save()
        return instance
