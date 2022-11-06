from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders import exhibits, galleries

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(exhibits)
process.crawl(galleries)
process.start()