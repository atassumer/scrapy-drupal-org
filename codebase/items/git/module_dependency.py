from scrapy.item import Item, Field


class ModuleDependency(Item):
    from_project_machine_name = Field()
    from_module_machine_name = Field()

    to_module_machine_name = Field()  # aka dependency

    from_project_reference = Field()
    from_module_reference = Field()
    # to_project_reference is hard to find

    from_version = Field()

    version_major = Field()
    quality = Field()

    title = Field()
    description = Field()


module_dependency_title_format = "Module %s %s-%s from project %s depends on module %s"
# third parameter is the major_version
