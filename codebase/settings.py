# Scrapy settings for drupalorg project

SPIDER_MODULES = ['codebase.spiders']
NEWSPIDER_MODULE = 'codebase.spiders'
DEFAULT_ITEM_CLASS = 'codebase.items.project_page.project.project.Project'

# DEPTH_LIMIT = 2

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 965
}

HTTPCACHE_ENABLED = True
HTTPCACHE_STORAGE = 'scrapy.contrib.downloadermiddleware.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = '/media/ubuntu/fad36a44-712c-44d4-bb85-7a2dd8584a0a/etc/drupal/scrapy-drupal-org/cached_pages/'

ITEM_PIPELINES = [
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    # 'codebase.pipelines.original_image.OriginalImagesPipeline',
    'codebase.pipelines.transform_item.TransformItemPipeline',
]

IMAGES_STORE = '/usr/share/drupal7/sites/default/files/images/'
IMAGES_MIN_HEIGHT = 110