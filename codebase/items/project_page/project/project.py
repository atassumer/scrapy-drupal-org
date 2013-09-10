import re
from scrapy.item import Item, Field


def apply_regexp_to_description(needle, haystack):
    """
    >>> apply_regexp_to_description("(\w)", "abc")
    'a'
    >>> apply_regexp_to_description("([a-z])", "1461")
    '1461'
    """
    match = re.search(needle, haystack)
    if match:
        return match.group(1)
    else:  # occurs in core_projects.py
        return haystack


def description_serializer(description_list):
    """
    >>> description_list = ["beginning <p>first block</p> <p>second block</p> end"]
    >>> description_serializer(description_list)
    '<p>first block</p> <p>second block</p> end'
    >>> description_list = ['content <h3 id="downloads"> downloads']
    >>> description_serializer(description_list)
    'content '
    >>> description_list = ['<p>Filters content in preparation for display.</p><p><strong>Included in Drupal Core</strong></p>']
    >>> description_serializer(description_list)
    '<p>Filters content in preparation for display.</p><p><strong>Included in Drupal Core</strong></p>'
    """
    marker_start = re.escape('<p>')
    regexp_start = "(%s.+)$" % marker_start
    marker_end = re.escape('<h3 id="downloads">')
    regexp_end = "^(.+)%s" % marker_end
    description = description_list[0].encode('utf-8').replace("\n", " ")  # todo: multiline regexp
    description = apply_regexp_to_description(regexp_start, description)
    description = apply_regexp_to_description(regexp_end, description)
    return description


class Project(Item):
    machine_name = Field()  # Title
    visible_name = Field()
    url = Field()
    nid = Field()  # node id
    uid = Field()  # user id
    uid_reference = Field()
    project_created = Field()
    project_modified = Field()
    latest_scraping_unixtime = Field()
    node_alias = Field()

    maintenance_status = Field()  # https://drupal.org/node/1066982  # taxonomy
    development_status = Field()  # taxonomy
    reported_installs_count = Field()
    downloads_count = Field()
    automated_tests_enabled = Field()  # taxonomy

    issues_open_count = Field()
    issues_total_count = Field()
    bugreports_open_count = Field()
    bugreports_total_count = Field()
    new_issues_count = Field()
    participants_count = Field()

    top_position = Field()  # taxonomy

    title = Field()  # (machine_name)
    # global description_serializer
    description = Field(serializer=description_serializer)  # Body

    image_urls = Field()
    images = Field()
    official_snapshot_full_path = Field()  # extracted from `images` and prefixed with root directory path


# the only content type promoted to the front page
project_title_format = "%s"  # no additional words for SEO purposes

# todo: add taxonomy of all modules which are higher in the tree
