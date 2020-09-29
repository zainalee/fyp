# from django.shortcuts import render, redirect
# from products.models import *
# from django.contrib.auth.models import User
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from products.filters import ProductFilter
# from django.conf import settings
# # from .filters import UserFilter


# # def search(request):
# #     product_list = Product.objects.all()
# #     user_filter = UserFilter(request.GET, queryset=product_list)
# #     return render(request, 'gui/product_search.html', {'filter': user_filter})


# def main(request):
#     products_list = Product.objects.all()
#     filter = ProductFilter(request.GET, queryset=products_list)
#     products_list = filter.qs
#     page = request.GET.get('page', 1)

#     paginator = Paginator(products_list, 12)
#     try:
#         product = paginator.page(page)
#     except PageNotAnInteger:
#         product = paginator.page(1)
#     except EmptyPage:
#         product = paginator.page(paginator.num_pages)
#     # context = {
#     #     'products_list': products_list,
#     #     'product': product,
#     #     'page': page
#     # }
#     return render(request, 'gui/main.html', {'product': product, 'filter': filter})


# def detailview(request, pk):
#     product_detail = Product.objects.get(id=pk)
#     user = Product.objects.filter(user=request.user)
#     print("user ", user)
#     context = {
#         'product_detail': product_detail,
#         'user': user
#     }
#     return render(request, 'gui/detailview.html', context)
