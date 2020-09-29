from django.urls import path, include
from products.api.views import CategoryViewSet, CategoryAPIView, ProductAPIView, api_detail_product_view, save_order, get_order, save_review, get_reviews
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('saveorder', save_order, name="saveorder"),
    path('getorder/<int:user_id>', get_order, name="getorder"),
    path('savereview', save_review, name="savereview"),
    path('productlist', ProductAPIView.as_view()),
    path('categorylist', CategoryAPIView.as_view()),
    path('getreviews/<int:product_id>', get_reviews, name="getreviews"),
    # path('CheckOutSerializer', CheckOutSerializer.as_view()),
    path('<str:pk>', api_detail_product_view, name="detail")
]
