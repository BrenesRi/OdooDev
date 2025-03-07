# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class Prueba(models.Model):

    _name = 'prueba'
    _description = 'Modelo de prueba'
    _rec_name = 'consecutivo'
    #_order = 'tramite_estado, fecha_emision, numero, tramite_numero'
    #_inherit = ['mail.thread', 'mail.activity.mixin']

    #region === CAMPOS: CERTIFICACION ====================================================

    consecutivo = fields.Integer(
        help='Número consecutivo del certificado (reinicia cada año)',
        group_operator=False
    )
