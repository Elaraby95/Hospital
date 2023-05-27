from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class HmsPatient(models.Model):
    _name = "hms.patient"
    _rec_name = "First_name"

    First_name = fields.Char(required=True)
    Last_name = fields.Char()
    email = fields.Char()
    Age = fields.Float(compute='calculate_age', store=True)
    Birth_date = fields.Date()
    PCR = fields.Boolean()
    CR_Ratio = fields.Float()
    Image = fields.Binary()
    Address = fields.Text()
    History = fields.Html()
    department_id = fields.Many2one("hms.department")
    department_capacity = fields.Integer(related="department_id.capacity")
    doctor_id = fields.Many2many("hms.doctor")
    Blood = fields.Selection([
        ('A1', "-A"), ('A2', "+A"), ('B1', "-B"), ('B2', "+B"), ('AB1', "-AB"), ('AB2', "+AB"), ('O1', "-O"),
        ('O2', "+O")
    ])
    state = fields.Selection([
        ("undetermined", "Undetermined"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("serious", "Serious"),
    ])
    description_ids = fields.One2many("hms.description", "patient_id")

    @api.constrains('email')
    def _check_email(self):
        count_email = self.search_count([('email', '=', self.email)])
        if count_email > 1 and self.email is not False:
            raise UserError('The email already registered, please use another email!')

    def undetermined(self):
        self.state = "undetermined"

    def good(self):
        self.state = "good"

    def fair(self):
        self.state = "fair"

    def serious(self):
        self.state = "serious"

    @api.model
    def create(self, vals):
        new_patient = super().create(vals)
        patient_split = new_patient.First_name.split()
        new_patient.email = f"{patient_split[0][0].upper()}{patient_split[0][2:]}@gmail.com"
        return new_patient

    def write(self, vals):
        if "First_name" in vals:
            patient_split = vals["First_name"].split()
            vals["email"] = f"{patient_split[0][0].upper()}{patient_split[0][2:]}@gmail.com"
        super().write(vals)

    def unlink(self):
        for record in self:
            if record.state in ["serious", "undetermined"]:
                raise UserError("You can't delete serious/undetermined")
        super().unlink()

    @api.depends('Birth_date')
    def calculate_age(self):
        today = date.today()
        for record in self:
            birth_date = record.Birth_date
            if birth_date:
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.Age = age

    @api.onchange("state")
    def _on_change_state(self):
        if not self.state:
            return {}
        return {
            'warning': {'title': 'warning',
                        'message': 'state changed to New_State'},
        }

    @api.onchange("Age")
    def _on_change_age(self):
        if not self.Age:
            return {}
        elif self.Age < 30:
            self.PCR = True
        else:
            self.PCR = False

        return {
            'warning': {'title': 'warning',
                        'message': 'message that has been checked'},
        }

    @api.constrains("department_id")
    def check_department_id(self):
        department_count = len(self.department_id.patient_ids)
        department_capacity = self.department_capacity
        if department_count > department_capacity:
            raise UserError("The Department is full")




class Description(models.Model):
    _name = 'hms.description'
    _rec_name = 'dsc'

    dsc = fields.Text(string="description")
    patient_id = fields.Many2one("hms.patient")

    # @api.onchange('Birth_date')
    # def set_age(self):
    #     for rec in self:
    #         if rec.Birth_date:
    #             dt = rec.Birth_date
    #             d1 = datetime.strptime(str(dt), "%Y-%m-%d").date()
    #             d2 = date.today()
    #             rd = relativedelta(d2, d1)
    #             rec.Age = str(rd.years) + ' years'
# شغالة بس لازم العمر يكون استرينج
