# -*- coding: utf-8 -*-
# © 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoiceSelf(models.Model):
    _name = 'account.invoice.self'
    _description = 'Self Invoices generated'

    @api.multi
    def name_get(self):
        result = []
        for inv in self:
            result.append((inv.id, inv.number))
        return result

    invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        required=True,
        readonly=True
    )

    number = fields.Char(
        required=True,
        readonly=True
    )
