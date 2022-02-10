# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    purchase_ids = fields.Many2many(
        comodel_name='purchase.order',
        string='Purchases', domain="[('state', 'in', ('purchase', 'done'))]")
    purchase_info_line_ids = fields.One2many(
        comodel_name='purchase.information.line',
        inverse_name='cost_id',
        string='Purchase Order Information',
        required=False)

    @api.onchange('purchase_ids')
    def _onchange_purchase_ids(self):

        for rec in self:
            for purchase in rec.purchase_ids:

                for picking in purchase.picking_ids:
                    rec.picking_ids = [(4, picking.id)]

    def load_purchases(self):

        for purchase in self.purchase_ids:

            for picking in purchase.picking_ids:

                self.env['purchase.information.line'].create({
                    'cost_id': self.id,
                    'picking_id': picking.id,
                    'purchase_id': picking.purchase_id.id,
                    'partner_id': picking.purchase_id.partner_id.id,
                })

            # for line in purchase.order_line:
            #     if line.product_id.landed_cost_ok:
            #
            #         self.env['stock.landed.cost.lines'].create({
            #             'cost_id': self.id,
            #             'account_id': line.account_id.id,
            #             'product_id': purchase.product_id.id,
            #             'price_unit': purchase.price_unit,
            #             'split_method': 'equal',
            #             'name': purchase.name
            #         })

class PurchaseInformationLine(models.Model):
    _name = 'purchase.information.line'
    _description = 'Purchase Information Line'

    cost_id = fields.Many2one(
        comodel_name='stock.landed.cost',
        string='Cost',
        required=False)
    picking_id = fields.Many2one(
        comodel_name='stock.picking',
        string='Picking',
        required=False)
    purchase_id = fields.Many2one(
        comodel_name='purchase.order',
        string='Purchase',
        required=False)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=False)
    qty_received = fields.Float(
        string='Received Qty', digits='Product Unit of Measure', compute="_compute_qty_received_product_qty")
    ordered_qty = fields.Float(string='Ordered Qty', digits='Product Unit of Measure', compute="_compute_qty_received_product_qty")
    amount_total = fields.Monetary(string='Total', store=True, related="purchase_id.amount_total")
    currency_id = fields.Many2one('res.currency', 'Currency', store=True, related="purchase_id.currency_id")

    @api.depends('purchase_id')
    def _compute_qty_received_product_qty(self):

        for rec in self:
            qty_received = 0.0
            ordered_qty = 0.0

            for line in rec.purchase_id.order_line:
                qty_received = qty_received + line.qty_received
                ordered_qty = ordered_qty + line.product_qty


            rec.ordered_qty = ordered_qty
            rec.qty_received = qty_received







