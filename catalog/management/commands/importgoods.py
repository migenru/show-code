from django.core.management.base import BaseCommand, CommandError
import io
import lxml.etree as ET
import requests
from .etl import extract_goods, extract_price, load_category, load_goods

goods = dict()
url_import = 'cml/import0_1.xml'
url_offers = 'cml/offers0_1.xml'

content = requests.get(url_import).content  # контент с товаром и группами
content_price = requests.get(url_offers).content  # контент с ценами
tree = ET.parse(io.BytesIO(content))  # дерево с товаром и группами
tree_price = ET.parse(io.BytesIO(content_price))  # дерево с ценами
menu = []
nms = {'ns': 'urn:1C.ru:commerceml_2'}


class Command(BaseCommand):
    help = 'ETL 1C to db shop'

    def add_arguments(self, parser):
        parser.add_argument('good_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        extract_goods()
        extract_price()
        load_category()
        load_goods()

        self.stdout.write(self.style.SUCCESS('Successfully add "%s" goods' % len(goods)))