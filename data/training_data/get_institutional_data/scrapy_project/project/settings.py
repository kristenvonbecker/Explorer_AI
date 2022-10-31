BOT_NAME = 'project'

SPIDER_MODULES = ['project.spiders']
NEWSPIDER_MODULE = 'project.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Set export encoding
# FEED_EXPORT_ENCODING = 'utf-8'

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en'
}

# Set feed configuration parameters
# FEEDS = {
#     '%(name)s.json': {
#         'format': 'json',
#         'encoding': 'utf8',
#         'store_empty': False,
#         'item_classes': [, 'myproject.items.MyItemClass2'],
#         'fields': None,
#         'indent': 2,
#         'item_export_kwargs': {
#            'export_empty_fields': True,
#         }
#     }
# }

# Enable or disable spider middlewares
#SPIDER_MIDDLEWARES = {
#    'project.middlewares.ProjectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
#DOWNLOADER_MIDDLEWARES = {
#    'project.middlewares.ProjectDownloaderMiddleware': 543,
#}

# Enable or disable extensions
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
#ITEM_PIPELINES = {
#    'project.pipelines.ProjectPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'