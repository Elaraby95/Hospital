from odoo import models, fields, api


class HmsDoctor(models.Model):
    _name = "hms.doctor"
    _rec_name = "First_name"

    First_name = fields.Char()
    Last_name = fields.Char()
    Image = fields.Binary()