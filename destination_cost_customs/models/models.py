# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    usd_rate = fields.Float(
        string='Rate',
        required=False, digits=0)
    FOBUSD = fields.Float(
        string='FOB-USD', 
        required=False, digits=0, compute="_compute_FOBUSD")
    FOBDOP = fields.Float(
        string='FOB-DOP',
        required=False, digits=0, compute="_compute_FOBDOP")
    amount_total_total = fields.Float(
        string='Total Amount',
        required=False, digits=0, compute="_compute_amount_total_total")
    cost_by_dop = fields.Float(
        string='Cost by DOP',
        required=False, digits=0, compute="_compute_cost_by_dop")
    cost_factor = fields.Float(
        string='Cost Factor',
        required=False, digits=0, compute="_compute_cost_factor")
    number = fields.Char(
        string='Number', 
        required=False)
    manifest = fields.Char(
        string='Manifest', 
        required=False)

    @api.depends('purchase_ids')
    def _compute_FOBUSD(self):

        for rec in self:

            total = 0.0

            for purchase in rec.purchase_ids:
                total = total + purchase.amount_total

            rec.FOBUSD = total

    @api.depends('FOBUSD')
    def _compute_FOBDOP(self):

        for rec in self:

            rec.FOBDOP = rec.FOBUSD * rec.usd_rate

    @api.depends('amount_total')
    def _compute_amount_total_total(self):

        for rec in self:

            rec.amount_total_total = rec.amount_total + rec.FOBDOP

    @api.depends('amount_total')
    def _compute_cost_by_dop(self):

        for rec in self:

            if rec.FOBUSD > 0:
                rec.cost_by_dop = rec.amount_total / rec.FOBUSD


    @api.depends('amount_total_total')
    def _compute_cost_factor(self):
        for rec in self:

            if rec.FOBUSD > 0:
                rec.cost_factor = rec.amount_total_total / rec.FOBUSD
