# -*- coding: utf-8 -*-
# from odoo import http


# class DestinationCostByInvoice(http.Controller):
#     @http.route('/destination_cost_by_invoice/destination_cost_by_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/destination_cost_by_invoice/destination_cost_by_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('destination_cost_by_invoice.listing', {
#             'root': '/destination_cost_by_invoice/destination_cost_by_invoice',
#             'objects': http.request.env['destination_cost_by_invoice.destination_cost_by_invoice'].search([]),
#         })

#     @http.route('/destination_cost_by_invoice/destination_cost_by_invoice/objects/<model("destination_cost_by_invoice.destination_cost_by_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('destination_cost_by_invoice.object', {
#             'object': obj
#         })
