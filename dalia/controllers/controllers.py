# -*- coding: utf-8 -*-
# from odoo import http


# class Dalia(http.Controller):
#     @http.route('/dalia/dalia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dalia/dalia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dalia.listing', {
#             'root': '/dalia/dalia',
#             'objects': http.request.env['dalia.dalia'].search([]),
#         })

#     @http.route('/dalia/dalia/objects/<model("dalia.dalia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dalia.object', {
#             'object': obj
#         })
