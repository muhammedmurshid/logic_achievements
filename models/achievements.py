from odoo import models, fields, _, api
from datetime import datetime, date
from odoo.exceptions import UserError


class LogicAchievements(models.Model):
    _name = 'logic.achievements'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Achievements'
    _order = 'id desc'

    name = fields.Char('Name')
    department_id = fields.Many2one('hr.department', 'Department')
    task_type = fields.Selection(
        [('meeting', 'Meeting'), ('telephone_discussion', 'Telephone Discussion'), ('clerical_works', 'Clerical Works'),
         ('day_to_day_works', 'Day To Day Works'), ('batch_related_works', 'Batch Related Works'), ('other', 'Other')],
        string="Task Types")
    date = fields.Date(string="Date", default=date.today())
    tags_id = fields.Many2many('project.tags', string="Tags")
    task_types = fields.Selection(selection=[('meeting', 'Meeting'), ('telephone_discussion', 'Telephone Discussion'),
                                             ('clerical_works', 'Clerical Works'),
                                             ('day_to_day_works', 'Day To Day Works'),
                                             ('batch_related_works', 'Batch Related Works'),
                                             ('other', 'Other')], string="Task Type",
                                  required=1)
    meeting_type = fields.Selection(selection=[('internal', 'Internal'), ('external', 'External')],
                                    string="Meeting Type")
    meeting_ids = fields.Many2many('hr.employee', string="Meeting With")
    meeting = fields.Selection(selection=[('online', 'Online'), ('offline', 'Offline')], string="Meeting")
    meeting_with = fields.Char(string="Meeting With")

    # telephone discussion
    discussion_type = fields.Selection(selection=[('internal', 'Internal'), ('external', 'External')],
                                       string="Discussion Type")
    discussion_with = fields.Char(string="Discussion With")
    discussion_ids = fields.Many2many('res.users', string="Discussion With")
    discussion_duration = fields.Float(string="Discussion Duration")

    # clerical works
    clerical_work_type = fields.Selection(
        selection=[('technical', 'Technical'), ('documentation', 'Documentation'), ('communication', 'Communication')],
        string="Work Type")

    # day to day works
    day_to_day_work_type = fields.Selection(
        selection=[('communication_with_student', 'Communication With Student'), ('mail', 'Mail'),
                   ('whatsapp', 'Whatsapp'), ('odoo', 'Odoo')], string="Work Type")

    # batch related works
    batch_related_work_type = fields.Selection(
        selection=[('attendance', 'Attendance'), ('clear_scheduling', 'Clear Scheduling'),
                   ('communication', 'Communication')], string="Work Type"
    )
    batch_id = fields.Many2one('logic.base.batch', string="Batch")
    description = fields.Text(string="Description")
    manager_id = fields.Many2one('hr.employee', 'Employee')
    owner_id = fields.Many2one('res.users', 'Task Owner')
    expected_completion = fields.Datetime('Expected Completion Date')
    remarks = fields.Text(string="Remarks")
    completed_on = fields.Datetime('Completed On')
    time_difference = fields.Float('Time Difference')
    expected_completed_status = fields.Char('Expected Completed Status')
    state = fields.Selection(
        [('draft', 'Draft'), ('submited', 'Submited'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='draft', string="Status")
    badge = fields.Selection([('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')], string="Badge")
    misc_id = fields.Integer()

    def action_submit(self):
        self.state = 'submited'

    def action_complete(self):
        if self.badge:
            misc = self.env['logic.task.other'].sudo().search([('id', '=', self.misc_id)])
            misc.badge = self.badge
            self.state = 'completed'
        else:
            raise UserError(_("Please Select Badge"))

    def action_cancel(self):
        self.state = 'cancelled'
