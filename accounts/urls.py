
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render
from products.models import *
from request_section.models import *
# from django.conf.urls.static import static


def adminstrator(request):
    products = Product.objects.filter(user=request.user)
    total_products = Product.objects.filter(user=request.user).count()
    context = {
        'products': products,
        'total_products': total_products
    }
    return render(request, 'gui/admin_index.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminstrator/', adminstrator, name='adminstrator'),
    path('api-auth/', include('rest_framework.urls')),
    path('profile/', include('profiles.api.urls')),
    path('product/', include('products.api.urls')),
    path('main/', include('main.urls')),
    path('request/', include('request_section.urls')),
    path('', include('useradmin.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
