# from twisted.internet import reactor
# from scrapy.crawler import Crawler
# from scrapy.settings import Settings
# from scrapy import log, signals
# from drupalorg.spiders.remote.projects import RelatedProjectsRemoteParsleySpider
#
#
# class RunScrapyFromScript:
#     items = []
#
#     def __init__(self):
#         crawler = Crawler(Settings())
#         crawler.configure()
#         # spider = crawler.spiders.create(spider_name)
#         # print crawler.spiders._spiders  # {}
#         crawler.signals.connect(self.process_item, signal=signals.item_scraped)
#         crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
#         crawler.crawl(RelatedProjectsRemoteParsleySpider())
#         crawler.start()
#         log.start()
#         log.msg('Running reactor...')
#         reactor.run()  # the script will block here until the spider is closed
#         log.msg('Reactor stopped.')
#         log.msg("items: %s" % self.items)
#
#     def process_item(self, item, response, spider):
#         print item
#         print response
#         print spider
#         self.items.append(item)
#         log.msg(item)
#
#
#         # import yappi
#         # yappi.start()
#         # RunScrapyFromScript()
#         # yappi.print_stats(sort_type=yappi.SORTTYPE_TSUB, sort_order=yappi.SORTORDER_DESC, limit=50)
#
#         # cProfile.run('RunScrapyFromScript()')