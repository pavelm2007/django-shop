from django.shortcuts import render_to_response, get_object_or_404
from catalog.models import Product, Category
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def index(request):
    return render_to_response(
        'catalog/index.html',
        {
            'product_list': Product.objects.all(),
            'nodes': Category.objects.add_related_count(Category.tree.all(),
                Product,
                'category', 'product_counts',
                cumulative=True)
        }
    )


def category(request, category_id):
    categories = Category.objects.add_related_count(
        Category.tree.all(),
        Product,
        'category', 'product_counts',
        cumulative=True
    );

    try:
        current_category = categories.get(name=category_id)
        descendants = current_category.get_descendants(include_self=True)
    except ObjectDoesNotExist:
        print("Either the category doesn't exist." + category_id)

    if settings.DEBUG:
        print " === Category page: " + current_category.__unicode__();

    return render_to_response(
        'catalog/category.html',
        {
            'product_list': Product.objects.filter(category__in=descendants),
            'current_category': current_category,
            'nodes': categories
        }
    )


def product(request, product_id):
    categories = Category.objects.add_related_count(
        Category.tree.all(),
        Product,
        'category', 'product_counts',
        cumulative=True
    );

    # looking for a product
    p = get_object_or_404(Product, name=product_id)

    if settings.DEBUG:
        print " === Product page: " + p.__unicode__();

    try:
        current_category = categories.get(pk=p.category_id)
    except ObjectDoesNotExist:
        print("Either the category doesn't exist." + p.category)

    return render_to_response('catalog/product.html',
        {'product': p,
         'current_category': current_category,
         'nodes': categories
        })
