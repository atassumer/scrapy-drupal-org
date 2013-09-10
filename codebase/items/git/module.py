from scrapy.item import Item, Field


class Module(Item):  # based on file.info

    project_machine_name = Field()
    project_reference = Field()
    module_machine_name = Field()
    version_major = Field()
    quality = Field()

    info_name = Field()  # visible name
    info_version = Field()
    info_description = Field()
    info_screenshot = Field()
    info_core = Field()
    info_engine = Field()
    info_base_theme = Field()
    info_regions = Field()
    info_features = Field()
    info_theme_settings = Field()
    info_stylesheets = Field()
    info_scripts = Field()
    info_php = Field()
    info_package = Field()
    info_hidden = Field()
    info_required = Field()
    info_configure = Field()

    title = Field()
    description = Field()


module_title_format = "Module %s %s-%s from project %s"
