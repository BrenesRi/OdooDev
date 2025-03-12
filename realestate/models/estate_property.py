# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char('Plan Name', required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date')
    expected_price = fields.Float('Expected Price', requiered=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Number of Bedrooms')
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        'Garden Orientation'
    )
