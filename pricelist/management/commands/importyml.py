import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from catalog.models import Product, Category
import urllib2, urlparse
from django.core.files.base import ContentFile
from django.conf import settings
import urllib2

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=True,
            help='Delete poll instead of closing it'),
        ) + (
        make_option('--images',
            action='store_true',
            dest='images',
            default=False,
            help='Import images from YML'),
        )
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified YML for importing'

    def handle(self, *args, **options):
        if options['delete']:
            Category.objects.all().delete();
            Product.objects.all().delete();

        for file in args:
            try:
#                if settings.DEBUG:
#                    file = '/Users/alexzaporozhets/Downloads/records.xml';
                request = urllib2.Request(file, headers={"Accept" : "application/xml"})
                file = urllib2.urlopen(request)

                tree = ET.parse(file)

            except ET.ParseError:
                raise CommandError('YML "%s" is not valid' % file)

            root = tree.getroot()

            trans_dct = {}

            # copy categories into databases
            for child in root.find('shop').find('categories'):
                category = Category(name=child.text);
                category.save()
                trans_dct[child.get('id')] = category.id;

            # setting child-parent relations
            for child in root.find('shop').find('categories'):
                # only for child elements
                if child.get('parentId') is not None:
                    # search for child a category
                    try:
                        category = Category.objects.get(pk=trans_dct[child.get('id')])
                    except Category.DoesNotExist:
                        raise CommandError('Category ID "%s" was not found' % child.get('id'))
                    pass
                    # adding relation to parent category
                    try:
                        category.parent = Category.objects.get(pk=trans_dct[child.get('parentId')])
                        category.save()
                    except Category.DoesNotExist:
                        raise CommandError('Category ID "%s" was not found' % child.get('id'))
                    pass

            self.stdout.write('Categories imported' + '\n')

            # import offers (products)
            for child in root.find('shop').find('offers'):
                description = child.find('description').text;
                if description is None:
                    description = ""

                offer = Product(
                                name=child.find('name').text,
                                price=child.find('price').text,
                                description=description,
                                category=Category.objects.get(pk=trans_dct[child.find('categoryId').text])

                );

                if options['images']:
                    # importing images from <picture>http://...</picture>
                    if child.find('picture') is not None:
                        image_data = urllib2.urlopen(child.find('picture').text, timeout=5)
                        filename = urlparse.urlparse(image_data.geturl()).path.split('/')[-1] + '.jpg'
                        offer.image = filename
                        offer.image.save(filename, ContentFile(image_data.read()), save=False)

                offer.save()

            self.stdout.write('Products imported' + '\n')

            # fix categories counters
            categories = Category.objects.all()

            for category in categories:
                category.count_products = Product.objects.filter(category__in=category.get_descendants(include_self=True)).count()
                category.save()
