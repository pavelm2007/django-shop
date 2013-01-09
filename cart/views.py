from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from cart.forms import OrderFormSimple
from cart.models import Order, OrderItem
from catalog.models import Product
from catalog.models import Category
from pprint import pprint
from utils.functions import get_client_ip
import json

def index(request):
    nodes = Category.active.all()
    return render_to_response('cart/index.html', locals(), context_instance=RequestContext(request))


def simple(request):
    if request.method == 'POST':
        form = OrderFormSimple(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            # parsing products items
            order_items = json.loads(form.cleaned_data['items'])

            if settings.DEBUG:
                print " === Order data === "
                pprint(form.cleaned_data)
                print " === Order items === "
                pprint(order_items)

            # saving order
            order = Order(
                shipping_name=form.cleaned_data['name'],
                billing_name=form.cleaned_data['name'],

                shipping_city=form.cleaned_data['city'],
                billing_city=form.cleaned_data['city'],

                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],

                ip_address = get_client_ip(request)
            )
            order.save()

            # saving order products
            for item in order_items:
                order_item = OrderItem(
                    product = Product.objects.get(pk=item['product']),
                    quantity = int(item['quantity']),
                    price = Product.objects.get(pk=item['product']).price,
                    order = order
                ).save()

            return HttpResponseRedirect('/cart/thanks/' + str(order.pk)) # Redirect after POST
    else:
        form = OrderFormSimple() # by default Standard

    nodes = Category.active.all()
    return render_to_response('cart/one_step_simple.html', locals(), context_instance=RequestContext(request))

def thanks(request):
    nodes = Category.active.all()
    return render_to_response('cart/thanks.html', locals(), context_instance=RequestContext(request))
