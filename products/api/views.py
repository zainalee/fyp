from products.models import Product, Categories, OrderItem, Order, ShippingAddress, Review
from rest_framework import viewsets
from .serializers import ProductSerializers, CategoriesSerializers
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import SearchFilter, OrderingFilter
import json
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime


#  {ListAPIView,
# RetrieveAPIView,
# CreateAPIView,
# DestroyAPIView,
# UpdateAPIView}


@api_view(['GET', ])
def api_detail_product_view(request, pk):

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": status.HTTP_404_NOT_FOUND})

    if request.method == 'GET':
        serializer = ProductSerializers(product)
        return Response({
            "status": status.HTTP_200_OK,
            "result": serializer.data,
        })


class ProductAPIView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title']


@api_view(['POST'])
def save_order(request):
    try:
        data = json.loads(request.body)
        user = User.objects.get(id=data.get('user_id'))
        order = Order.objects.create(
            user=user,
            complete=1
        )
        ShippingAddress.objects.create(
            order=order,
            zipcode=data.get('zipcode'),
            state=data.get('state'),
            address=data.get('address'),
            city=data.get('city'),
        )
        for order_item in data.get('products'):
            OrderItem.objects.create(
                user=user,
                order=order,
                quantity=order_item.get('quantity'),
                price=order_item.get('price'),
                product=Product.objects.get(id=order_item.get('product_id')),
            )
        return Response({
            "message": "Order created successfully",
            'code': status.HTTP_200_OK
        })
    except Exception as e:
        return Response({
            '"message': str(e),
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR
        })


@api_view(['GET'])
def get_order(request, user_id):
    order_details = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from products_order WHERE user_id = %s", [user_id])
            row = cursor.fetchall()
        for data in row:
            db_json = {}
            db_json.update({'order_id': data[0]})
            db_json.update({'date_created': data[1]})
            db_json.update({'complete': data[2]})
            db_json.update({'user_id': data[4]})
            with connection.cursor() as cursor1:
                cursor1.execute(
                    "select * from products_orderitem INNER JOIN products_product on products_orderitem.product_id=products_product.id  WHERE order_id = %s", [data[0]])
                products = cursor1.fetchall()
            db_json.update({'products': []})
            total_price = 0
            for product in products:
                total_price += product[3]
                product_json = {}
                product_json.update({'quantity': product[1]})
                product_json.update({'price': product[3]})
                product_json.update({'product_id': product[5]})
                product_json.update({'unit': product[8]})
                product_json.update({'title': product[9]})
                product_json.update({'slug': product[15]})
                product_json.update({'image': product[14]})
                db_json['products'].append(product_json)
            db_json.update({'total_price': total_price})
            with connection.cursor() as cursor0:
                cursor0.execute(
                    "select * from products_shippingaddress WHERE order_id = %s", [data[0]])
                shipping_address = cursor0.fetchone()
            if shipping_address:
                db_json.update({'address': shipping_address[2]})
                db_json.update({'city': shipping_address[3]})
                db_json.update({'state': shipping_address[4]})
                db_json.update({'zipcode': shipping_address[5]})
            order_details.append(db_json)
        return Response({
            "message": "Success",
            "status": status.HTTP_200_OK,
            "orders": order_details,
        })
    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        })


@api_view(['POST'])
def save_review(request):
    try:
        data = json.loads(request.body)
        product = Product.objects.get(id=data.get('product_id'))
        Review.objects.create(
            product=product,
            user_name=data.get('user_name'),
            comment=data.get('comment'),
            rating=data.get('rating'),
            pub_date=datetime.now()
        )
        return Response({"message": "Review added successfully successfully", 'code': 200})
    except Exception as e:
        return Response({'"message': str(e), 'code': 500})


@api_view(['GET'])
def get_reviews(request, product_id):
    review_details = []
    try:
        product = Product.objects.get(id=product_id)
        reviews = Review.objects.all().filter(product=product)
        for review in reviews:
            db_json = {}
            db_json.update({'user_name': review.user_name})
            db_json.update({'rating': review.rating})
            db_json.update({'comment': review.comment})
            db_json.update({'pub_date': review.pub_date})
            review_details.append(db_json)
        return Response({"reviews": review_details, 'code': 200})
    except Exception as e:
        return Response({"message": str(e), 'code': 500})


class CategoryAPIView(ListAPIView):
    def list(self, request):
        queryset = Categories.objects.all()
        serializer = CategoriesSerializers(queryset, many=True)
        if serializer.data is None:
            return Response({
                "message": "Data Not Found"
            })
        else:
            return Response({
                "message": "success",
                "status": status.HTTP_200_OK,
                "Record": serializer.data
            })


# class ProductViewSet(viewsets.ModelViewSet):
#     pass
    #     search_fields = ['title']
    #     filter_backends = (filters.SearchFilter,)
    #     serializer_class = ProductSerializers
    #     queryset = Product.objects.all()
    #  def get_queryset(self):
    #         user = self.request.user
    #     return user.purchase_set.all()
    #     message = "success"
    #     return Response({
    #         "message": message,
    #         "status": status.HTTP_201_CREATED,
    #         "Record": serializer,
    #     })
    # permission_classes = []

    # def get (self,request, *args, **kwargs):
    #     if request.method =='GET':
    #         snippets = Product.objects.all()
    #         serializer = ProductSerializers(snippets, many=True)
    #         return Response(serializer.data)

    #     if request.method == 'POST':
    #         serializer = ProductSerializers(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response (
    #             {
    #             "message":"Success",
    #             "status" : 200,
    # "result": ax.data,
    # "result_count" : qs.count()

    # })
    # elif:
    #     return Response(
    #     {
    #         'message':fail,
    #         "status" : 400,
    #     }
    # )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializers
    queryset = Categories.objects.all()


# @api_view(['GET', ])
# def checkout(request)

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     if queryset == "":
    #         message = "no data avaialable"
    #         return Response({"error": status.HTTP_204_NO_CONTENT})

    # def list(self, request):
    #     if self.filter_backends == '':
    #         return self.response
    # print(filter_backends)
    # print(search_fields)

    # def list(self, request):
    #     filter_backends = (SearchFilter)
    #     search_fields = ['title', 'category']
    #     queryset = Product.objects.all()
    #     serializer = ProductSerializers(queryset, many=True)
    #     message = "success"
    #     return Response({
    #         "message": message,
    #         "status": status.HTTP_201_CREATED,
    #         "Record": serializer.data
    #     })

    # def get_queryset(self, *args, **kwargs):
    #     queryset_list = Product.objects.all()
    #     query = self.request.GET.get("q")
    #     if query:
    #         queryset_list = queryset_list.filter(
    #             Q(title__icontains=query)
    #         ).distinct()
    #     return queryset_list
    # return Response({
    #     "message": "success",
    #     "status": status.HTTP_201_CREATED,
    #     "Record": queryset_list
    # })

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     filter_backends = (SearchFilter, OrderingFilter)
    #     search_fields = ['title']
    #     return
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
