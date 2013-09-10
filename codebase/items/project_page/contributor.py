from scrapy.item import Item, Field


class Contributor(Item):
    uid = Field()
    name = Field()
    link = Field()

    description = Field()
    title = Field()


contributor_title_format = "Contributor uid %s"
