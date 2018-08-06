odoo.define('document_page.remove_attach_button', function(require) {

"use strict";

var core = require('web.core');
var Sidebar = require('web.Sidebar');

var _t = core._t;

Sidebar.include({
    init : function(){
        this._super.apply(this, arguments);
        var view = this.getParent();
        if (view.fields_view && view.fields_view.type === "form" && window.location.href.indexOf('&model=document.page') > -1) {
            var i = this.sections.findIndex(function(x){ return x.name==='files';});
            this.sections.splice(i, 1,);
        }
    },

});

});
