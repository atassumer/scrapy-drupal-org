scrapy-drupal-org
=================

Parse Drupal.org's projects


Dependencies:
 - https://github.com/fizx/parsley
 - https://github.com/fizx/pyparsley
 - https://github.com/scrapy/scrapy

Code to integrate PyParsley into Scrapy located in `codebase.shared` package.



Tools
================
To write and debug your parselet, paste contents of `parsley-firefox/boilerplate.js` into Web Console
Usage:

```
// parselet for https://drupal.org/project/flag
json = {
    "url": "ul.primary li:nth-of-type(1) a @href",
    "machine_name": "regexp:match(ul.primary li:nth-of-type(1) a @href, '[^/]+$')",
    "visible_name": "#page-subtitle",
    "uid": "regexp:match(.submitted a @href, '\\d+')",
    "nid": "regexp:match(id('block-project-development')//ul/li[contains(.,'commits')]/a/@href, '\\d+')",
    "image_urls?": "a.imagecache @href",
    "info(.project-info)": [{
          "info_to": "ul"
        }],
    "issues(.issue-cockpit-categories)?": [{
          "issues_open_count": "regexp:match(.issue-cockpit-totals a:nth-of-type(1), '\\d+')",
          "issues_total_count": "regexp:match(.issue-cockpit-totals a:nth-of-type(2), '\\d+')",
          "bugreports_open_count": "regexp:match(.issue-cockpit-bug a:nth-of-type(1), '\\d+')",
          "bugreports_total_count": "regexp:match(.issue-cockpit-bug a:nth-of-type(2), '\\d+')"
        }]
}
new Structure(json)  // run it
```
