from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_dict = {'id': 'id', 'name': 'name', 'min_price': 'price', 'max_price': '-price'}
    template = 'catalog.html'
    sort = request.GET.get('sort', 'id')
    phones = Phone.objects.all().order_by(sort_dict[sort])
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
