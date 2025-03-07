# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Estudiante(models.Model):
    #Metainformación
    _name = "school.estudiante"
    _desciption = "Tabla de estudiantes de prueba"

    #Información de la tabla
    name = fields.Char(string="Nombre", required=True)
    age = fields.Integer(string="Edad", searchable=True)
    description = fields.Text(string="Descripción", searchable=True)

#    @api.depends('value')
#    def _value_pc(self):
#        for record in self:
#            record.value2 = float(record.value) / 100
