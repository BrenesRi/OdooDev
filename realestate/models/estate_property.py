from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
import logging
_logger = logging.getLogger(__name__)


class Property(models.Model):
  _name = "estate.property"
  _description = "this is my new model at odoo 16"

  name = fields.Char(string="Title", required=True)
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date(string="Available From", copy=False, default=date.today() + relativedelta(months=+3))
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(readonly=True, copy=False)
  bedrooms = fields.Integer(default=2)
  living_area = fields.Integer(string="Living Area (sqm)")
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection(selection=[('North',"North"),
                                                  ('South',"South"),
                                                  ('East',"East"),
                                                  ('West',"West")])
  active = fields.Boolean('Active', default=True)
  state = fields.Selection(selection=[('New',"New"),
                                      ('Offer Received',"Offer Received"),
                                      ('Offer Accepted',"Offer Accepted"),
                                      ('Sold',"Sold"),
                                      ('Canceled',"Canceled"),], default='New', string='State', required=True, copy=False)
  property_type_id = fields.Many2one('estate.property.type', string="Property Type")

  buyer = fields.Many2one('res.partner', copy=False, string = "Buyer")
  salesperson = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
  tag_ids = fields.Many2many('estate.property.tag', string="Tag")
  offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer")

  total_area = fields.Float(string="Total Area (sqm)", compute="_total_area")
  best_price = fields.Float(string="Best Offer", compute="_best_price")
  
  @api.depends("living_area", "garden_area")
  def _total_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area

  @api.depends("offer_ids")
  def _best_price(self):
    for record in self:
      if self.offer_ids:
        record.best_price = max(self.offer_ids.mapped('price'))
      else:
        record.best_price = 0

  @api.onchange("garden")
  def _onchange_garden(self):
    if self.garden:
      self.garden_area = 10
      self.garden_orientation = 'North'
    else:
      self.garden_area = 0
      self.garden_orientation = ''

  def sell_property(self):
    _logger.info('sell property from parent')
    for record in self:
        if record.state == "Canceled":
            raise UserError(_("You can't set Caceled property as sold"))
        else:
            record.state = "Sold"
    return True
  def cancel_property(self):
    for record in self:
        if record.state == "Sold":
            raise UserError(_("You can't set Sold property as Canceled"))
        else:
            record.state = "Canceled"
    return True