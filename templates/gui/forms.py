from django import forms
from profiles.models import ClientProfile, SellerProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from products.models import Product, Review, Categories, Order, OrderItem
from request_section.models import *
from django.utils.translation import ugettext_lazy


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This Email Already exist.')
        return email

    def save(self, commit=False):
        user = super().save()

        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SellerFrom(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['city', 'address', 'state', 'shop_name', 'mobileNo']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        help_texts = {
            'username': None,
        }


class CLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        help_texts = {
            'username': None,
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price',
                  'quantity', 'category', 'minorder', 'image', 'unit', 'delivery_days', 'max_delivery_days', 'stock_status']


class DealProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['deal_price', 'deal_status']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 40, 'rows': 5})
        }


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'


class PostRequestForm(forms.ModelForm):
    class Meta:
        model = PostRequest
        fields = '__all__'
        exclude = ['user']


class SendOfferForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['post', 'user']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5})
        }
        description = forms.CharField(
            label='description',
            widget=forms.Textarea(attrs={'placeholder': '1234 Main St'})
        )


class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_orderd', 'complete',
                   'transaction_id', 'user_id', 'user', 'statusforbuyer']


class StatusForbuyerForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_orderd', 'complete',
                   'transaction_id', 'user_id', 'user', 'status']


class UpdateOrderItemStatusForSllerForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']
        # exclude = ['date_orderd', 'complete',
        #            'transaction_id', 'user_id', 'user', 'statusforbuyer']


class UpdateOrderItemStatusForBuyerForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['statusforbuyer']


class UploadProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = '__all__'
        exclude = ['user']
