scrapy-drupal-org
=================

Parse Drupal.org's projects


Dependencies:
 - https://github.com/fizx/parsley
 - https://github.com/fizx/pyparsley
 - https://github.com/scrapy/scrapy

Code to integrate PyParsley into Scrapy located in `codebase.shared` package.



Main issue
================
PyParsey throws parsing errors too often. 
There are 
 - `Segmentation error` for JSON syntax errors and
 - `RuntimeError` wrapped into `ParseletException` for selector errors
 
Both of them give no information on that went wrong.

To simplify parselet development I started to make firefox extension. See `parsley-firefox` folder
