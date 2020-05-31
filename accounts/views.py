from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .filters import *
from .decorators import *

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    last_5 = orders.order_by('-id')[:5]
    #print(last_5)
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'customers':customers,'orders':orders,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending,'last_5':last_5}
    return render(request,'accounts/dashboard.html',context)


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                )
            messages.success(request,'Account was created')
            return redirect('login')
    context = {'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
    context = {}
    return render(request,'accounts/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')
@admin_only
def allOrders(request):
    orders = Order.objects.all()
    context = {'orders':orders}
    return render(request,'accounts/orders.html',context)

@login_required(login_url='login')
@admin_only
def products(request):
    p = Product.objects.all()
    return render(request,'accounts/products.html',{'products':p})


@login_required(login_url='login')
@admin_only
def customer(request,uid):
    c = Customer.objects.get(id=uid)
    orders = c.order_set.all()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'customer':c,'orders':orders,'total_orders':orders.count(),'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@admin_only
def createOrder(request,uid):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
    customer = Customer.objects.get(id=uid)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'form':formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@admin_only
def updateOrder(request,uid):
    order = Order.objects.get(id=uid)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@admin_only
def deleteOrder(request,uid):
    order = Order.objects.get(id=uid)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order,'command':'delete_order'}
    return render(request,'accounts/delete_order.html',context)

@login_required(login_url='login')
@admin_only
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
@admin_only
def updateCustomer(request,uid):
    customer = Customer.objects.get(id=uid)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
@admin_only
def deleteCustomer(request,uid):
    customer = Customer.objects.get(id=uid)
    if request.method == 'POST':
        for order in customer.order_set.all():
            order.delete()
        customer.delete()
        return redirect('/')
    context = {'item':customer,'command':'delete_customer'}
    return render(request,'accounts/delete_customer.html',context)