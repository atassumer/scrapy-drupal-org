from codebase.shared.spiders.parselet.parsley_spiders import ParsleySpider


class YelpParsleySpider(ParsleySpider):
    name = 'yelp'
    allowed_domains = ["www.yelp.com"]
    start_urls = ["http://www.yelp.com/biz/amnesia-san-francisco"]
