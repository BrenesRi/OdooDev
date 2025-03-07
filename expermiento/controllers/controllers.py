# -*- coding: utf-8 -*-
# from odoo import http


# class Expermiento(http.Controller):
#     @http.route('/expermiento/expermiento', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expermiento/expermiento/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('expermiento.listing', {
#             'root': '/expermiento/expermiento',
#             'objects': http.request.env['expermiento.expermiento'].search([]),
#         })

#     @http.route('/expermiento/expermiento/objects/<model("expermiento.expermiento"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expermiento.object', {
#             'object': obj
#         })
