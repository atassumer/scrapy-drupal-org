##################
# parsley_wrappers settings
##################
PARSLEY_CRAWLER_ROOT = "/home/ubuntu/Programs/drupal/scrapy-parsley/drupalorg"
PARSLEY_FILES_ROOT = "/home/ubuntu/Programs/drupal/files"


#################
# scrapy_wrappers settings
#################
SPIDER_MODULES = ['drupalorg.spiders']
NEWSPIDER_MODULE = 'drupalorg.spiders'
DEFAULT_ITEM_CLASS = 'scrapy_wrappers.item.Item'

HTTPCACHE_ENABLED = True
#HTTPCACHE_STORAGE = 'scrapy_wrappers.contrib.downloadermiddleware.httpcache.FilesystemCacheStorage'  # old path
HTTPCACHE_STORAGE = 'scrapy_wrappers.contrib.httpcache.FilesystemCacheStorage'  # new path
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = PARSLEY_FILES_ROOT + '/cached_pages'

IMAGES_MIN_HEIGHT = 110
IMAGES_STORE = PARSLEY_FILES_ROOT + '/images'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_wrappers.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 543,
    'scrapy_wrappers.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 965,
}

ITEM_PIPELINES = {
    # 'scrapy_wrappers.contrib.pipeline.images.ImagesPipeline': 100,
    'drupalorg.pipelines.projects_contributed_git_clone.ProjectsContributedGitClonePipeline': 200,
    # 'drupalorg.pipelines.original_image.OriginalImagesPipeline': 300,
    # 'drupalorg.pipelines.transform_item.TransformItemPipeline': 400,
}


###########################
# project-specific settings
###########################
PARSLEY_CONTRIBUTED_PROJECTS_ROOT = PARSLEY_FILES_ROOT + '/git'
PARSLEY_CORE_PROJECTS_ROOT = PARSLEY_CONTRIBUTED_PROJECTS_ROOT + '/drupal/modules'

PARSLEY_SUPPORTED_MAJOR_VERSIONS = [6, 7]
PARSLEY_GIT_TAGS_CSV_PATH = PARSLEY_FILES_ROOT + '/projects_releases.csv'
