from catalog.models import Category
def catalog(request):
    return {
        #    'active_categories': Category.active.all(),
        #    'site_name': settings.SITE_NAME,
        #    'meta_keywords': settings.META_KEYWORDS,
        #    'meta_description': settings.META_DESCRIPTION,
        #    'request': request
    }