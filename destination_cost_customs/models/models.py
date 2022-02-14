# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    usd_rate = fields.Float(
        string='Rate',
        required=False, digits=0)
    FOBUSD = fields.Float(
        string='FOB-USD', 
        required=False, digits=0, compute="_compute_get_totals", store=True)
    FOBDOP = fields.Float(
        string='FOB-DOP',
        required=False, digits=0, compute="_compute_get_totals", store=True)
    amount_total_total = fields.Float(
        string='Total Amount',
        required=False, digits=0, compute="_compute_get_totals", store=True)
    cost_by_dop = fields.Float(
        string='Cost by DOP',
        required=False, digits=0, compute="_compute_get_totals", store=True)
    cost_factor = fields.Float(
        string='Cost Factor',
        required=False, digits=0, compute="_compute_get_totals", store=True)
    number = fields.Char(
        string='Number', 
        required=False)
    manifest = fields.Char(
        string='Manifest', 
        required=False)

    @api.onchange('purchase_ids')
    def _onchange_purchase_ids(self):

        for rec in self:
            for purchase in rec.purchase_ids:

                for picking in purchase.picking_ids:
                    rec.picking_ids = [(4, picking.id)]

                for invoice in purchase.invoice_ids:
                    rec.vendor_invoice_ids = [(4, invoice.id)]

    @api.depends('purchase_ids', 'amount_total')
    def _compute_get_totals(self):

        for rec in self:

            FOBUSD_total = 0.0

            for purchase in rec.purchase_ids:
                FOBUSD_total = FOBUSD_total + purchase.amount_total

            rec.FOBUSD = FOBUSD_total

            FOBDOP_total = FOBUSD_total * rec.usd_rate
            rec.FOBDOP = FOBDOP_total

            rec.amount_total_total = rec.amount_total + FOBUSD_total

            if FOBUSD_total > 0:
                rec.cost_by_dop = rec.amount_total / FOBUSD_total
            else:
                rec.cost_by_dop = 0.0

            if FOBUSD_total > 0:
                rec.cost_factor = rec.amount_total_total / FOBUSD_total
            else:
                rec.cost_factor = 0.0
