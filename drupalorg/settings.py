##################
# parsley settings
##################
PARSLEY_CRAWLER_ROOT = "/media/ubuntu/39bb3d82-6f8a-414b-8005-2528f35107cd/ubuntu/Programs/drupal/scrapy-parsley/drupalorg"
PARSLEY_FILES_ROOT = "/media/ubuntu/39bb3d82-6f8a-414b-8005-2528f35107cd/ubuntu/Programs/drupal/files"


#################
# scrapy settings
#################
SPIDER_MODULES = ['drupalorg.spiders']
NEWSPIDER_MODULE = 'drupalorg.spiders'
DEFAULT_ITEM_CLASS = 'scrapy.item.Item'

HTTPCACHE_ENABLED = True
#HTTPCACHE_STORAGE = 'scrapy.contrib.downloadermiddleware.httpcache.FilesystemCacheStorage'  # old path
HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.FilesystemCacheStorage'  # new path
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = PARSLEY_FILES_ROOT + '/cached_pages'

IMAGES_MIN_HEIGHT = 110
IMAGES_STORE = PARSLEY_FILES_ROOT + '/images'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 965,
}

ITEM_PIPELINES = {
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 100,
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
