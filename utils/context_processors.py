from django.conf import settings
def catalog(request):
    return {
        #    '/active_categories': Category.active.all(),
             'settings': settings,
        #    'meta_keywords': settings.META_KEYWORDS,
        #    'meta_description': settings.META_DESCRIPTION,
        #    'request': request
    }