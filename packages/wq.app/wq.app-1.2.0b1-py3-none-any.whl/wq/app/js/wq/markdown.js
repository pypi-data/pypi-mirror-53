/*
 * wq.app v1.2.0b1 - @wq/markdown 1.2.0-beta.1
 * Markdown and syntax highlighting for @wq/app
 * (c) 2013-2019, S. Andrew Sheppard
 * https://wq.io/license
 */

define(['marked', 'highlight'], function (marked, _highlight) { 'use strict';

marked = marked && marked.hasOwnProperty('default') ? marked['default'] : marked;
_highlight = _highlight && _highlight.hasOwnProperty('default') ? _highlight['default'] : _highlight;

var md = {};

md.init = function (config) {
    if (!config) {
        config = {};
    } // Default variable names


    if (!config.output) {
        config.output = 'html'; // Look for {{html}} in template
    }

    if (!config.input) {
        config.input = 'markdown'; // Replace w/parse(this.markdown)
    }

    md.config = config;
};

md.context = function (context) {
    var output = '';

    if (context[md.config.input]) {
        output = md.parse(context[md.config.input]);
    }

    var result = {};
    result[md.config.output] = output;
    return result;
}; // Parsing function (can be used directly)


md.parse = function (value) {
    return md.postProcess(marked.parse(value));
}; // Override with custom post-processing function


md.postProcess = function (html) {
    if (md.config.postProcess) {
        return md.config.postProcess(html);
    } else {
        return html;
    }
}; // Connect markdown processor to code highlighter


marked.setOptions({
    highlight: function highlight(code, lang) {
        return _highlight.highlight(lang, code).value;
    }
}); // Run for server-rendered markdown

md.run = function ($page) {
    $page.find('pre code:not(.hljs)').each(function (i, el) {
        _highlight.highlightBlock(el);
    });
};

return md;

});
//# sourceMappingURL=markdown.js.map
