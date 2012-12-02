from django.shortcuts import render_to_response
from catalog.models import Product, Category

# Create your views here.
def index(request):
    return render_to_response(
        'compare/index.html',
        {
            'product_list': Product.objects.all(),
            'nodes': Category.objects.add_related_count(Category.tree.all(),
                Product,
                'category', 'product_counts',
                cumulative=True)
        }
    )