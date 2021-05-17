from django.db.models import fields
from sales.models import Customers, Orders, Dates
from rest_framework import serializers




class OrderSerializers(serializers.ModelSerializer):

    
    class Meta:
        model = Orders
        # fields = '__all__'
        exclude = ['date']
    # order_date = serializers.CharField(source='orders.order_date')
    # colthe_num = serializers.CharField(source='orders.colthe_num')
    # color = serializers.CharField(source='orders.color')
    # amount = serializers.IntegerField(source='orders.amount')
    # price = serializers.FloatField(source='orders.price')
    # total_price = serializers.FloatField(source='orders.total_price')
    # delivered = serializers.CharField(source='orders.delivered')

    # order_date = serializers.DateField('customer.date')
    # name = serializers.CharField(source='customer.name')
    # address = serializers.CharField(source='customer.address')
    # phone = serializers.CharField(source='customer.phone')
    # order = serializers.SerializerMethodField()

    # class Meta:
    #     model = Orders
    #     # fields = ['order_date', 'name', 'colthe_num','color','amount','price','total_price','phone','address','delivered']
    #     fields = ['order_date', 'name', 'phone','address', 'order']
    # def get_order(self, order):
    #     result = []
    #     date =  order.dates.all()
    #     for order in list_orders:


# class OrderSerializers(serializers.Serializer):
#     order_date = serializers.DateField()
#     name = serializers.CharField(source='customer.name')
#     address = serializers.CharField(source='customer.address')
#     phone = serializers.CharField(source='customer.phone')
#     order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.filter(date=order_date))

class CustomerSerializers(serializers.ModelSerializer):
    # order_date = serializers.DateField('customer.date')
    order = OrderSerializers(many=True)
    order_date = serializers.SerializerMethodField()
    # order = serializers.SerializerMethodField()
    class Meta:
        model = Customers
        fields = ['order_date','name','phone','address','order']
    
    def get_order_date(self, row):
        order_dic ={}
        orders = row.order
        order_dic['order_date'] = 
        return order_dic
        # orders = row.order.filter(customer__name=row.name)
        # for order in orders:
        #     order_dic['order'] = order
        # return result

    




# from sales.serializers import CustomerSerializers
# k = CustomerSerializers()
# from sales.models import Customers
# k.get_order(Customers)