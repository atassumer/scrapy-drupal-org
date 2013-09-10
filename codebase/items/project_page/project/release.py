from scrapy.item import Item, Field


class Release(Item):
    # project
    project_machine_name = Field()
    project_machine_name_reference = Field()

    # release
    quality = Field()  # Recommended or Other or Development: ok, warning, error  # taxonomy

    version_visible = Field()  # 7.x-3.7  # title
    version_major = Field()  # taxonomy
    version_minor = Field()
    version_patch_level = Field()
    is_created_manually = Field()  # true: tag, false: branch  # taxonomy

    zip_filesize_visible = Field()  # 1.79 MB
    zip_filesize_in_bytes_approximate = Field()  # 1790000

    date_visible = Field()  # 2013-Apr-09
    # date_unixtimestamp = Field()

    notes_link = Field()  # /node/1965242

    description = Field()  # body
    title = Field()


release_title_format = "Project %s, Major release version %s, Quality %s"
