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

    # Compute
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_get_deadline', inverse='_set_deadline')

    @api.depends('create_date','validity')
    def _get_deadline(self):
        """
        The function calculates the deadline by adding the validity duration to the create date.
        """
        
        for record in self:
            if not (record.create_date and record.validity):
                start = datetime.now()
                duration = timedelta(record.validity, seconds=-1)
                record.date_deadline = start + duration
                continue
            
            start = fields.Datetime.from_string(record.create_date)
            duration = timedelta(record.validity, seconds=-1)
            record.date_deadline = start + duration
    
    def _set_deadline(self):
        for record in self:
            if not (record.create_date and record.validity):
                start = datetime.now()
                duration = timedelta(record.validity, seconds=-1)
                record.date_deadline = start + duration
                continue

            start = fields.Datetime.from_string(record.create_date)
            end = fields.Datetime.from_string(record.date_deadline)
            record.validity = (end - start).days + 1

    def action_accept(self):
        for line in  self:
            line.property_id.selling_price = line.price
            line.property_id.buyer = line.partner_id
            line.property_id.state = "Offer Received"
            line.status = "Accepted"
    def action_refuse(self):
        for line in  self:
            line.property_id.selling_price = 0
            line.property_id.buyer = None
            line.status = "Refused"