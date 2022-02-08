from django.db import models
# from sales.models import Orders
import sales.models
from django.db.models import Q


class Product(models.Model):
    clothe_num = models.CharField(max_length=20,unique=True)

class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=10)
    amount = models.IntegerField()

class Income(models.Model):
    date = models.DateField(auto_now_add=True)
    bag_num = models.IntegerField()
    clothe_num = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    amount = models.IntegerField()

    def save(self, *args, **kwarg):
        product = Product.objects.filter(clothe_num=self.clothe_num).first()
        color = Color.objects.filter(color=self.color).first()
        if product and color:
            color.amount += get_amount(self.clothe_num,self.color)
            color.save()
        elif product and not color:
            Color.objects.create(product=product, color=self.color,amount=self.amount)
        else:
            # p = Product.objects.create(clothe_num=self.clothe_num)
            p = Product()
            p.clothe_num = self.clothe_num
            p.save()
            Color.objects.create(product=p, color=self.color,amount=self.amount)
        super(Income, self).save()

"""
    1. 如果产品和颜色都有，那么只需要在color表加上income的数量
    2. 如果有产品，没有颜色，那么需要创建color对象
    3. 如果没有产品，则需要重新创建product，和color
"""

'''
    get_amount --> 所有的income减去outcome的结果
'''
def get_amount(clothe_num, color):
    # order_list = sales.models.OrdersDetail.objects.filter(clothe_num=clothe_num,color=color,order_header__delivered=True)
    order_list = sales.models.OrdersDetail.objects.filter(Q(clothe_num=clothe_num,color=color,order_header__issued_all=True) | Q(clothe_num=clothe_num,color=color,order_header__issued_partial=True))
    income_amount, out_amount = 0, 0
    if order_list:
        for order in order_list:
            # out_amount += order.amount
            out_amount += order.issued_num
            # out_amount = out_amount + order.amount
    else:
        out_amount = 0
    income_list = Income.objects.filter(clothe_num=clothe_num,color=color)
    if income_list:
        for income in income_list:
            income_amount += income.amount
            # income_amount = income_amount + income.amount
    else:
        income_list = 0
    
    return income_amount - out_amount

# class Inventory(models.Model):
#     clothe_num = models.CharField(max_length=20)
#     color = models.CharField(max_length=10)
#     amount = models.IntegerField()

#     def get_amount(self):
#         order_list = Orders.objects.filter(delivered=True)
#         for order in order_list:
#             out_amount += order.amount
#         income_list = Income.objects.all()
#         for income in income_list:
#             income_amount += income.amount
        
#         return income_amount - outcome_amount
        
    # def save(self, *args, **kwarg):
    #     self.amount = self.get_amount()
    #     super().save()
