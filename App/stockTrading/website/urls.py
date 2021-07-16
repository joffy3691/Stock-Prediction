from django.urls import path
from .views import home_view, line_chart, line_chart_json, deposit_view, trade_history, portfolio_view

urlpatterns = [
    path('', home_view, name='home'),
    path('deposit', deposit_view, name='deposit'),
    path('portfolio', portfolio_view, name='portfolio'),
    path('trades', trade_history, name='trades'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]