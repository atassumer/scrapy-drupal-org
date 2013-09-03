#################
# scrapy settings
#################
SPIDER_MODULES = ['codebase.spiders']
NEWSPIDER_MODULE = 'codebase.spiders'
DEFAULT_ITEM_CLASS = 'scrapy.item.Item'

HTTPCACHE_ENABLED = True
HTTPCACHE_STORAGE = 'scrapy.contrib.downloadermiddleware.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = '/home/ubuntu/Programs/drupal/files/cached_pages'

IMAGES_MIN_HEIGHT = 110
IMAGES_STORE = '/home/ubuntu/Programs/drupal/files/images'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 965,
}

ITEM_PIPELINES = [
    # 'scrapy.contrib.pipeline.images.ImagesPipeline',
    'codebase.pipelines.git_clone.GitClonePipeline',
    # 'codebase.pipelines.original_image.OriginalImagesPipeline',
    # 'codebase.pipelines.transform_item.TransformItemPipeline',
]


#################
# custom settings
#################
C_CODEBASE_ROOT = "/home/ubuntu/Programs/drupal/scrapy-parsley/codebase"

C_GIT_ROOT = "/home/ubuntu/Programs/drupal/files/git"
C_PROJECTS_ROOTS = [
    C_GIT_ROOT,
    C_GIT_ROOT + '/drupal/modules'
]

C_TARGET_VERSION = 6  # todo: make it dynamic
C_TARGET_QUALITY = 'ok'

C_PAGES_LIMIT = 5  # how many pages to crawl
