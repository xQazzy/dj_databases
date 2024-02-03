from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_param = request.GET.get('sort', 'name')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    phones = Phone.objects.all()
    if min_price is not None:
        phones = phones.filter(price__gte=min_price)
    if max_price is not None:
        phones = phones.filter(price__lte=max_price)

    if sort_param == 'name':
        phones = phones.order_by('name')
    elif sort_param == 'min_price':
        phones = phones.order_by('price')
    elif sort_param == 'max_price':
        phones = phones.order_by('-price')

    template = 'catalog.html'
    context = {
        'phones': phones,
        'sort_param': sort_param,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, template, context)


def show_product(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)
