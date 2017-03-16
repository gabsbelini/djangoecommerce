from django.shortcuts import render

from .models import Product
# Create your views here.

def product_list(request):
    context = {
        'product_list': Product.objects.all()
    }
    return render(request, 'catalog/product_list.html', context)
