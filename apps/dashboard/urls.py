from django.urls import path, re_path
from dashboard.views import TotalSummaryView, PreviousSevenDaysRevenueView, PreviousSevenDaysOrdersCountView\
    , PreviousSevenDaysSalesCountView, PreviousHalfYearsMonthsRevenueView, TopTenCustomersView

urlpatterns = [
    re_path('^total_summary/$', TotalSummaryView.as_view()),
    re_path('^seven_dates_revenue/$', PreviousSevenDaysRevenueView.as_view()),
    re_path('^seven_dates_orders/$', PreviousSevenDaysOrdersCountView.as_view()),
    re_path('^seven_dates_sales/$', PreviousSevenDaysSalesCountView.as_view()),
    re_path('^seven_months_revenue/$', PreviousHalfYearsMonthsRevenueView.as_view()),
    re_path('^top_seven_customers/$', TopTenCustomersView.as_view())
]
