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




// =====
// model
// =====


// ==============
// Selector class
// ==============

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



// ====================
// SingleSelector class
// ====================
SingleSelector.prototype = new Selector();        // Here's where the inheritance occurs
SingleSelector.prototype.constructor=SingleSelector;       // Otherwise instances of SingleSelector would have a constructor of Selector

function SingleSelector(raw_selector, root_node) {
	this.raw_selector = raw_selector;
    this.extracted_selector_array = this._extractSelector(raw_selector)
    this.root_node = typeof root_node !== 'undefined' ? root_node : document
    this.node = this._getNode()
}

SingleSelector.prototype._extractSelector = function(raw_selector) {
    var result = raw_selector
    // extract attributes
    var re = /^[\w\-]+:[\w\-]+\((.*?)\)$/
    var occurrences = re.exec(raw_selector)
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
        return this.getNode().textContent  // todo: extract text
    }
}


// ===================
// GroupSelector class
// ===================
GroupSelector.prototype = new Selector();        // Here's where the inheritance occurs
SingleSelector.prototype.constructor=GroupSelector;       // Otherwise instances of SingleSelector would have a constructor of Selector

function GroupSelector(raw_selector) {
	this.raw_selector = raw_selector;
    this.extracted_selector_array = this._extractSelector(raw_selector)
    this.root_node = document
    this.node = this._getNode()
}

GroupSelector.prototype._extractSelector = function(raw_selector) {
    var re = /\((.*?)\)/
    return re.exec(raw_selector)[1]
}




// ==========
// controller
// ==========
_forEachSelector = function(key, selector, group_node) {
    if (typeof selector == 'string') {
        var obj = new SingleSelector(selector, group_node)
        console.log(' ')
        console.log(key)
        console.log(selector)
        console.log(group_node)
        console.log(obj.extracted_selector_array)
        console.log(obj.getNode())
        console.log(obj.getValue())
    } else if (selector instanceof Array) {
        var subStructure = selector[0];
        for (var subStructureKey in subStructure) {
            obj = new GroupSelector(selector)
            group_node = obj.getNode()
            _forEachSelector(subStructureKey, subStructure[subStructureKey], group_node)
        }
    }
}

forEachSelector = function(key, selector) {
//        console.log(selector)
////        console.log($(selector).text())
//        console.log($(selector).css('border', '1px solid black'))
    _forEachSelector(key, selector);
};

jQuery.each(structure, forEachSelector)
