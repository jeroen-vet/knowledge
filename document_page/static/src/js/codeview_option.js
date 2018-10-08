odoo.define('document_page.codeview_option', function(require) {

"use strict";
var core = require('web.core');
var session = require('web.session');
var summernote = require('web_editor.summernote');
var transcoder = require('web_editor.transcoder');

var QWeb = core.qweb;
var backend = require('web_editor.backend');
var _t = core._t;

backend.FieldTextHtmlSimple.include({
    _config: function () {
        var self = this;
        var config = {
            'focus': false,
            'height': 180,
            'toolbar': [
                ['style', ['style']],
                ['font', ['bold', 'italic', 'underline', 'clear']],
                ['fontsize', ['fontsize']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture']],
                ['history', ['undo', 'redo']]
            ],
            'prettifyHtml': false,
            'styleWithSpan': false,
            'inlinemedia': ['p'],
            'lang': "odoo",
            'onChange': function (value) {
                self.internal_set_value(value);
                self.trigger('changed_value');
            }
        };
        if (session.debug || this.options['codeview_on']) {
            config.toolbar.splice(7, 0, ['view', ['codeview']]);
        }
        return config;
    },


});


});
