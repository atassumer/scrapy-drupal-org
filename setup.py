from setuptools import setup, find_packages

setup(
    name='codebase',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = codebase.settings']},
)
# todo: rename `codebase` to `source_code`
