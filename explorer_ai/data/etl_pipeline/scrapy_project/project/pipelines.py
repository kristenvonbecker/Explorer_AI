# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json


class ProjectPipeline:
    def process_item(self, item, spider):
        return item


class ExhibitPipeline:

    def process_item(self, item, spider):
        if spider.name not in ['exhibits']:
            return item
        adapter = ItemAdapter(item)
        if adapter.get('title'):
            if adapter.get('id') not in ['es', 'zht', 'fil']:
                return item
            else:
                raise DropItem(f'Non-English language in {item}')
        else:
            raise DropItem(f"Missing title in {item}")


# class GalleryPipeline:
#
#     def process_item(self, item, spider):
#         if spider.name not in ['galleries']:
#             return item
#         adapter = ItemAdapter(item)
#         if adapter.get('title'):
#             del adapter['curator_url']
#             return item
#         else:
#             raise DropItem(f"Missing title in {item}")