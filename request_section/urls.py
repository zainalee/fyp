from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# from useradmin.views import adminstrator

urlpatterns = [
    path('post', views.post_request, name="post"),
    path('myrequests', views.my_request, name='myrequests'),
    path('deleterequest/<str:pk>', views.deleterequest, name='deleterequest'),
    path('requestfeed', views.requestfeed, name='requestfeed'),
    path('sendoffer/<str:pk>', views.sendoffer, name='sendoffer'),
    path('view_offers/<str:pk>', views.view_offers, name='view_offers'),
]
