from sales.models import Customers, OrdersHeader, OrdersDetail
from rest_framework import serializers
from django.db.models import Count, Sum
from datetime import datetime, timedelta
import arrow as a


class BaseDateListSerializer(serializers.Serializer):
    x_pre_seven_days = serializers.SerializerMethodField()

    def get_x_pre_seven_days(self, obj):
        result_list = []
        current_date = datetime.now()
        str_current_date = current_date.strftime('%b %d')
        result_list.append(str_current_date)
        for i in range(1, 7):
            result_list.append((current_date - timedelta(days=i)).strftime('%b %d'))
        return result_list

    def get_pre_seven_dates_list(self):
        date_list = []
        current_date = datetime.today().date()
        date_list.append(current_date)
        for i in range(1, 7):
            date_list.append(current_date - timedelta(days=i))
        return date_list


class BaseHalfYearsMonthsListSerializer(serializers.Serializer):
    x_pre_half_years_months = serializers.SerializerMethodField()

    def get_x_pre_half_years_months(self, obj):
        result_list = []
        current_date = a.now()
        str_current_month = current_date.strftime('%b')
        result_list.append(str_current_month)
        for i in range(1, 7):
            result_list.append((current_date.shift(months=-i)).strftime('%b'))
        return result_list

    def get_pre_half_years_month_list(self):
        date_list = []
        current_date = a.now()
        date_list.append(current_date)
        for i in range(1, 7):
            date_list.append(current_date.shift(months=-i))
        date_list = [item.strftime('%Y') + item.strftime('%m') for item in date_list]
        return date_list


class TotalSummarySerializer(serializers.Serializer):
    total_customers = serializers.SerializerMethodField()
    total_sales_amount = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()

    def get_total_customers(self, obj):
        dic = Customers.objects.aggregate(total_customers=Count('name', distinct=True))
        return dic['total_customers']

    def get_total_sales_amount(self, obj):
        dic = OrdersDetail.objects.aggregate(total_sales_amount=Sum('amount'))
        return dic['total_sales_amount']

    def get_total_revenue(self, obj):
        dic = OrdersHeader.objects.aggregate(total_revenue=Sum('order_price'))
        return dic['total_revenue']

    def get_total_orders(self, obj):
        dic = OrdersHeader.objects.aggregate(total_orders=Count('order_num', distinct=True))
        return dic['total_orders']


class PreviousSevenDaysRevenueSerializer(BaseDateListSerializer):
    # x_pre_seven_days = serializers.SerializerMethodField()
    y_sales_revenue = serializers.SerializerMethodField()

    # def get_x_pre_seven_days(self, obj):
    #     result_list = []
    #     current_date = datetime.now()
    #     str_current_date = current_date.strftime('%b %d')
    #     result_list.append(str_current_date)
    #     for i in range(1, 7):
    #         result_list.append((current_date - timedelta(days=i)).strftime('%b %d'))
    #     return result_list

    def get_y_sales_revenue(self, obj):
        pre_seven_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        db_list = OrdersHeader.objects.values('order_date').annotate(total_revenue=Sum('order_price')).filter(
            order_date__gt=pre_seven_date)
        result_list = list(db_list)
        seven_dates_list = self.get_pre_seven_dates_list()
        db_list_dates = [item['order_date'] for item in result_list]  # 将数据库删选结果遍历出order_date放到list里面
        for date in seven_dates_list:
            if date not in db_list_dates:  # 如果前七天的日期不在
                result_list.append({'order_date': date, 'total_revenue': 0})
        result_list.sort(key=lambda x: x['order_date'], reverse=True)  # 对结果按照order_date降序排列
        result_list = [item['total_revenue'] for item in result_list]
        return result_list

    # def get_pre_seven_dates_list(self):
    #     date_list = []
    #     current_date = datetime.today().date()
    #     date_list.append(current_date)
    #     for i in range(1, 7):
    #         date_list.append(current_date - timedelta(days=i))
    #     return date_list


