ROOT_DIR = /home/ubuntu/Programs/drupal
SCRAPY_DIR = $(ROOT_DIR)/scrapy-parsley/drupalorg
LOGS_DIR = $(ROOT_DIR)/files/csv_files
CSV_DIR = $(ROOT_DIR)/files/csv_files


default:
	@echo No target specified.
	@echo Syntax: \`make projects_core.csv\`
	@echo   or \`make projects\|modules\|other\`
	@echo   or \`make all\`
	@echo 
	@echo Available spiders\:
	@echo ==================
	-@ scrapy list

$(LOGS_DIR)/%.log:
	@echo scrapy crawl $(basename $(@F)) \
		-t csv -o $(CSV_DIR)/$(basename $(@F)).csv \
		--logfile $(LOGS_DIR)/$(basename $(@F)).log

%.csv: $(LOGS_DIR)/%.log
	@echo Crawling $@...

other: 	other_contributors.csv other_top.csv
modules: modules_dependencies.csv modules_meta.csv
projects: projects_linked.csv projects_core.csv projects_description.csv 		projects_contributed.csv projects_related.csv projects_categories.csv 		projects_releases.csv

all: projects modules other

# todo: rm command