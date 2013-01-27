from django.http import HttpResponse
from django.contrib.sites.models import get_current_site

# Create your views here.
def yml(request):
    from xml.etree.ElementTree import Element, SubElement, Comment, tostring
    from core.models import Setting
    from catalog.models import Category, Product

    # loading shop settings
    shop_settings = Setting.objects.filter(is_active=True)[0]

    # creating root elements
    yml_catalog = Element('yml_catalog')
    yml_catalog.append(Comment('Generated by iSells'))
    shop = SubElement(yml_catalog, 'shop')

    # currency for site-settings
    currencies = SubElement(shop, 'currencies')
    currency = SubElement(currencies, 'currency')
    currency.set('id', shop_settings.currency)
    currency.set('rate', "1")
    currency.set('plus', "0")

    # all active categories
    categories = SubElement(shop, 'categories')
    for cat in Category.active.all():
        category = SubElement(categories, 'category')
        category.text = cat.name
        category.set('id', str(cat.pk))
        if cat.parent_id > 0 :
            category.set('parentId', str(cat.parent_id))

    # all active products
    offers = SubElement(shop, 'offers')
    current_site = get_current_site(request)
    for product in Product.active.all():
        offer = SubElement(offers, 'offer')
        offer.set('id', str(product.pk))

        #todo: find a better way to get absolute URL
        url = SubElement(offer, 'url')
        url.text = 'http://'+ current_site.domain + product.get_absolute_url()

        price = SubElement(offer, 'price')
        price.text = str(product.price)

        currency_id = SubElement(offer, 'currencyId')
        currency_id.text = str(shop_settings.currency)

        category_id = SubElement(offer, 'categoryId')
        category_id.text = str(product.category_id)

        if product.image:
            picture = SubElement(offer, 'picture')
            picture.text = 'http://'+ current_site.domain + '/' + str(product.image)

        delivery = SubElement(offer, 'delivery')
        delivery.text = "true"

        name = SubElement(offer, 'name')
        name.text = product.name

        description = SubElement(offer, 'description')
        description.text = product.description

        if product.SKU :
            SKU = SubElement(offer, 'vendorCode')
            SKU.text = product.SKU

    return HttpResponse(tostring(yml_catalog), mimetype="application/xhtml+xml")