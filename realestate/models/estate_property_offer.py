from datetime import timedelta, datetime
from odoo import api, fields, models

# The `PropertyOffer` class is a model that represents an offer made on a property, with fields for
# price, status, partner, property, validity, and deadline.
class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is a model who can offer the property"

    # Basic
    price = fields.Float("Price")
    status = fields.Selection(selection=[('Accepted', "Accepted"), ('Refused', "Refused"), ], string="Status", copy=False)
    
    # Relation
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)