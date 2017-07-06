# -*- coding: utf-8 -*-
# © 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestSelfInvoice(common.TransactionCase):

    def setUp(self):
        return super(TestSelfInvoice, self).setUp()

    def test_self_invoice(self):
        partner = self.env['res.partner'].create({
            'name': 'Partner',
            'supplier': True,
            'self_invoice': False
        })
        simple_partner = self.env['res.partner'].create({
            'name': 'Partner',
            'supplier': True,
            'self_invoice': False
        })
        main_company = self.env.ref('base.main_company')
        invoice = self.env['account.invoice'].create({
            'company_id': main_company.id,
            'partner_id': simple_partner.id,
            'type': 'in_invoice'
        })
        product = self.env['product.product'].create({
            'name': 'Product'
        })
        account = self.env['account.account'].create({
            'company_id': main_company.id,
            'name': 'Testing Product account',
            'code': 'test_product',
            'user_type_id': self.env.ref(
                'account.data_account_type_revenue').id
        })
        self.env['account.invoice.line'].create({
            'invoice_id': invoice.id,
            'product_id': product.id,
            'quantity': 1,
            'account_id': account.id,
            'name': 'Test product',
            'price_unit': 20
        })
        invoice._onchange_invoice_line_ids()
        invoice.action_invoice_open()
        invoice.number = 'self/00001'
        self.assertFalse(invoice.has_self_invoice)
        partner.set_self_invoice()
        self.assertNotEqual(partner.self_invoice_sequence_id, False)
        invoice2 = self.env['account.invoice'].create({
            'company_id': main_company.id,
            'partner_id': simple_partner.id,
            'set_self_invoice': True,
            'type': 'in_invoice'
        })
        self.env['account.invoice.line'].create({
            'invoice_id': invoice2.id,
            'product_id': product.id,
            'quantity': 1.0,
            'account_id': account.id,
            'name': 'Test product',
            'price_unit': 20.0
        })
        invoice2.partner_id = partner
        invoice2._onchange_invoice_line_ids()
        invoice2.action_invoice_open()

        self.assertTrue(invoice2.has_self_invoice)
        self.assertEqual(
            invoice2.action_view_account_invoice_self()[
                'context']['active_ids'],
            invoice2.account_invoice_self_ids.ids
        )
        self.assertTrue(partner.self_invoice)
        partner.set_self_invoice()
        self.assertFalse(partner.self_invoice)
        names = invoice2.account_invoice_self_ids.name_get()
        self.assertEqual(
            invoice2.account_invoice_self_ids.ensure_one().number,
            names[invoice.account_invoice_self_ids.ensure_one().id]
        )
