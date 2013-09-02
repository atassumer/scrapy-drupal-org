structure = {
    "url": "ul.primary li:first a @href",
    "machine_name": "regexp:match(ul.primary li:first a @href, '[^/]+$')",
    "visible_name": "#page-subtitle",
    "uid": "regexp:match(.submitted a @href, '\\d+')",
    "nid": "regexp:match(id('block-project-development')//ul/li[contains(.,'commits')]/a/@href, '\\d+')",
    "image_urls?": ".imagecache",
    "info(.project-info)": [{
          "info_to": "ul"
        }],
    "issues(.issue-cockpit-categories)?": [{
          "issues_open_count": "regexp:match(.issue-cockpit-totals a:first, '\\d+')",
          "issues_total_count": "regexp:match(.issue-cockpit-totals a:last, '\\d+')",
          "bugreports_open_count": "regexp:match(.issue-cockpit-bug a:first, '\\d+')",
          "bugreports_total_count": "regexp:match(.issue-cockpit-bug a:last, '\\d+')"
        }]
}

_extractSelector = function(value) {
    var result = value
    // extract attributes
    var re = /^[\w\-]+:[\w\-]+\((.*?)\)$/
    // todo: make it in two steps: (1) extract arguments and (2) separate arguments
    var occurrences = re.exec(value)
    if (occurrences != null) {
        result = occurrences[1]
    }

    // get first attribute
    result = result.split(', ')[0]

    // separate selector from attribute
    return result.split(' @')[0]
}
console.log(_extractSelector('asdfklasjd') == 'asdfklasjd')
console.log(_extractSelector("regexp:match(.issue-cockpit-totals a:last @href, '\\d+')") == '.issue-cockpit-totals a:last')

forEach = function(el) {
    var selector = structure[el]
    if (typeof selector == 'string') {
        selector = _extractSelector(selector)
        console.log(' ')
        console.log(selector)
//        console.log($(selector).text())
        console.log($(selector).css('border', '1px solid black'))
    }
};

jQuery.each(structure, forEach)
