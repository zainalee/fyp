from django.shortcuts import render, redirect
from products.models import *
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import json
import datetime
# from django.contrib.auth.forms import UserCreationForm
from templates.gui.forms import UserForm, SellerFrom, ProductForm, LoginForm, CLoginForm, ReviewForm, CategoriesForm, UpdateOrderStatusForm, StatusForbuyerForm, UpdateOrderItemStatusForSllerForm, UpdateOrderItemStatusForBuyerForm, UploadProfileForm, DealProductForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Subquery

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decoraters import unauthenticated, allowed_users
from profiles.models import SellerProfile
from django.contrib.auth.models import PermissionsMixin
from django.http import HttpResponse, HttpResponseRedirect
from products.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.filters import ProductFilter, OrderFilter
from django.conf import settings
from django.db.models import Subquery
from django.core.mail import EmailMessage
from django.db.models import Q
from math import ceil
# from .filters import UserFilter


def is_valid_queryparam(param):
    return param != '' and param is not None


def main(request):
    products_slider = Product.objects.filter(deal_status=1)
    print(products_slider)
    n = len(products_slider)
    nSlides = n//4 + ceil((n/4)-(n//4))
    params = {'no_of_slides': nSlides, 'range': range(
        1, nSlides), 'products_slider': products_slider}
    products_list = Product.objects.filter(deal_status=0)
    categories = Categories.objects.all()
    category = request.GET.get('category')
    title = request.GET.get('title')
    min_price = request.GET.get('min-price')
    max_price = request.GET.get('max-price')

    # latest_review_list = Review.objects.filter(
    #     product=pk).order_by('-pub_date')[:9]
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        orderItems = order['get_cart_items']

    # filter = ProductFilter(request.GET, queryset=products_list)
    # products_list = filter.qs
    if is_valid_queryparam(title):
        products_list = products_list.filter(title__icontains=title)

    if is_valid_queryparam(category) and category != 'Select Category':
        products_list = products_list.filter(category__title=category)

    if is_valid_queryparam(min_price):
        products_list = products_list.filter(price__gte=min_price)

    if is_valid_queryparam(max_price):
        products_list = products_list.filter(price__lte=max_price)

    page = request.GET.get('page', 1)

    paginator = Paginator(products_list, 12)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    # context = {
    #     'products_list': products_list,
    #     'product': product,
    #     'page': page
    # }
    return render(request, 'gui/main.html', {'no_of_slides': nSlides, 'range': range(1, nSlides), 'products_slider': products_slider, 'product': product, 'products_list': products_list, 'orderItems': orderItems, 'categories': categories, })


def detailview(request, pk):
    product_detail = Product.objects.get(id=pk)
    suggestion = Product.objects.filter(
        title__icontains=product_detail.title)
    suggestion2 = Product.objects.all()
    if suggestion:
        for product in suggestion:
            print(product.title)
    else:
        for product in suggestion2:
            print(product.title)

    latest_review_list = Review.objects.filter(
        product=pk).order_by('-pub_date')[:9]
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        # user_name = form.cleaned_data['user_name']
        review = Review()
        review.product = product_detail
        review.user_name = request.user
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect('')
    if request.user.is_authenticated:
        user = Product.objects.filter(user=request.user)
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        orderItems = order['get_cart_items']
    # print("user ", user)
    context = {
        'product_detail': product_detail,
        'latest_review_list': latest_review_list,
        # 'user': user,
        'orderItems': orderItems,
        'form': form,
        'suggestion': suggestion,
        'suggestion2': suggestion2
    }
    return render(request, 'gui/detailview.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers'])
def home(request):
    # user = User.objects.filter(user=request.user)
    # context = {'user': user}
    product = Product.objects.filter(user=request.user).count()
    product_owner = Product.objects.filter(user=request.user)
    print(product_owner)
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        orderItems = order['get_cart_items']
    context = {
        'product': product,
        'orderItems': orderItems
    }
    return render(request, 'gui/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers'])
def products(request):
    products = Product.objects.filter(user=request.user)
    context = {'products': products, }
    return render(request, 'sellerprofile/myproducts.html', context)


