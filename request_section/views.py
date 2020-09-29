from django.shortcuts import render, redirect
from .models import *
from templates.gui.forms import PostRequestForm, SendOfferForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Subquery
# Create your views here.


def post_request(request):
    form = PostRequestForm()
    if request.method == 'POST':
        form = PostRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success = (request, 'Post Created Successfully')
            return redirect('adminhome')
    context = {
        'form': form
    }
    return render(request, 'sellerprofile/postrequest.html', context)


def my_request(request):
    myrequest = PostRequest.objects.filter(user=request.user)
    total_offers = Comment.objects.filter(
        post_id__in=Subquery(myrequest.values('id'))).count()
    print(total_offers)
    context = {
        'myrequest': myrequest,
        'total_offers': total_offers
    }
    return render(request, 'sellerprofile/myrequest.html', context)


def view_offers(request, pk):
    myrequest = PostRequest.objects.filter(id=pk)
    total_offers = Comment.objects.filter(
        post_id__in=Subquery(myrequest.values('id'))).count()
    offers = Comment.objects.filter(
        post_id__in=Subquery(myrequest.values('id')))
    print(total_offers)
    context = {
        'myrequest': myrequest,
        'total_offers': total_offers,
        'offers': offers
    }
    return render(request, 'sellerprofile/viewoffers.html', context)


def deleterequest(request, pk):
    myrequest = PostRequest.objects.get(id=pk)
    if request.method == 'POST':
        myrequest.delete()
        return redirect('myrequests')
    context = {
        'myrequest': myrequest
    }
    return render(request, 'sellerprofile/deleterequest.html', context)


def requestfeed(request):
    requests = PostRequest.objects.all()
    total_requests = PostRequest.objects.all().count()
    context = {
        'requests': requests,
        'total_requests': total_requests
    }
    return render(request, 'gui/requestfeed.html', context)


def sendoffer(request, pk):
    requests = PostRequest.objects.get(id=pk)
    form = SendOfferForm()
    if request.method == 'POST':
        form = SendOfferForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            contact_number = form.cleaned_data['contact_number']
            offer = Comment()
            offer.post = requests
            offer.description = description
            offer.price = price
            offer.contact_number = contact_number
            offer.user = request.user
            offer.save()
            messages.success(request, "Offer Sent Successfully")
            return redirect('requestfeed')
    context = {
        'requests': requests,
        'form': form
    }
    return render(request, 'gui/sendoffer.html', context)
