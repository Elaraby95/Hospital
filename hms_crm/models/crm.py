from odoo import models, fields, api
from odoo.exceptions import UserError


class CrmInherit(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one('hms.patient')
    name_two = fields.Char()

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError("You can't delete this patient")
        super().unlink()

    # @api.constrains("email")
    # def check_email_id(self):
    #     this_mail = self.email
    #     other_mail = hms.patient.email
    #     if this_mail == other_mail:
    #         raise UserError("The Department is full")
