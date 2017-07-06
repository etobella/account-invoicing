# -*- coding: utf-8 -*-
# © 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    account_invoice_self_ids = fields.One2many(
        comodel_name='account.invoice.self',
        inverse_name='invoice_id',
        string='Self Invoice'
    )

    has_self_invoice = fields.Boolean(compute='_has_self_invoice')
    set_self_invoice = fields.Boolean(string='Set self invoice')
    can_self_invoice = fields.Boolean(related='partner_id.self_invoice')

    @api.multi
    @api.depends('account_invoice_self_ids')
    def _has_self_invoice(self):
        for record in self:
            record.has_self_invoice = len(self.account_invoice_self_ids) > 0

    @api.onchange('partner_id')
    def _on_change_partner_self_invoice(self):
        self.set_self_invoice = self.partner_id.self_invoice

    @api.constrains('account_invoice_self_ids')
    def check_self_invoices(self):
        if len(self.account_invoice_self_ids) > 1:
            raise ValidationError(
                _('Only one self invoice per invoice is allowed'))

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            partner = invoice.partner_id
            if partner.self_invoice and invoice.type in 'in_invoice' and \
                    invoice.set_self_invoice:
                self.env['account.invoice.self'].create({
                    'invoice_id': invoice.id,
                    'number':
                        partner.self_invoice_sequence_id.with_context(
                            ir_sequence_date=invoice.date).next_by_id()
                })
        return res

    @api.multi
    def action_view_account_invoice_self(self):
        return self.env['report'].get_action(
            self.account_invoice_self_ids.ids,
            'account_invoice_supplier_self_invoice.report_invoice_self'
        )
