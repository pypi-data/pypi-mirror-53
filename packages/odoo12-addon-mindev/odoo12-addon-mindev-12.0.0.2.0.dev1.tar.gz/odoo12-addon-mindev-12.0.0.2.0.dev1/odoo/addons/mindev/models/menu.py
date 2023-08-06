# Copyright 2011 Minorisa, S.L. <http://www.minorisa.net>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    xml_id = fields.Char(
        string="XML ID",
        compute="_compute_xml_fields"
    )
    xml_module = fields.Char(
        string="XML Module",
        compute="_compute_xml_fields"
    )
    xml_name = fields.Char(
        string="XML Name",
        compute="_compute_xml_fields"
    )

    @api.multi
    def _compute_xml_fields(self):
        objimd = self.env['ir.model.data']
        for rec in self:
            xml_id = objimd.search([
                ('model', '=', self._name),
                ('res_id', '=', rec.id)
            ], limit=1)
            if xml_id:
                rec.xml_id = str(xml_id.id)
                rec.xml_module = xml_id.module
                rec.xml_name = xml_id.name
