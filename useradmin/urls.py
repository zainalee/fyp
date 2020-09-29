from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from request_section.views import post_request
# from useradmin.views import adminstrator

urlpatterns = [
    path('', views.main, name='adminhome'),
    path('demo', views.demo, name='demo'),
    path('shop', views.shop, name='shop'),
    path('profile', views.profile, name='profile'),
    path('profile/<str:pk>', views.showprofile, name='profile'),
    path('login', views.login, name='login'),
    path('Clientlogin', views.Clientlogin, name='Clientlogin'),
    path('logout', views.logoutuser, name='logout'),
    path('products', views.products, name='products'),
    path('createproduct/', views.createproduct, name='createproduct'),
    path('updateproduct/<str:pk>', views.updateproduct, name='updateproduct'),
    path('deleteproduct/<str:pk>', views.deleteproduct, name='deleteproduct'),
    path('deleteuser/<str:pk>', views.deleteuser, name='deleteuser'),
    path('registration', views.registration, name='registration'),
    path('Clientregistration', views.ClientRegistration, name='cregister'),
    path('cart', views.cart, name='cart'),
    path('update_item', views.updateItem, name='update_item'),
    path('process_order', views.processOrder, name='process_order'),
    path('checkout', views.checkout, name="checkout"),
    path('main', views.main, name='main'),
    path('detailview/<str:pk>', views.detailview, name='detailview'),
    path('myOrders', views.myOrders, name='myorders'),
    path('updateorderforbuyer/<str:pk>',
         views.updateorderforbuyer, name='updateorderforbuyer'),
    path('selling', views.selling, name='selling'),
    path('updateorder/<str:pk>', views.updateorder, name='updateorder'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('add_to_wishlist/<str:pk>', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist_detail_view/<str:pk>', views.wishlist_detail_view,
         name='wishlist_detail_view'),
    path('wishlistdelete/<str:pk>', views.delete_wishlist,
         name='wishlistdelete'),
    path('userlist', views.users, name='userlist'),
    path('addcat', views.add_categories, name='addcat'),
    path('categories', views.categories, name='categories'),
    path('deletecat/<str:pk>', views.deletecat, name='deletecat'),
    path('feedback/<str:pk>', views.feedback, name='feedback'),
    path('mystore/<str:pk>', views.mystore, name='mystore'),
    path('orderdetails/<str:pk>', views.orderdetails, name='orderdetails'),
    path('profile_settings', views.profile_settings, name='profile_settings'),
    path('seller_product_view_details/<str:pk>',
         views.seller_product_view_details, name='seller_product_view_details'),
    path('product_deal/<str:pk>',
         views.product_deal, name='product_deal'),


    # password-reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name="password_reset_complete"),

    # request_post

]
