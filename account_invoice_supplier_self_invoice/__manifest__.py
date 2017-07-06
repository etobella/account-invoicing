# -*- coding: utf-8 -*-
# © 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Self Invoice",
    "version": "10.0.1.0.0",
    "author": "Creu Blanca, "
              "Odoo Community Association (OCA)",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/account-invoicing",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/account_invoice_views.xml",
        "views/account_invoice_self_views.xml",
        "views/report_self_invoice.xml"
    ],
    "installable": True,
}
