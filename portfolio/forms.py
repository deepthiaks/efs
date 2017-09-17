from django import forms
from .models import Customer, Investment, Stock, Mutual_fund


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_number', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone',)


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = (
            'customer', 'category', 'description', 'acquired_value', 'acquired_date', 'recent_value',
            'recent_date',)


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('customer', 'symbol', 'name', 'shares', 'purchase_price', 'purchase_date',)



class Mutual_fundForm(forms.ModelForm):
    class Meta:
        model = Mutual_fund
        fields = ('customer', 'fund_name', 'units', 'purchase_date', 'net_asset_value',)
