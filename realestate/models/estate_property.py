# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Plan Name", required=True, translate=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string="Available From", copy=False, default=date.today() + relativedelta(months=+3))
    expected_price = fields.Float(string='Expected Price', requiered=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m²)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(selection=[
                                        ('north', 'North'), 
                                        ('south', 'South'), 
                                        ('east', 'East'), 
                                        ('west', 'West')],
                                        string='Garden Orientation'
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(selection=[('New',"New"),
                                      ('Offer Received',"Offer Received"),
                                      ('Offer Accepted',"Offer Accepted"),
                                      ('Sold',"Sold"),
                                      ('Canceled',"Canceled")], 
                                      default='New', string='State', required=True, copy=False)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer = fields.Many2one('res.partner', copy=False, string = "Buyer")
    salesperson = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tag")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer")