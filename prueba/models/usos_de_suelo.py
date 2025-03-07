# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import logging


_logger = logging.getLogger(__name__)

class UsosDeSuelo(models.Model):

    _name = 'pdi.usos_de_suelo'
    _description = 'Certificado de Uso de Suelo'
    _rec_name = 'tramite_numero'
    _order = 'tramite_estado,fecha_emision, numero, tramite_numero'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _todo_mayuscula = ['tramite_solicitante']
    _sin_tildes = ['tramite_solicitante']

    #region === CAMPOS: CERTIFICACION ====================================================

    consecutivo = fields.Integer(
        help='Número consecutivo del certificado (reinicia cada año)',
        group_operator=False
    )

    @api.depends('fecha_emision', 'consecutivo')
    def _calcular_numero(self):
        for reg in self:
            reg.numero = ''
            if not reg.consecutivo or not reg.fecha_emision:
                return
            reg.numero = f'{str(reg.consecutivo).zfill(4)}-{reg.fecha_emision.year}'

    numero = fields.Char(
        help='Número del certificado de uso de suelo (Consecutivo-Año)',
        string='Número',
        compute=_calcular_numero,
        store=True,
        tracking=True
    )

    @api.constrains('active')
    def _verificar_active(self):
        for reg in self:
            if reg.active:
                return
            if reg.tramite_estado != 'resuelto':
                raise ValidationError('No es posible archivar porque el trámite no está resuelto')
            elif not reg.numero:
                raise ValidationError('No es posible archivar porque no está definido el número del documento')

    active = fields.Boolean(
        help='Debe mostrarse el registro o está archivado',
        string="Activo",
        default=True
    )

    resultado_seleccion = [
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('informativo', 'Informativo'),
        ('patentes', 'Patentes'),
        ('condicionado', 'Condicionado'),
        ('de_licores', 'De Licores')
    ]

    resultado = fields.Selection(
        help="Resultado del análisis de la solicitud",
        selection=resultado_seleccion
    )

    documento = fields.Binary(
        help="Documento generado con el certificado del uso del suelo",
        attachment=True
    )

    documento_nombre = fields.Char(
        help='Nombre del archivo que tendrá el documento generado con el certificado del '
             'uso de suelo',
        string='Nombre del Archivo'
    )

    #endregion

    #region ==== CAMPOS: SEGUIMIENTO =====================================================
    
    fecha_ingreso = fields.Date(
        string='Fecha de Ingreso',
        default=fields.Date.today,
        help='Fecha de ingreso del trámite al departamento',
        required=True,
        tracking=True
    )

    fecha_emision = fields.Date(
        string='Fecha de Emisión',
        help='Fecha en que se emitió el certificado',
        tracking=True
    )

    fecha_traslado = fields.Date(
        string='Fecha de Traslado',
        help='Fecha en que se devolvió el trámite a Plataforma de Servicios',
        tracking=True
    )

    @api.depends('tramite_fecha', 'fecha_traslado')
    def _calcular_duracion(self):
        for reg in self:
            inicio = reg.tramite_fecha
            final = reg.fecha_traslado if reg.fecha_traslado else fields.Date.context_today(reg)
            reg.duracion = (final - inicio).days

    def _buscar_duracion(self, operator, value):
        self.env.cr.execute(
            "SELECT id "
            "FROM pdi_usos_de_suelo "
            "WHERE "
            "(fecha_traslado is not NULL "
            f"AND fecha_traslado - tramite_fecha {operator} {value}) "
            "OR (fecha_traslado is NULL "
            f"AND '{fields.Date.context_today(self)}'::date - tramite_fecha {operator} {value})"
        )
        return [('id', 'in', self.env.cr.fetchall()), '|', ('active', '=', True), ('active', '=', False)]

    duracion = fields.Integer(
        help='Cantidad de días naturales que transcurrieron para resolver el trámite. Si el trámite no se ha resuelto indica la cantidad de días que han transcurrido hasta el día de hoy',
        string='Duración',
        compute=_calcular_duracion,
        search=_buscar_duracion,
        group_operator='avg'
    )

    #endregion

    #region ==== CAMPOS: Información del Trámite =========================================
    
    tramite_numero = fields.Char(
        help='Indica el número de trámite según el sistema usado en la Plataforma de Servicios', 
        string='N° de Trámite', 
        required=True,
        tracking=True)

    tramite_solicitante = fields.Char(
        help='Nombre del solicitante del certificado de uso de suelo', 
        string='Solicitante',
        required=True,
        tracking=True)

    tramite_fecha = fields.Date(
        help='Fecha de solicitud del trámite',
        string='Fecha del Trámite',
        default=fields.Date.today,
        required=True,
        tracking=True)

    tramite_estado_seleccion = [
        ('en_tramite', 'En trámite'),
        ('resuelto', 'Resuelto')
    ]
    tramite_estado = fields.Selection(
        help='Está el trámite resuelto o en trámite',
        string='Estado del trámite',
        selection=tramite_estado_seleccion,
        default='en_tramite',
        tracking=True)

    tramite_uso_solicitado =fields.Text(
        help='Uso solicitado según el trámite',
        string='Uso Solicitado',
        tracking=True
        )

    #endregion

    #region ==== CAMPOS: Información de la Finca =========================================

    finca_localizacion = fields.Char (
        help='Código de localización de la finca según el sistema de Catastro',
        string='Localización',
        required=False,
        tracking=True
    )

    finca_plano = fields.Char(
        help='Número de plano según el sistema de Catastro',
        string='N° Plano',
        required=False,
        tracking=True
    )

    finca_folio_real = fields.Char(
        help="Folio real que identifica a la finca",
        string="Folio Real",
        tracking=True
    )

    finca_direccion = fields.Text(
        help='Dirección física de la finca',
        string='Dirección',
        tracking=True
    )

    distrito_seleccion=[
        ('1', '1. San Isidro'),
        ('2', '2. San Rafael'),
        ('3', '3. Dulce Nombre'),
        ('4', '4. Patalillo'),
        ('5', '5. Cascajal')
    ]

    finca_distrito = fields.Selection(
        help='Distrito donde se encuentra la finca',
        string='Distrito',
        selection=distrito_seleccion,
        required=False,
        tracking=True
    )

    zona_seleccion = [
        ('ZA', 'Agropecuaria'),
        ('ZCA', 'Cascajal'),
        ('ZC', 'Cauces'),
        ('ZCE', 'Cautela Ecologica'),
        ('ZCRI', 'Comercial Residencial Industrial'),
        ('ZCM', 'Comercio Mixta'),
        ('ZCUGA', 'Control Urbano Gallera'),
        ('ZCULN', 'Control Urbano Las Nubes'),
        ('ZCUMA', 'Control Urbano Manantial'),
        ('ZCURO', 'Control Urbano Rodeo'),
        ('ZCUSP', 'Control Urbano San Pedro'),
        ('ZCUSR', 'Control Urbano San Rafael'),
        ('ZCUSI', 'Control Urbano Sinai'),
        ('ZENT', 'Entorno'),
        ('ZIC', 'Industrial Comercial'),
        ('ZLCSSA', 'Lineal de Comercios y Servicios San Antonio'),
        ('ZPA', 'Parcelas Agricolas'),
        ('ZPN', 'Parques Nacionales'),
        ('ZRSCBI', 'Residencia Servicios y Comercio de Baja Intensidad'),
        ('ZRCSIC', 'Residencial Casco San Isidro de Coronado'),
        ('ZRAD', 'Residencial de Alta Densidad'),
        ('ZRBD', 'Residencial de Baja Densidad'),
        ('ZRA', 'Restriccion Agricola '),
        ('ZSI', 'Servicios Institucionales '),
    ]

    zona_plan_regulador_1998 = fields.Selection(
        help='donde se encuentra la finca según el Plan Regulador',
        string='Zona',
        selection=zona_seleccion,
        tracking=True
    )

    #endregion

    #region ==== FUNCIONES DE ACCION =====================================================

    def marcar_traslado(self):
        for reg in self:
            if reg.tramite_estado != 'resuelto':
                raise UserError('No es posible trasladar un documento si el trámite no '
                    'está resuelto.')
            if reg.fecha_traslado:
                raise UserError('Este documento ya tiene fecha de traslado')

            reg.fecha_traslado = fields.Date.context_today(reg)

    #endregion

    #region ==== FUNCIONES OVERRIDE ======================================================

    def write(self, vals):
        if 'tramite_estado' in vals  and vals['tramite_estado'] == 'resuelto':
            hoy = fields.Date.context_today(self)
            if not self.fecha_emision:
                vals['fecha_emision'] = hoy
            if self.consecutivo == 0:
                ultimo = self.search(
                    [('fecha_emision', '<=', f'{hoy.year}-12-31'),
                    ('fecha_emision', '>=', f'{hoy.year}-01-01'),
                    '|', ('active', '=', True), ('active', '=', False)],
                    order='consecutivo desc',
                    limit=1
                )
                vals['consecutivo'] = ultimo['consecutivo'] + 1 if len(ultimo) > 0 else 1
        return super(UsosDeSuelo, self).write(vals)

    #endregion
