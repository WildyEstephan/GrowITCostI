# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    vendor_invoice_ids = fields.Many2many(
        comodel_name='account.move',
        string='Invoices', domain="[('state', 'not in', ('draft', 'cancel'))]")
    vendor_invoice_line = fields.One2many(
        comodel_name='stock.landed.cost',
        inverse_name='cost_id',
        string='Vendor Invoice Line',
        required=False)

    def load_invoices(self):

        for invoice in self.vendor_invoice_ids:

            products = invoice.invoice_line_ids.filtered(lambda r: r.is_landed_costs_line)

            for product in products:

                self.env['stock.landed.cost.lines'].create({
                    'cost_id': self.id,
                    'account_id': product.account_id.id,
                    'product_id': product.product_id.id,
                    'price_unit': product.price_unit,
                    'split_method': 'equal',
                    'name': product.name
                })

class Invoice(models.Model):
    _inherit = 'account.move'

    cost_liq_id = fields.Many2one(
        comodel_name='stock.landed.cost',
        string='Cost',
        required=False)


