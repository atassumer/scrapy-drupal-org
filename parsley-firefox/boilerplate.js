// https://drupal.org/project/flag
structure = {
    "url": "ul.primary li:nth-of-type(1) a @href",
    "machine_name": "regexp:match(ul.primary li:nth-of-type(1) a @href, '[^/]+$')",
    "visible_name": "#page-subtitle",
    "uid": "regexp:match(.submitted a @href, '\\d+')",
    "nid": "regexp:match(id('block-project-development')//ul/li[contains(.,'commits')]/a/@href, '\\d+')",
    "image_urls?": ".imagecache",
    "info(.project-info)": [{
          "info_to": "ul"
        }],
    "issues(.issue-cockpit-categories)?": [{
          "issues_open_count": "regexp:match(.issue-cockpit-totals a:nth-of-type(1), '\\d+')",
          "issues_total_count": "regexp:match(.issue-cockpit-totals a:last, '\\d+')",
          "bugreports_open_count": "regexp:match(.issue-cockpit-bug a:nth-of-type(1), '\\d+')",
          "bugreports_total_count": "regexp:match(.issue-cockpit-bug a:last, '\\d+')"
        }]
}

// Known issues: Firefox's implementation of CSS differs from Parsley's implementation

_extractSingleSelector = function(value) {
    var result = value
    // extract attributes
    var re = /^[\w\-]+:[\w\-]+\((.*?)\)$/
    var occurrences = re.exec(value)
    if (occurrences != null) {
        result = occurrences[1]
    }

    // get first attribute
    result = result.split(', ')[0]

    // separate selector from attribute
    return result.split(' @')
}
console.log(_extractSingleSelector('asdfklasjd') == 'asdfklasjd')
console.log(_extractSingleSelector("regexp:match(.issue-cockpit-totals a:last @href, '\\d+')") == '.issue-cockpit-totals a:last')

_extractGroupSelector = function(value) {
    var re = /\((.*?)\)/
    return re.exec(value)[1]
}

_applySelector = function(selector) {
    try {
        return document.querySelector(selector)
    } catch (err) {
        return $x(selector)
    }
}

_extractValue = function(selector) {
    var selection = _applySelector(selector[0])
    if (selector[1]) {
        return selection.attributes.getNamedItem(selector[0])
    } else {
        return selector
    }
}

_forEachSelector = function(key, selector, group_selector) {
    if (typeof selector == 'string') {
        selector = _extractSingleSelector(selector)
        console.log(' ')
        console.log(key)
        console.log(selector)
        console.log(group_selector)
        console.log(_extractValue(selector))
    } else if (selector instanceof Array) {
        var subStructure = selector[0];
        for (var subStructureKey in subStructure) {
            group_selector = _extractGroupSelector(key)
            _forEachSelector(subStructureKey, subStructure[subStructureKey], group_selector)
        }
    }
}

forEachSelector = function(key, selector) {
//        console.log(selector)
////        console.log($(selector).text())
//        console.log($(selector).css('border', '1px solid black'))
    _forEachSelector(key, selector, "root");
};

jQuery.each(structure, forEachSelector)
