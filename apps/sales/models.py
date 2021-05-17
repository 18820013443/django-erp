from django.db import models
# from warehouse.models import Product, Color
import warehouse.models
from warehouse.models import get_amount
# from datetime import datetime
import datetime
import time

# Create your models here.
# class Dates(models.Model):
    # orders = models.ForeignKey(Orders,on_delete=models.CASCADE)
    # date = models.DateField(auto_now=True)

class Customers(models.Model):
    name = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    # orders = models.ForeignKey(Orders, on_delete=models.CASCADE)


class OrdersHeader(models.Model):
    order_date = models.DateField(auto_now_add=True)
    order_num = models.CharField(max_length=12, unique=True,blank=True,null=False)
    # delivered = models.BooleanField(default=False)
    customer = models.ForeignKey(Customers, related_name='order_detail',on_delete=models.CASCADE)
    order_price = models.FloatField(blank=True,null=True)
    issued_all = models.BooleanField(default=False)
    issued_partial = models.BooleanField(default=False)
    # date = models.ForeignKey(Dates,on_delete=models.CASCADE)

    # 0001
    @property
    def get_order_number(self):
        date = datetime.date.today().strftime('%Y%m%d')
        num = len(OrdersHeader.objects.filter(order_date=datetime.date.today())) + 1
        # num = len(OrdersHeader.objects.all()) + 1
        print("num:",num)
        
        if len(str(num)) == 1:
            order_num = '%s%s%s'%(date,'000',num)
        elif len(str(num)) ==2:
            order_num = '%s%s%s'%(date,'00',num)
        elif len(str(num)) ==3:
            order_num = '%s%s%s'%(date,'0',num)
        elif len(str(num)) ==4:
            order_num = '%s%s'%(date,num)
        # num = ""
        # for i in range(count-1):
        #     num = num + '0'
        # if count != 4:
        #     order_num = '%s%s%s'%(date,num,len(OrdersHeader.objects.all()+1))
        # else:
        #     order_num = '%s%s'%(date, num)
        return order_num

   


    def save(self, *args, **kwarg):
        # try:
        if not self.order_num:
            self.order_num = self.get_order_number
        super(OrdersHeader, self).save(*args, **kwarg)
        # except:
        #     time.sleep(0.3)
        #     self.save(*args, **kwarg)


class OrdersDetail(models.Model):
    clothe_num = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    amount = models.IntegerField()
    issued_num = models.IntegerField(default=0)
    pending_num = models.IntegerField(default=0)
    price = models.FloatField()
    total_price = models.FloatField(blank=True,null=False)
    # order_header = models.ForeignKey(OrdersHeader, blank=True,null=False,related_name='order_detail',on_delete=models.CASCADE)
    order_header = models.ForeignKey(OrdersHeader, blank=True,null=False,on_delete=models.CASCADE)

    @property
    def get_total_price(self):
        return float(self.price) * float(self.amount)

    @property
    def get_order_price(self):
        print(self.order_header)
        details = OrdersDetail.objects.filter(order_header=self.order_header)
        # print(details)
        order_price = 0
        for detail in details:
            print(detail.total_price)
            order_price += detail.total_price
        return order_price

    def save(self, *args, **kwarg):
        self.total_price = self.get_total_price
        # self.pending_num = self.amount - self.issued_num
        super(OrdersDetail, self).save(*args, **kwarg)
        # print(self.get_order_price)
        # print(self.order_header)
        self.order_header.order_price = self.get_order_price

        # if self.issued_num == self.amount:
        #     self.order_header.issued_all = True
        #     self.order_header.issued_partial = False
        # else:
        #     self.order_header.issued_all = False
        #     self.order_header.issued_partial = True
        self.order_header.save()
        # inventory = Inventory.objects.get(clothe_num=self.clothe_num, color=self.color)
        # p = warehouse.models.Product.objects.filter(clothe_num = self.clothe_num).first()
        # c = warehouse.models.Color.objects.filter(product=p).first()
        # c.amount = int(get_amount(self.clothe_num, self.color)) - int(self.amount)
        # c.save()
        # super(OrdersHeader, self.order_header).save(*args, **kwarg)

# class DeliverGoods(models.Model):
#     issue_num = models.IntegerField(default=0)
#     pending_num = models.IntegerField(default=0)
#     issue_all = models.BooleanField(default=False)
#     issue_partial = models.BooleanField(default=False)
#     order_header = models.OneToOneField(OrdersHeader, on_delete=models.CASCADE)

#     def get_issue_num(self):
#         pass

#     def get_pending_num(self):
#         pass
    
#     def get_issue_all(self):
#         pass

#     def get_order_header(self):
#         pass












