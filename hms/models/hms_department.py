from odoo import models, fields, api


class HmsDepartment(models.Model):
    _name = "hms.department"

    name = fields.Char(required=True, string="Department Name")
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many("hms.patient", "department_id")


