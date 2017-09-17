from builtins import print
from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum



def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})


def login(request):
   return render(request, 'portfolio/login.html',
                 {'portfolio': login})


@login_required
def customer_list(request):
   customer = Customer.objects.filter(created_date__lte=timezone.now())
   return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
       # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
   print("inside stocks")
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

#investment code goes here
@login_required
def investment_list(request):
   print("inside investment")
   investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investments = form.save(commit=False)
           investments.created_date = timezone.now()
           investments.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})


@login_required
def investment_edit(request, pk):
   investments = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investments)
       if form.is_valid():
           investments = form.save()
           # stock.customer = stock.id
           investments.updated_date = timezone.now()
           investments.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
   else:
       # print("else")
       form = InvestmentForm(instance=investments)
   return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
   investments = get_object_or_404(Investment, pk=pk)
   investments.delete()
   investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   mutual_fund = Mutual_fund.objects.filter(customer=pk)
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   sum_recent_value= Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   for k,v in sum_acquired_value.items():
       var1=v
   for k,v in sum_recent_value.items():
        var2=v
   print(stocks)
   stock_list=[]
   sum1=0
   for i in stocks:
       print (i.symbol)
       yahoo=Share(i.symbol)
       va=yahoo.get_price()
       va2=float(va) * float(i.shares)
       stock_list.append(va)
       sum1=sum1+float(va) * float(i.shares)

   print(stock_list)
   sum=0
   for i in stocks:
       sum=sum+i.shares * i.purchase_price

   sum_initial_mf=0
   for i in mutual_fund:
        sum_initial_mf= sum_initial_mf+i.units *i.net_asset_value

   sum_recent_mf = Mutual_fund.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   for k,v in sum_recent_mf.items():
       sum_recent_mf=v

   portfolio_initial=float(sum)+float(var1)+float(sum_initial_mf)
   portfolio_current=float(sum1)+float(var2)+float(sum_recent_mf)
   grand_total=float(portfolio_current)-float(portfolio_initial)
   grand_total=str(round(grand_total,2))

   return render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                      'stocks': stocks,
                                                      'sum_acquired_value': var1,
                                                       'sum_recent_value':var2,
                                                       'sum_initial_stock_value':sum,
                                                       'sum_current_stock_value':sum1,
                                                       'result1':float(sum1)-float(sum),
                                                        'result':var2-var1,
                                                        'mutual_fund':mutual_fund,
                                                       'stock_list':stock_list,
                                                       'sum_initial_mutual_funds':sum_initial_mf,
                                                       'sum_current_mutual_funds':sum_recent_mf,
                                                       'result2':str(round(float(sum_recent_mf)-float(sum_initial_mf),2)),
                                                       'portfolio_initial':str(round(portfolio_initial,2)),
                                                       'portfolio_current':str(round(portfolio_current,2)),
                                                       'grand_total':grand_total,},

                                                       )
def sub(recent_value,acquired_value):
    result=recent_value-acquired_value
    return result

def curr(a,b):
    result= a * b
    print ("curr_stock_value" +str(result))
    return result

def acquired_value(request,pk):
    var=Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    return str(var)



@login_required
def mutual_fund_list(request):
   print("inside mutual fund")
   mutual_fund = Mutual_fund.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/mutual_fund_list.html', {'mutual_fund': mutual_fund})

@login_required
def mutual_fund_new(request):
   if request.method == "POST":
       form = Mutual_fundForm(request.POST)
       if form.is_valid():
           mutual_fund = form.save(commit=False)
           mutual_fund.purchase_date = timezone.now()
           mutual_fund.save()
           mutual_fund = Mutual_fund.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/mutual_fund_list.html',
                         {'mutual_fund': mutual_fund})
   else:
       form = Mutual_fundForm()
       # print("Else")
   return render(request, 'portfolio/mutual_fund_new.html', {'form': form})

@login_required
def mutual_fund_edit(request, pk):
   mutual_fund = get_object_or_404(Mutual_fund, pk=pk)
   if request.method == "POST":
       form = Mutual_fundForm(request.POST, instance=mutual_fund)
       if form.is_valid():
           mutual_fund = form.save()
           # stock.customer = stock.id
           mutual_fund.updated_date = timezone.now()
           mutual_fund.save()
           mutual_fund = Mutual_fund.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/mutual_fund_list.html', {'mutual_fund': mutual_fund})
   else:
       # print("else")
       form = Mutual_fundForm(instance=mutual_fund)
   return render(request, 'portfolio/mutual_fund_edit.html', {'form': form})


@login_required
def mutual_fund_delete(request, pk):
   mutual_fund = get_object_or_404(Mutual_fund, pk=pk)
   mutual_fund.delete()
   mutual_fund = Mutual_fund.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/mutual_fund_list.html', {'mutual_fund': mutual_fund})

