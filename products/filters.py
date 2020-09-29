from .models import *
from django_filters import CharFilter
import django_filters
from django import forms


class ProductFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder': 'Search...'}))

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image', 'user', 'description',
                   'price', 'quantity', 'minorder', 'slug', 'unit']
        # widgets = {
        #     'title': forms.Label(attrs={'title': "Title"})
        # }


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = OrderItem
        fields = '__all__'
