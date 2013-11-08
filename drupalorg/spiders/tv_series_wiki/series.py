# -*- coding: utf-8 -*-

from scrapy_parsley.scrapy_parsley2.parsley_spider import ParsleyBaseSpider
from scrapy_parsley.scrapy_parsley2.parser import Parser


class WikiSeries(ParsleyBaseSpider):
    name = "wiki_series"
    # Категория:Телесериалы_США_по_десятилетиям
    start_urls = [
        u"http://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A2%D0%B5%D0%BB%D0%B5%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B_%D0%A1%D0%A8%D0%90_%D0%BF%D0%BE_%D0%B4%D0%B5%D1%81%D1%8F%D1%82%D0%B8%D0%BB%D0%B5%D1%82%D0%B8%D1%8F%D0%BC"]
    links_parselet_categories = {"links(.mw-content-ltr:last a)": [{
                                                                       "link": "str:replace(@href, '/wiki/', 'http://ru.wikipedia.org/wiki/')"
                                                                       #"link": "@href"
                                                                   }]}
    links_parselet_next_200 = {"links(.mw-content-ltr:last a)": [{
                                                                     "link": "str:replace(@href, '/wiki/', 'http://ru.wikipedia.org/wiki/')"
                                                                     #"link": "@href"
                                                                 }]}
    items_parselet = {
        'russian_title': 'h1',
        'english_title?': 'li.interwiki-en a @title',
        'russian_wiki_unformatted_link': "#ca-view a @href",
        'english_wiki_unformatted_link': "li.interwiki-en a @href",
        'year_of_premiere': '',
    }

    def parse(self, response):  # 100
        # example: Категория:Телесериалы США по десятилетиям
        for item in self.apply_links_parselet(
                callback=self.parse_decade,
                response=response,
                override_parselet=self.links_parselet_categories):
            yield item
            #for item in self.apply_items_parselet(response):
            #    yield item

    def parse_decade(self, response):  # 10
        # example: Категория:Телесериалы США 2000-х годов
        for item in self.apply_links_parselet(
                callback=self.parse_article,
                response=response,
                override_parselet=self.links_parselet_categories):
            yield item
        for item in self.apply_links_parselet(
                callback=self.parse_article,
                response=response,
                override_parselet=self.links_parselet_next_200):
            yield item
            #for item in self.apply_items_parselet(response):
            #    yield item

    def parse_article(self, response):
        # example: Viva la Bam
        for item in self.apply_items_parselet(response, parser=Parser.REDAPPLE):
            #item.replace('english_wiki_unformatted_link', '^.*?$', '______')
            yield item
