from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from chartjs.views.lines import BaseLineChartView
from Data import main_predict
from accounts.models import Deposit, Wallet, Trade, Stock
from django.db.models import Sum
import pandas as pd


class home(TemplateView):
    template_name='website/home.html'
    def get(self, request):
        symbol_list = pd.read_csv("App/stockTrading/Data/ind_nifty50list.csv")
        symbol_list = symbol_list["Symbol"].tolist()
        context = {}
        context['stock'] = request.GET.get('stock')
        context['stock_list'] = symbol_list
        if(request.user.is_authenticated):
            context['deposits'] = Deposit.objects.filter(user = request.user).aggregate(Sum('amount'))['amount__sum']
            wallet = Wallet.objects.filter(user = request.user)
            if wallet.count():
                context['balance'] = wallet.first()
            else:
                context['balance'] = {'balance': None}
            context['open_trades'] = Trade.objects.filter(user = request.user).count()
            context['traded_amount'] = Trade.objects.filter(user = request.user).aggregate(Sum('amount'))['amount__sum']
            if context['stock'] is not None:
                return redirect('{}?stock={}'.format(reverse('line_chart'), request.GET.get('stock')))
            else:
                return render(request, 'website/home.html', context)
        else:
            return redirect(reverse('login'))

class trades(TemplateView):
    template_name='website/tables.html'

    def get(self, request):
        symbol_list = pd.read_csv("App/stockTrading/Data/ind_nifty50list.csv")
        symbol_list = symbol_list["Symbol"].tolist()
        context = {}
        context['stock'] = request.GET.get('stock')
        context['stock_list'] = symbol_list
        if(request.user.is_authenticated):
            context['trades'] = Trade.objects.filter(user = request.user)
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('login'))

class portfolio(TemplateView):
    template_name='website/portfolio.html'

    def get(self, request):
        symbol_list = pd.read_csv("App/stockTrading/Data/ind_nifty50list.csv")
        symbol_list = symbol_list["Symbol"].tolist()
        context = {}
        context['stock'] = request.GET.get('stock')
        context['stock_list'] = symbol_list
        if(request.user.is_authenticated):
            trades = Trade.objects.filter(user = request.user).filter(is_open = True)
            investment = 0
            current_value = 0
            buy_trades = trades.filter(type = 'buy')
            sell_trades = trades.filter(type = 'sell')
            if buy_trades.count():
                investment = investment + float(buy_trades.aggregate(Sum('amount'))['amount__sum'])
            if sell_trades.count():
                current_value = current_value + float(sell_trades.aggregate(Sum('amount'))['amount__sum'])
            for trade in sell_trades:
                symbol = trade.stock
                cmp = float(Stock.objects.filter(stock = symbol).first().ltp)
                investment += cmp*float(trade.quantity)
                trade.current_value = cmp*float(trade.quantity)
                trade.save()
            for trade in buy_trades:
                symbol = trade.stock
                cmp = float(Stock.objects.filter(stock = symbol).first().ltp)
                current_value += cmp*float(trade.quantity)
                trade.current_value = cmp*float(trade.quantity)
                trade.save()
            context['investment'] = investment
            context['current_value'] = current_value
            context['trades'] = trades
            context['pl'] = current_value - investment
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('login'))
            
class LineChartJSONView(BaseLineChartView):

    df_list = []

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        df_list = main_predict.predict_data(self.request.GET.get('stock'))
        index_list = []
        for i in range(len(df_list[1])):
            index_list.append("Day - " + str(i+1))
        x = index_list
        self.df_list = df_list
        return x

    def get_providers(self):
        """Return names of datasets."""
        return ["CLOSE", "SVR", "LSTM"]

    def get_data(self):
        """Return 3 datasets to plot."""

        y0 = self.df_list[0]['Close'].tolist()
        y1 = self.df_list[1].tolist()
        y1_proxy = []
        for i in range(len(y1)):
            y1_proxy.append(y1[i][0])
        y2 = self.df_list[2].tolist()
        y2_proxy = []
        for i in range(len(y2)):
            y2_proxy.append(y2[i][0])
        return [y0, y1_proxy, y2_proxy]


class lc(TemplateView):
    template_name='website/charts.html'

    symbol_list = pd.read_csv("App/stockTrading/Data/ind_nifty50list.csv")
    symbol_list = symbol_list["Symbol"].tolist()

    def get(self, request):
        context = {}
        context['stock'] = request.GET.get('stock')
        context['stock_list'] = self.symbol_list
        if(request.user.is_authenticated):
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('login'))

class deposit(TemplateView):
    template_name='website/deposit.html'

    symbol_list = pd.read_csv("App/stockTrading/Data/ind_nifty50list.csv")
    symbol_list = symbol_list["Symbol"].tolist()

    def get(self, request):
        context = {}
        context['stock'] = request.GET.get('stock')
        context['stock_list'] = self.symbol_list
        if(request.user.is_authenticated):
            context['deposits'] = Deposit.objects.filter(user_id = request.user.id)
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('login'))
    
    def post(self, request):
        context = {}
        context['stock'] = request.GET.get('stock')
        context['stock_list'] = self.symbol_list
        if(request.user.is_authenticated):
            context['deposits'] = Deposit.objects.filter(user_id = request.user.id)
            amount = request.POST.get('amount')
            new_deposit = Deposit(amount = amount, user = request.user)
            new_deposit.save()
            wallet = Wallet.objects.filter(user=request.user)
            if wallet.first() is None:
                wallet = Wallet(balance = float(amount), user = request.user)
            else:
                wallet = wallet.first()
                wallet.balance = wallet.balance + float(amount)
            wallet.save()
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('login'))

line_chart = lc.as_view()
line_chart_json = LineChartJSONView.as_view()
home_view = home.as_view()
deposit_view = deposit.as_view()
trade_history = trades.as_view()
portfolio_view = portfolio.as_view()