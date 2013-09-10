import spynner

browser = spynner.Browser()
browser.load("http://localhost/drupal7/?q=user")
browser.wk_fill('input[id=edit-name]', 'root')
browser.wk_fill('input[id=edit-pass]', 'jh8I3eC5KUbP')
browser.click("#edit-submit")
browser.wait_load(60)
browser.load('http://localhost/drupal7/?q=admin/people/permissions#module-overlay')
# browser.browse()
browser.snapshot().save('file.png')
browser.close()