class PreviousSevenDaysOrdersCountSerializer(BaseDateListSerializer):
    # x_pre_seven_days = serializers.SerializerMethodField()
    y_orders_count = serializers.SerializerMethodField()

    # def get_x_pre_seven_days(self, obj):
    #     return PreviousSevenDaysRevenueSerializer().get_x_pre_seven_days(obj)

    def get_y_orders_count(self, obj):
        pre_seven_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        db_list = OrdersHeader.objects.values('order_date').annotate(total_order_count=Count('order_num')).filter(
            order_date__gt=pre_seven_date)
        result_list = list(db_list)
        seven_dates_list = self.get_pre_seven_dates_list()
        db_list_dates = [item['order_date'] for item in result_list]  # 将数据库删选结果遍历出order_date放到list里面
        for date in seven_dates_list:
            if date not in db_list_dates:
                result_list.append({'order_date': date, 'total_order_count': 0})
        result_list.sort(key=lambda x: x['order_date'], reverse=True)
        result_list = [item['total_order_count'] for item in result_list]
        return result_list


class PreviousSevenDaysSalesCountSerializer(BaseDateListSerializer):
    y_sales_count = serializers.SerializerMethodField()

    def get_y_sales_count(self, obj):
        pre_seven_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        db_list = OrdersHeader.objects.values('order_date').annotate(total_sales_count=Sum('ordersdetail__amount')) \
            .filter(order_date__gt=pre_seven_date)
        result_list = list(db_list)
        seven_dates_list = self.get_pre_seven_dates_list()
        db_list_dates = [item['order_date'] for item in result_list]  # 将数据库删选结果遍历出order_date放到list里面
        for date in seven_dates_list:
            if date not in db_list_dates:
                result_list.append({'order_date': date, 'total_sales_count': 0})
        result_list.sort(key=lambda x: x['order_date'], reverse=True)
        result_list = [item['total_sales_count'] for item in result_list]
        return result_list


class PreviousSevenMonthsRevenueSerializer(BaseHalfYearsMonthsListSerializer):
    y_sales_revenue = serializers.SerializerMethodField()

    def get_y_sales_revenue(self, obj):
        str_from_date = a.now().shift(months=-5).replace(day=1).strftime('%Y-%m-%d')
        # db_list = OrdersHeader.objects.values('order_date__month').annotate(total_value=Sum('order_price')) \
        #     .filter(order_date__gte=str_from_date)
        db_list_year = OrdersHeader.objects.values('order_date__year').annotate(total_value=Sum('order_price')) \
            .filter(order_date__gte=str_from_date)
        db_list_month = OrdersHeader.objects.values('order_date__month').annotate(total_value=Sum('order_price')) \
            .filter(order_date__gte=str_from_date)
        for index, item in enumerate(db_list_month):
            if len(str(item['order_date__month'])) == 1:
                item['order_date__month'] = '0%s' % (item['order_date__month'])
            item['order_date__month'] = '%s%s' % (db_list_year[index]['order_date__year'], item['order_date__month'])
        result_list = list(db_list_month)
        db_list_month = [item['order_date__month'] for item in result_list]
        half_years_month_list = self.get_pre_half_years_month_list()
        for m in half_years_month_list:
            if m not in db_list_month:
                result_list.append({'order_date__month': m, 'total_value': 0})
        result_list.sort(key=lambda x: int(x['order_date__month']), reverse=True)
        result_list = [item['total_value'] for item in result_list]
        return result_list


class TopSevenCustomersSerializer(serializers.Serializer):
    customer_names = serializers.SerializerMethodField()
    total_order_price = serializers.SerializerMethodField()

    def get_customer_names(self, obj):
        db_list = self.get_db_list
        return [item['customer_id__name'] for item in db_list]

    def get_total_order_price(self, obj):
        db_list = self.get_db_list
        return [item['total_order_price'] for item in db_list]

    @property
    def get_db_list(self):
        db_list = OrdersHeader.objects.values('customer_id__name').annotate(total_order_price=Sum('order_price')) \
            .order_by('-total_order_price')[:7]
        return db_list














