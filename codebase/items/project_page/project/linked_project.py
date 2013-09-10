from scrapy.item import Item, Field


class LinkedProject(Item):
    link_from = Field()
    link_from_reference = Field()
    link_to = Field()
    link_to_reference = Field()

    description = Field()

    title = Field()


linked_project_title_format = "Project %s linked to %s"