@unauthenticated
def login(request):
    form = LoginForm
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user = SellerProfile
        user = authenticate(
            request, username=username, password=password)
        if user is not None:
            # if user.role == "seller_profile":
            auth_login(request, user)

            return redirect('main')
        else:
            messages.error(request, 'Username or password is incorrect!')
    context = {
        'form': form
    }
    return render(request, 'sellerprofile/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


@unauthenticated
def registration(request):
    if request.method == 'POST':
        # username = request.POST.get('first_name')
        # password = request.POST.get('username')
        # username = request.POST.get('password')
        # password = request.POST.get('password2')
        form = UserForm(request.POST)
        sellerFrom = SellerFrom(request.POST)
        if form.is_valid() and sellerFrom.is_valid():
            cnic = form.cleaned_data.get('cnic')
            # v = len(str(cnic))
            # print(v)
            user = form.save()
            seller = sellerFrom.save()
            seller.user = user
            seller.save()
            username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            gorup = Group.objects.get(name='sellers')
            user.groups.add(gorup)
            messages.success(request, 'account was created for' + username)
            # form = UserForm()
            # sellerFrom = SellerFrom()
            return redirect('login')
    else:
        form = UserForm()
        sellerFrom = SellerFrom()

    context = {'form': form, 'sellerForm': sellerFrom}
    return render(request, 'sellerprofile/sellersignup.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers'])
def createproduct(request):
    categories = Categories.objects.all()
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            quantity = form.cleaned_data.get("quantity")
            minorder = form.cleaned_data.get("minorder")
            price = form.cleaned_data.get("price")
            image = form.cleaned_data.get("image")
            title = form.cleaned_data.get("title")
            min_delivery_days = form.cleaned_data.get("delivery_days")
            max_delivery_days = form.cleaned_data.get("max_delivery_days")

            print(quantity)
            print(price)
            print(minorder)
            print(title)
            if(quantity >= minorder):
                if min_delivery_days < max_delivery_days:
                    print("quantity checked")
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
                    return redirect('products')
                else:
                    messages.error(
                        request, 'Minimum Delivery Days should musl be less than maximum delivery days')
            else:
                messages.error(
                    request, 'minimum order quantity must be less than or equal to orignal quantity')
        else:
            messages.error(request, "Please Fill all Fields")
    else:
        form = ProductForm()
    context = {'form': form, 'categories': categories}
    return render(request, 'sellerprofile/creatproduct.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers'])
def updateproduct(request, pk):
    product = Product.objects.get(id=pk)
    # form = ProductForm(request.POST,
    #                    request.FILES,  instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,
                           request.FILES,  instance=product)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    context = {'form': form}
    return render(request, 'sellerprofile/updateproduct.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers'])
def product_deal(request, pk):
    product = Product.objects.get(id=pk)
    form = DealProductForm(request.POST, instance=product)
    if request.method == 'POST':
        form = DealProductForm(request.POST, instance=product)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            return redirect('products')
    else:
        form = DealProductForm(instance=product)
    context = {'form': form}
    return render(request, 'sellerprofile/product_deal.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sellers'])
def deleteproduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    context = {'product': product}
    return render(request, 'gui/deleteproduct.html', context)

# @unauthenticated
# def ClientRegistration(request):
#     context = {}
#     if request.POST:
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             email = EmailMessage(
#                 'Hello',
#                 'Body goes here',
#                 'from@example.com',
#                 ['to1@example.com', 'to2@example.com'],
#                 ['bcc@example.com'],
#                 reply_to=['another@example.com'],
#                 headers={'Message-ID': 'foo'},
#             )
#             return redirect('login')
#         else:
#             # messages.error(request, "this field require")
#             context['form'] = form
#     else:
#         form = UserForm()
#         context['form'] = form
#     return render(request, 'sellerprofile/sregister.html', context)


@unauthenticated
def ClientRegistration(request):
    context = {}
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # messages.error(request, "this field require")
            context['form'] = form
    else:
        form = UserForm()
        context['form'] = form
    return render(request, 'sellerprofile/sregister.html', context)


@unauthenticated
def Clientlogin(request):
    form = CLoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user = SellerProfile
        user = authenticate(
            request, username=username, password=password)
        if user is not None:
            # if user.role == "seller_profile":
            auth_login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {'form': form}
    return render(request, 'gui/Clientlogin.html', context)


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        orderItems = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'orderItems': orderItems
    }
    return render(request, 'gui/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    # product_detail = Product.objects.get(id=pk)
    context = {
        'items': items,
        'order': order
    }
    return render(request, "gui/checkout.html", context)


def updateItem(request):
    print("view test")
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    minimum = data['minorder']
    # minorder = int(minimum)
    print('Action: ', action)
    print('ProductId: ', productId)
    print('minorder:', minimum)
    user = request.user

    product = Product.objects.get(id=productId)
    # productmin = Product.objects.filter(id=productId)
    print('minprder', product.minorder)
    order, created = Order.objects.get_or_create(user=user, complete=False)
    total = order.get_cart_total
    if product.deal_status == 1:
        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product, user=user, price=product.get_deal_price, quantity=minimum)
    else:
        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product, user=user, price=product.get_price, quantity=minimum)
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    if action == 'delete':
        order_item.quantity = 0
    order_item.save()
    if order_item.quantity < int(product.minorder):
        order_item.delete()

    return JsonResponse("item was added", safe=False)


# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    user = request.user
    email = user.email
    usernname = request.user.username
    # email = User.objects.get(user)
    # print(email.email)
    number = data['ph_number']

    order, created = Order.objects.get_or_create(user=user, complete=False)
    order.transaction_id = transaction_id
    order.complete = True
    order.save()
    ShippingAddress.objects.create(
        name=usernname,
        user=user,
        order=order,
        address=data['address'],
        ph_number=data['ph_number'],
        city=data['city'],
        state=data['state'],
        zipcode=data['zipcode'],
    )

    email_subject = "Congratulations order placed successfully"
    email_body = ".." + data['address']
    email = EmailMessage(
        email_subject,
        email_body,
        'from@example.com',
        [email],
    )
    email.send(fail_silently=True)

    print("transaction id is :", transaction_id)
    print('data:', request.body)
    return JsonResponse("order Completed", safe=False)


def demo(request):
    return render(request, "sellerprofile/layout.html")


def shop(request):
    return render(request, "shop/navbar.html")


def profile(request):
    return render(request, "sellerprofile/profile.html")


def showprofile(request, pk):

    return render(request, "sellerprofile/profile.html")


def myOrders(request):
    order = Order.objects.filter().order_by('-date_orderd')
    orderq = Order.objects.all().values_list('id', flat=True)

    orderitems = OrderItem.objects.filter(
        user=request.user, order__complete=1).select_related('order').order_by('-date_orderd')
    filter = OrderFilter(request.GET, queryset=orderitems)
    orderitems = filter.qs
    # detail = zip(order, orderitems)
    return render(request, "sellerprofile/myOrders.html", {'detail': orderitems, 'filter': filter})


def selling(request):
    order = Order.objects.all()
    items = OrderItem.objects.all()
    uid = request.user.id
    orderitems = OrderItem.objects.filter(
        product__user=request.user, order__complete=1).select_related('order').order_by('-date_orderd')

    return render(request, "sellerprofile/selling.html", {'orderitems': orderitems})


def orderdetails(request, pk):
    orderdetails = ShippingAddress.objects.get(order_id=pk)
    print(pk)
    context = {
        'orderdetails': orderdetails,
    }
    return render(request, 'sellerprofile/orderdetails.html', context)


def updateorder(request, pk):
    orderitem = OrderItem.objects.get(id=pk)
    orderdetails = ShippingAddress.objects.get(order_id=orderitem.order)
    if request.user.is_authenticated:
        form = UpdateOrderItemStatusForSllerForm(instance=orderitem)
        if request.method == 'POST':
            form = UpdateOrderItemStatusForSllerForm(
                request.POST, instance=orderitem)
            if form.is_valid():
                form.save()
                return redirect('selling')
    context = {
        'form': form,
        'orderdetails': orderdetails,
        'orderitem': orderitem
    }
    return render(request, 'sellerprofile/updateorder.html', context)


def updateorderforbuyer(request, pk):
    orderitem = OrderItem.objects.get(id=pk)
    form = UpdateOrderItemStatusForBuyerForm(instance=orderitem)
    if request.method == 'POST':
        form = UpdateOrderItemStatusForBuyerForm(
            request.POST, instance=orderitem)
        if form.is_valid():
            form.save()
            return redirect('myorders')
    context = {
        'form': form
    }
    return render(request, 'sellerprofile/updateorderbybuyer.html', context)


def adminhome(request):
    users = User.objects.all().count()
    products = Product.objects.all().count()
    categories = Categories.objects.all().count()
    if request.user.is_authenticated:
        wish_list = Wishlist.objects.filter(user=request.user)
        order = Order.objects.filter(user=request.user)
    address = ShippingAddress.objects.select_related('order')
    uid = request.user.id
    orderitems = OrderItem.objects.select_related('product', 'order')
    total_orderitems = OrderItem.objects.filter(
        product__user=request.user, order__complete=1, status='Delivered', statusforbuyer="Received")
    total_incom = 0
    for price in total_orderitems:
        total_incom = total_incom+price.price*price.quantity
    detail = zip(order, orderitems, address)
    total_product = Product.objects.filter(user=request.user).count()
    total_orders = OrderItem.objects.filter(
        product__user=request.user, status='Delivered', statusforbuyer="Received").filter(order__complete=1).count()
    total_orders_analysis = OrderItem.objects.filter(
        product__user=request.user).filter(date_orderd__month='8')
    buyer_orders = 0
    for o in order:
        if o.complete == 1:
            buyer_orders = OrderItem.objects.filter(
                user=request.user, status='Delivered', statusforbuyer="Received").count()
    total_spent = 0
    total_buy = OrderItem.objects.filter(
        user=request.user, status='Delivered', statusforbuyer="Received")
    for spent in total_buy:
        total_spent = total_spent + spent.price*spent.quantity
    context = {
        'total_product': total_product,
        'detail': detail,
        'uid': uid,
        'total_orders': total_orders,
        'total_incom': total_incom,
        'buyer_orders': buyer_orders,
        'total_spent': total_spent,
        'total_orders_analysis': total_orders_analysis,
        'wish_list': wish_list,

        # for superuser
        'users': users,
        'products': products,
        'categories': categories

    }
    return render(request, "sellerprofile/home.html", context)


