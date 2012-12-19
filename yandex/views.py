import xml.etree.ElementTree as ET

# Create your views here.
def index(request):
    tree = ET.parse('/Users/alexzaporozhets/Downloads/records.xml')
    root = tree.getroot()
    for child in root.find('shop').find('categories'):
        print child.text