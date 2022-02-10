# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    usd_rate = fields.Float(
        string='Rate',
        required=False, digits=0)
    FOBUSD = fields.Float(
        string='FOB-USD', 
        required=False, digits=0, compute="_compute_get_totals")
    FOBDOP = fields.Float(
        string='FOB-DOP',
        required=False, digits=0, compute="_compute_get_totals")
    amount_total_total = fields.Float(
        string='Total Amount',
        required=False, digits=0, compute="_compute_get_totals")
    cost_by_dop = fields.Float(
        string='Cost by DOP',
        required=False, digits=0, compute="_compute_get_totals")
    cost_factor = fields.Float(
        string='Cost Factor',
        required=False, digits=0, compute="_compute_get_totals")
    number = fields.Char(
        string='Number', 
        required=False)
    manifest = fields.Char(
        string='Manifest', 
        required=False)

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

            if FOBUSD_total > 0:
                rec.cost_factor = rec.amount_total_total / FOBUSD_total
