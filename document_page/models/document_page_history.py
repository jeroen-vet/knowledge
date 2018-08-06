# -*- coding: utf-8 -*-
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import difflib
from odoo import api, fields, models
from odoo.tools.translate import _


#~ class DocumentPageAtt(models.Model):
    #~ _name = 'document.page.att'
    #~ _inherits = {'ir.attachment': 'attach_id'}
       #~ 
    #~ attach_id = fields.Many2one('ir.attachment',required=True, ondelete='cascade') # actually is one to one but no such type
    #~ #doc_page_hist_ids = fields.Many2many('document.page.history', string='Document Page') 
#~ 
    #~ 
    #~ @api.model
    #~ def create(self, values):
        #~ values['res_id']=values['id']
        #~ values['res_model']='project.task'
        #~ return super(TaskReport, self).create(values)    



class DocumentPageHistory(models.Model):
    """This model is necessary to manage a document history."""

    _name = "document.page.history"
    _description = "Document Page History"
    _order = 'id DESC'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env['res.company']._company_default_get('document.page.history'))
    page_id = fields.Many2one('document.page', 'Page', ondelete='cascade')
    name = fields.Char(index=True)
    summary = fields.Char(index=True)
    content = fields.Text()
    diff = fields.Text(compute='_compute_diff')
    #att_ids = fields.Many2many('document.page.att', string="Attachments")     
    att_ids = fields.Many2many('ir.attachment', string="Attachments") # this allows more than one history page to refer to same attachment (simple
                                                                      # solution without intermediate model. This would mean that all attachments 
                                                                      # still appear as attachment to the page itself from ir_attachment point of view

    @api.multi
    def _compute_diff(self):
        """Shows a diff between this version and the previous version"""
        history = self.env['document.page.history']
        for rec in self:
            prev = history.search([
                ('page_id', '=', rec.page_id.id),
                ('create_date', '<', rec.create_date)],
                limit=1,
                order='create_date DESC')
            if prev:
                
                rec.diff = self.getDiff(prev.id, rec.id)
            else:
                rec.diff = self.getDiff(False, rec.id)


    # here have to include "Removed attachment: .... Added attachment: ....." with details as date, byte count etc
    @api.model
    def getDiff(self, v1, v2):
        """Return the difference between two version of document version."""
        text1 = v1 and self.browse(v1).content or ''
        text2 = v2 and self.browse(v2).content or ''
        # Include line breaks to make it more readable
        # TODO: consider using a beautify library directly on the content
        text1 = text1.replace('</p><p>', '</p>\r\n<p>')
        text2 = text2.replace('</p><p>', '</p>\r\n<p>')
        line1 = text1.splitlines(1)
        line2 = text2.splitlines(1)
        # get differences in attachments
        v1atts= v1 and self.browse(v1).att_ids or self.browse(v2).att_ids & self.browse(v2).att_ids # get empty record set in case v1 is false 
        v2atts= v2 and self.browse(v2).att_ids # v2 should never be empty
        if line1 == line2 and v1atts==v2atts:
            return _('There are no changes in revisions.')
        else:
            res=""
            if v1atts<>v2atts:
                removed=v1atts-v2atts
                added=v2atts-v1atts
                if removed or added:
                    res+='''
                        <style>
                        table, th, td {
                        border: 1px solid black;
                        border-collapse: collapse;
                        }
                        th, td {
                        padding: 5px;
                        text-align: left;
                        }
                        caption { 
                        text-align: left;
                        font-weight: bold;
                        }
                        </style>'''                    
                if removed:
                    res+="<table><caption>Attachments removed:</caption>"
                    res+="<tr><th>File</th><th>Name</th><th>Size</th></tr>"
                    for r in removed:
                        res+="<tr><td>%s</td><td>%s</td><td>%s</td></tr><br />" % (r.datas_fname, r.name, r.file_size)
                    res+="</table><br/>"   

                if added:
                    res+="<table><caption>Attachments added:</caption>"
                    res+="<tr><th>File</th><th>Name</th><th>Size</th></tr>"
                    for r in added:
                        res+="<tr><td>%s</td><td>%s</td><td>%s</td></tr><br />" % (r.datas_fname, r.name, r.file_size)   
                    res+="</table><br/>"                             
            if line1<>line2:
                diff = difflib.HtmlDiff()
                res+="<p><b>Content changes:<b></p>"
                res+= diff.make_table(
                    line1, line2,
                    "Revision-{}".format(v1),
                    "Revision-{}".format(v2),
                    context=True
                )
            return res    
                
    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = "%s #%i" % (rec.page_id.name, rec.id)
            result.append((rec.id, name))
        return result
