# -*- coding: utf-8 -*-

# Scrapy settings for ViVoSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ViVoSpider'

SPIDER_MODULES = ['ViVoSpider.spiders']
NEWSPIDER_MODULE = 'ViVoSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ViVoSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# 数据存入 mongodb 时的一些配置
MONGO_IP = "localhost"  # mongodb ip
MONGO_PORT = 27017  # mongodb 端口
MONGO_DB_NAME = "f_vivo"   # mongodb 数据库名称
MONGO_URL = "mongodb://admin:admin@IP:Port"    # mongodb URL   存储数据主要是根据它来定数据库位置的
RESULT_COLLECTIONS_NAME = "vivo_result"  # 表名


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ViVoSpider.middlewares.VivospiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ViVoSpider.middlewares.VivospiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #'ViVoSpider.pipelines.VivospiderPipeline': 300,
   'ViVoSpider.pipelines.ResultMongoPipeline': 300,
   #'scrapy_redis.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 分布式爬虫添加的配置信息
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"   # 使用scrapy_redis 里的去重组件，不使用scrapy默认的去重方式
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用scrapy_redis 里的调度器组件，不使用默认的调度器
SCHEDULER_PERSIST = True    # 允许暂停，redis请求记录不丢失
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"    # 默认使用scrapy_redis请求队列形式（优先级）
# 队列形式，请求先进先出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# 栈形式，请求先进后出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
LOG_LEVEL = 'DEBUG'     # 日志级别
REDIS_HOST = '127.0.0.1'    # 连接本机
REDIS_PORT = '6379'   # 端口
REDIS_PARAMS = {
    'password': 'pengfeiQDS',
    'db': 0
}       # 密码一般不设置，使用数据0
