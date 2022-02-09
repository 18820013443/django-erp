# from warehouse.models import Product, Color
from rest_framework import serializers
import warehouse.models


class InventorySerializer(serializers.ModelSerializer):

    clothe_num = serializers.CharField(source='product.clothe_num')
    class Meta:
        model = warehouse.models.Color
        fields = ['id','clothe_num','color','amount']


    def create(self, validated_data):
        clothe_num = validated_data.pop('product')['clothe_num']
        color = validated_data['color']
        amount = validated_data['amount']
        p = warehouse.models.Product.objects.filter(clothe_num=clothe_num).first()
        if not p: # 如果产品不存在，创建产品，创建颜色和数量
            p = warehouse.models.Product.objects.create(clothe_num=clothe_num)
            c = warehouse.models.Color.objects.create(product=p,color=color,amount=amount)
        else:
            c = warehouse.models.Color.objects.filter(product=p,color=color).first()
            if c: # 查看款号和颜色是否存在，如果存在, 增加数量保存
                c.amount += amount
                c.save()
            else: # 如果不存在，创建新的记录
                c = warehouse.models.Color.objects.create(product=p,color=color,amount=amount)
        
        return c
    
    def update(self, instance, validated_data):
        clothe_num = validated_data.pop('product')['clothe_num']
        print(clothe_num)
        color = validated_data['color']
        amount = validated_data['amount']
        # p = warehouse.models.Color.objects.filter(clothe_num=clothe_num).first()
        p = instance.product
        p.clothe_num = clothe_num
        p.save()
        instance.color = color
        instance.amount = amount
        instance.save()
        return instance

    

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = warehouse.models.Income
        fields = "__all__"