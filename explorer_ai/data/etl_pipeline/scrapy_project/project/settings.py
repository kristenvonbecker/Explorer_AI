BOT_NAME = 'project'

SPIDER_MODULES = ['project.spiders']
NEWSPIDER_MODULE = 'proejct.spiders'

ROBOTSTXT_OBEY = True
COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en'
}

ITEM_PIPELINES = {
  'project.pipelines.ProjectPipeline': 300,
  'project.pipelines.ExhibitPipeline': 500,
  'project.pipelines.GalleryPipeline': 700,
}

FEEDS = {
    'file://../../cache/raw/%(name)s.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 2,
        'overwrite': True,
    }
}

#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
