from django.shortcuts import render_to_response
from catalog.models import Product, Category

# Create your views here.
def index(request):
    return render_to_response(
        'cart/index.html',
        {
            'product_list': Product.objects.all(),
            'nodes': Category.active.all()
        }
    )