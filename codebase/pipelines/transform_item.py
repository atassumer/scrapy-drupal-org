import re
from codebase import settings


class TransformItemPipeline(object):
    def process_item(self, current_item, current_spider):
        self.item = current_item
        if current_spider.name == 'contributed_projects':
            self.process_contributed_projects()
        elif current_spider.name == 'releases':
            self.process_release()
        elif current_spider.name == 'related_projects':
            self.process_related_projects()
        elif current_spider.name == 'contributors':
            self.process_contributors()
        elif current_spider.name == 'linked_projects':
            self.process_linked_projects()
            # else:
        #     self.log('ERROR: UNKNOWN SPIDER TYPE')
        return self.item

    def process_contributed_projects(self):
        # self.transform_field('project_created', r'at', r'-')
        if len(self.item['images']):
            self.item['official_snapshot_full_path'] = "%s%s%s2" % (
                settings.IMAGES_STORE, 'official/', self.item['images'][0]['path'])
            del self.item['images']

    def process_release(self):
        pass

    def process_related_projects(self):
        pass

    def process_contributors(self):
        pass

    def process_linked_projects(self):
        pass

    # # regexp utility functions
    # def match(self, field_name, pattern, subgroup=0):
    #     self.item[field_name] = re.search(pattern, self.item[field_name]).group(subgroup)

    def transform_field(self, field_name, pattern, replacement):
        field_value = self.item[field_name][0]
        self.item[field_name] = [re.sub(pattern, replacement, field_value)]
        # "%s %s %s %s" % (field_name, pattern, replacement, subgroup)  #


        #
        # def process_item(self, item, spider):
        #         if item['price']:
        #             if item['price_excludes_vat']:
        #                 item['price'] = item['price'] * self.vat_factor
        #             return item
        #         else:
        #             raise DropItem("Missing price in %s" % item)
        #         return item
        #