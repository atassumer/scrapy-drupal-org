#################
# scrapy settings
#################
SPIDER_MODULES = ['codebase.spiders']
NEWSPIDER_MODULE = 'codebase.spiders'
DEFAULT_ITEM_CLASS = 'scrapy.item.Item'

HTTPCACHE_ENABLED = True
# HTTPCACHE_STORAGE = 'scrapy.contrib.downloadermiddleware.httpcache.FilesystemCacheStorage'  # old path
HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.FilesystemCacheStorage'  # new path
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
    'codebase.pipelines.projects_contributed_git_clone.ProjectsContributedGitClonePipeline',
    # 'codebase.pipelines.original_image.OriginalImagesPipeline',
    # 'codebase.pipelines.transform_item.TransformItemPipeline',
]


#################
# custom settings
#################
C_CODEBASE_ROOT = "/home/ubuntu/Programs/drupal/scrapy-parsley/codebase"

C_CONTRIBUTED_PROJECTS_ROOT = "/home/ubuntu/Programs/drupal/files/git"
C_CORE_PROJECTS_ROOT = C_CONTRIBUTED_PROJECTS_ROOT + '/drupal/modules'

C_SUPPORTED_MAJOR_VERSIONS = [6, 7]

# C_PAGES_LIMIT = 5  # how many pages to crawl
