# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectRisk(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectRisk, cls).setUpClass()
        cls.table_model = cls.env['project.risk.table']
        cls.opportunity_model = cls.env['project.opportunity.table']
        cls.probability = cls.env.ref('project_risk.probab1')
        cls.impact = cls.env.ref('project_risk.impact1')
        cls.chance_prob = cls.env.ref('project_risk.prob1')
        cls.chance_prof = cls.env.ref('project_risk.prof1')
        cls.project = cls.env['project.project'].create({
            'name': 'Test Project',
        })
        cls.risk = cls.env['project.risk.risk'].create({
            'name': 'Test Risk',
            'description': 'Risk description',
        })
        cls.action1 = cls.env['project.risk.action'].create({
            'name': 'Test Action',
            'description': 'Action description',
        })
        cls.chance = cls.env['project.opportunity.opportunity'].create({
            'name': 'Test Chance',
            'description': 'Chance description',
        })
        cls.action2 = cls.env['project.opportunity.action'].create({
            'name': 'Test Action',
            'description': 'Action description',
        })
        cls.setting = cls.env['res.config.settings'].create({})

    def test_risk_table(self):
        table = self.table_model.create({
            'project_id': self.project.id,
        })
        self.assertFalse(table.risk_level)
        table.write({
            'probability_id': self.probability.id,
            'impact_id': False,
        })
        self.assertFalse(table.risk_level)
        table.write({
            'probability_id': False,
            'impact_id': self.impact.id,
        })
        self.assertFalse(table.risk_level)
        table.write({
            'probability_id': self.probability.id,
            'impact_id': self.impact.id,
        })
        self.assertFalse(table.level_surpassed)
        self.assertTrue(table.risk_level)
        self.setting.risk_limit = 0.00001
        self.setting.set_values()
        table.invalidate_cache()
        self.assertTrue(table.level_surpassed)
        self.assertEquals(
            round(table.risk_level, 4),
            round(self.impact.rating * self.probability.rating, 4))

    def test_chance_table(self):
        table = self.opportunity_model.create({
            'project_id': self.project.id,
        })
        self.assertFalse(table.chance_level)
        table.write({
            'probability_id': self.chance_prob.id,
            'impact_id': False,
        })
        self.assertFalse(table.chance_level)
        table.write({
            'probability_id': False,
            'impact_id': self.chance_prof.id,
        })
        self.assertFalse(table.chance_level)
        table.write({
            'probability_id': self.chance_prob.id,
            'impact_id': self.chance_prof.id,
        })
        self.assertTrue(table.chance_level)
        self.assertEquals(
            round(table.chance_level, 4),
            round(self.chance_prof.rating *
                  self.chance_prob.rating, 4))

    def test_onchange_risk_id(self):
        table = self.table_model.create({
            'project_id': self.project.id,
            'risk_id': self.risk.id,
        })
        self.assertFalse(table.risk)
        table.onchange_risk_id()
        self.assertEquals(table.risk,
                          table.risk_id.description)

    def test_onchange_action_id(self):
        table = self.table_model.create({
            'project_id': self.project.id,
            'action_id': self.action1.id,
        })
        self.assertFalse(table.action)
        table.onchange_action_id()
        self.assertEquals(table.action,
                          table.action_id.description)

    def test_onchange_chance_id(self):
        table = self.opportunity_model.create({
            'project_id': self.project.id,
            'opportunity_id': self.chance.id,
        })
        self.assertFalse(table.opportunity)
        table.onchange_opportunity_id()
        self.assertEquals(table.opportunity,
                          table.opportunity_id.description)

    def test_prob_onchange(self):
        table = self.opportunity_model.create({
            'project_id': self.project.id,
            'action_id': self.action2.id,
        })
        self.assertFalse(table.action)
        table.onchange_action_id()
        self.assertEquals(table.action,
                          table.action_id.description)

    def test_res_config(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        self.assertFalse(
            self.setting.risk_limit)
        self.setting.risk_limit = 2.0
        self.setting.set_values()
        self.assertEqual(
            self.setting.risk_limit,
            float(get_param('project_risk.risk_limit', '0.0')))

    def test_project_disable_enable(self):
        self.assertTrue(self.project.active)
        for risk in self.project.with_context(
                active_test=False).risk_table_ids:
            self.assertTrue(risk.active)
        self.project.toggle_active()
        self.assertFalse(self.project.active)
        for risk in self.project.with_context(
                active_test=False).risk_table_ids:
            self.assertFalse(risk.active)
        self.project.toggle_active()
        self.assertTrue(self.project.active)
        for risk in self.project.with_context(
                active_test=False).risk_table_ids:
            self.assertTrue(risk.active)

        self.assertTrue(self.project.active)
        for chance in self.project.with_context(
                active_test=False).risk_chance_table_ids:
            self.assertTrue(chance.active)
        self.project.toggle_active()
        self.assertFalse(self.project.active)
        for chance in self.project.with_context(
                active_test=False).risk_chance_table_ids:
            self.assertFalse(chance.active)
        self.project.toggle_active()
        self.assertTrue(self.project.active)
        for chance in self.project.with_context(
                active_test=False).risk_chance_table_ids:
            self.assertTrue(chance.active)
