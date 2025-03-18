# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class EstatePropertyType(models.Model):
  _name = 'estate.property.type'
  _description = 'Type of Properties'

  name = fields.Char(required=True)