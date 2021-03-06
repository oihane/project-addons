# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common

str2date = fields.Date.from_string


class TestProjectBudgetExpense(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectBudgetExpense, cls).setUpClass()
        position_model = cls.env['account.budget.post']
        cls.position = position_model.search([('expenses', '=', True)])
        if not cls.position:
            cls.position = position_model.create({
                'name': 'Expenses Position',
                'expenses': True,
                'account_ids': [
                    (4, x.id) for x in cls.env['account.account'].search(
                        [('deprecated', '=', False)], limit=1)],

            })
        cls.project_model = cls.env['project.project']
        cls.template = cls.env.ref('project_budget.project_budget_template')
        cls.template.write({
            'budget_post_ids': [(4, cls.position.id)]
        })
        cls.project = cls.project_model.create({
            'name': 'New Project',
        })
        cls.task_model = cls.env['project.task']
        month_gap = 2
        date_start = str2date(fields.Datetime.now()) + relativedelta(days=1)
        date_end = date_start + relativedelta(months=month_gap)
        cls.task = cls.task_model.create({
            'name': 'Name',
            'planned_hours': 30.0,
            'employee_cost': 20.0,
            'user_id': cls.env.user.id,
            'date_start': date_start,
            'date_end': date_end,
            'project_id': cls.project.id,
        })

    def test_budget_distribution(self):
        self.assertTrue(self.task.planned_cost)
        budget = self.project.budget_ids[:1]
        budget.budget_tmpl_id = self.template
        budget.button_compute_lines()
        self.assertNotEquals(
            round(self.task.planned_cost, 2),
            abs(round(sum(budget.crossovered_budget_line.filtered(
                lambda l: l.general_budget_id.expenses).mapped(
                'planned_amount')), 2)))
        budget.button_distribute_task_costs()
        self.assertEquals(
            round(self.task.planned_cost, 2),
            abs(round(sum(budget.crossovered_budget_line.filtered(
                lambda l: l.general_budget_id.expenses).mapped(
                'planned_amount')), 2)))
