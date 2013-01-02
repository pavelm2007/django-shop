from django.shortcuts import render_to_response, get_object_or_404
from catalog.models import Product, Category
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext

def index(request):
    return render_to_response(
        'catalog/index.html',
        {
            'product_list': Product.objects.filter()[:9],
            'nodes': Category.active.all()
        },
        context_instance=RequestContext(request)
    )


def category(request, category_slug):
    categories = Category.active.all()

    try:
        current_category = categories.get(slug=category_slug)
        descendants = current_category.get_descendants(include_self=True)
    except ObjectDoesNotExist:
        print("Either the category doesn't exist." + category_slug)

    if settings.DEBUG:
        print " === Category page: " + current_category.__unicode__();

    product_list = Product.objects.filter(category__in=descendants)
    paginator = Paginator(product_list, 15) # Show 15 contacts per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)



    return render_to_response(
        'catalog/category.html',
        {
            'product_list': products,
            'current_category': current_category,
            'nodes': categories
        },
        context_instance=RequestContext(request)
    )


def product(request, product_slug):
    categories = Category.active.all()

    # looking for a product
    p = get_object_or_404(Product, slug=product_slug)

    if settings.DEBUG:
        print " === Product page: " + p.__unicode__();

    try:
        #todo: get current category from categories
        current_category = categories.get(pk=p.category_id)
    except ObjectDoesNotExist:
        print("Either the category doesn't exist." + p.category)

    return render_to_response('catalog/product.html',
        {'product': p,
         'current_category': current_category,
         'nodes': categories
        },
        context_instance=RequestContext(request)
    )
