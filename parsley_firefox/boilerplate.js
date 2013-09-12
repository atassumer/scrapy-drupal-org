/**

    USAGE


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
*/

/**
 * KNOWN ISSUES
 *
 * Firefox's implementation of CSS differs from Parsley's implementation
 * Firefox don't support EXSLT functions
 */


/**
 * Model
 */


/**
 * Class Selector
 */
//Selector.prototype.constructor=Selector;       // Otherwise instances of SingleSelector would have a constructor of Selector
function Selector() {}

Selector.prototype._getNode = function() {
    try {               // css 3
        return this.root_node.querySelector(this.extracted_selector_array[0])
    } catch (err) {     // xpath
        return document.evaluate( this.extracted_selector_array[0], this.root_node, null, XPathResult.ANY_TYPE, null).iterateNext();
    }
}

Selector.prototype._extractSelector = function() {
    console.log('ERROR: Selector._extractSelector should be overridden')
}

Selector.prototype.getNode = function() {
    return this.node
}


/**
 * Class SingleSelector
 */
SingleSelector.prototype = new Selector();        // Here's where the inheritance occurs
SingleSelector.prototype.constructor=SingleSelector;       // Otherwise instances of SingleSelector would have a constructor of Selector

function SingleSelector(raw_selector, root_node, highlight) {
    this.extracted_selector_array = this._extractSelector(raw_selector)
    this.root_node = typeof root_node !== 'undefined' ? root_node : document
    this.node = this._getNode()

    if (highlight == true) {
        var elementNode = this.node
        if (this.node instanceof Attr) {
            elementNode = elementNode.ownerElement
        }
        elementNode.style.border = "1px solid black"
    }
}

SingleSelector.prototype._extractSelector = function(raw_selector) {
    var result = raw_selector
    // extract attributes
    var re = /^[\w\-]+:[\w\-]+\((.*?)\)$/
    var occurrences = re.exec(result)
    if (occurrences != null) {
        result = occurrences[1]
    }

    // get first attribute
    result = result.split(', ')[0]

    // separate selector from attribute
    return result.split(' @')
}
//    console.log(_extractSelector('asdfklasjd') == 'asdfklasjd')
//    console.log(_extractSelector("regexp:match(.issue-cockpit-totals a:last @href, '\\d+')") == '.issue-cockpit-totals a:last')

SingleSelector.prototype.getValue = function() {
    if (this.extracted_selector_array.length == 2) {
        return this.getNode().attributes.getNamedItem(this.extracted_selector_array[1]).value
    } else {
        return this.getNode().textContent  // works in both CSS and XPath selectors
    }
}


/**
 * Class GroupSelector
 * @type {Selector}
 */
GroupSelector.prototype = new Selector();        // Here's where the inheritance occurs
GroupSelector.prototype.constructor=GroupSelector;       // Otherwise instances of SingleSelector would have a constructor of Selector

function GroupSelector(raw_group_selector) {
    this.extracted_selector_array = this._extractSelector(raw_group_selector)
    this.root_node = document
    this.node = this._getNode()
}

GroupSelector.prototype._extractSelector = function(raw_group_selector) {
    var re = /\((.*?)\)/
    return [re.exec(raw_group_selector)[1]]
}


/**
 * Controller
 */

/**
 * Class Structure
 */
function Structure(json) {
    try {
        this.parse()
    } catch (err) {
        throw 'USAGE: `new Structure(json)`'
    }
    this.json = json
    this.extracted = {}
    this.highlight = true
    this.parse()
}

Structure.prototype.parse = function() {
    for (var selectorKey in this.json) {
        this.parseSelector(selectorKey, this.json[selectorKey])
    }
}

Structure.prototype.parseSelector = function(key, selector, group_node) {
    if (typeof selector == 'string') {
        var obj = new SingleSelector(selector, group_node, this.highlight)
        this.extracted[key] = obj.getValue()
    } else if (selector instanceof Array) {
        var subStructure = selector[0]
        var root_node = new GroupSelector(key).getNode()
        for (var subStructureKey in subStructure) {
            this.parseSelector(subStructureKey, subStructure[subStructureKey], root_node)
        }
    }
}

Structure.prototype.toString = function() {
    return this.extracted
}


// USAGE: `new Structure(json)`
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


// new Structure(json)