# @login_required
def add_to_wishlist(request, pk):
    if request.user.is_authenticated:
        item = Product.objects.get(id=pk)

        wished_item, created = Wishlist.objects.get_or_create(wished_item=item,
                                                              user=request.user,
                                                              )
        messages.success(request, 'The item was added to your wishlist')
    return redirect('main')


@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    # product = Wishlist.objects.get(wished_item=pk)
    # contnt = zip(wishlist, product)
    return render(request, 'sellerprofile/wishlist.html', {'wishlist': wishlist})


def wishlist_detail_view(request, pk):
    wishlist = Wishlist.objects.get(user=request.user, id=pk)
    return render(request, 'sellerprofile/wishlist.html', {'wishlist': wishlist})


def delete_wishlist(request, pk):
    wishlist = Wishlist.objects.get(id=pk)
    if request.method == 'POST':
        wishlist.delete()
        messages.success(request, 'The item Removed from your wishlist')
        return redirect('wishlist')
    context = {'wishlist': wishlist}
    return render(request, 'sellerprofile/deletewishlist.html', context)


def users(request):
    user = User.objects.all()
    products = Product.objects.all()
    context = {
        'user': user,
        'products': products
    }
    return render(request, 'sellerprofile/userlist.html', context)


# def products(request):
#     user = User.objects.all()
#     products = Product.objects.all()
#     context = {
#         'user': user,
#         'products': products
#     }
#     return render(request, 'sellerprofile/products.html', context)


def deleteuser(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('userlist')
    context = {'user': user}
    return render(request, 'sellerprofile/deleteuser.html', context)


def add_categories(request):
    form = CategoriesForm()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('adminhome')
    context = {
        'form': form
    }
    return render(request, 'sellerprofile/addcategories.html', context)


def categories(request):
    categories = Categories.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'sellerprofile/categories.html', context)


def deletecat(request, pk):
    cat = Categories.objects.get(id=pk)
    if request.method == 'POST':
        cat.delete()
        return redirect('categories')
    context = {'cat': cat}
    return render(request, 'sellerprofile/deletecategory.html', context)


def feedback(request, pk):
    # product_detail = Product.objects.get(id=pk)
    latest_review_list = Review.objects.filter(
        product=pk).order_by('-pub_date')[:9]
    orderitems = OrderItem.objects.get(id=pk)
    product_detail = Product.objects.get(id=orderitems.product_id)
    orderitem = OrderItem.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            # user_name = form.cleaned_data['user_name']
            review = Review()
            review.product = product_detail
            review.user_name = request.user
            review.rating = rating
            review.comment = comment
            review.pub_date = datetime.datetime.now()
            review.save()
            OrderItem.objects.filter(
                id=orderitem.id).update(feedback_status='1')
            return redirect('myorders')
    context = {
        'form': form
    }
    return render(request, 'sellerprofile/feedback.html', context)


def mystore(request, pk):
    products = Product.objects.filter(user=pk)
    user_info = Product.objects.filter(user=pk).first()
    reviews = Review.objects.filter(product__user=pk)
    total_reviews = Review.objects.filter(product__user=pk).count()
    for review in reviews:
        print(review.comment)

    for product in products:
        print(product.title)

    context = {
        'products': products,
        'user_info': user_info,
        'reviews': reviews,
        'total_reviews': total_reviews
    }

    return render(request, 'gui/mystore.html', context)


def profile_settings(request):
    user = request.user.sellerprofile
    form = UploadProfileForm(instance=user)
    if request.method == 'POST':
        form = UploadProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Settings updated Successfully!')
            return redirect('profile')

    context = {
        'form': form,
    }
    return render(request, 'sellerprofile/settings.html', context)


def seller_product_view_details(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product
    }
    return render(request, 'sellerprofile/seller_product_view_details.html', context)
