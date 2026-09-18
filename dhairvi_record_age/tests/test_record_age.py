# -*- coding: utf-8 -*-
# Copyright 2026 Dhairvi Solutions LLP
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from datetime import date, datetime

from odoo import fields
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestDhairviRecordAge(TransactionCase):
    def _records(self):
        return self.env['res.partner'].with_context(tz='UTC')

    def test_field_exists_without_optional_apps(self):
        self.assertIn('record_age_days', self.env['res.partner']._fields)
        self.assertIn('record_age_days', self.env['res.users']._fields)

    def test_missing_create_date_is_zero(self):
        self.assertEqual(self._records()._dhairvi_calendar_days_since(False), 0)
        self.assertEqual(self._records()._dhairvi_calendar_days_since(None), 0)

    def test_same_calendar_day_is_zero(self):
        created = datetime(2026, 9, 14, 23, 0, 0)
        self.assertEqual(
            self._records()._dhairvi_calendar_days_since(
                created, today=date(2026, 9, 14)
            ),
            0,
        )

    def test_yesterday_is_one_day(self):
        created = datetime(2026, 9, 13, 12, 0, 0)
        self.assertEqual(
            self._records()._dhairvi_calendar_days_since(
                created, today=date(2026, 9, 14)
            ),
            1,
        )

    def test_ten_days_ago(self):
        created = datetime(2026, 9, 4, 8, 0, 0)
        self.assertEqual(
            self._records()._dhairvi_calendar_days_since(
                created, today=date(2026, 9, 14)
            ),
            10,
        )

    def test_future_create_date_is_not_negative(self):
        created = datetime(2026, 9, 17, 8, 0, 0)
        self.assertEqual(
            self._records()._dhairvi_calendar_days_since(
                created, today=date(2026, 9, 14)
            ),
            0,
        )

    def test_hours_do_not_count_as_extra_days(self):
        created = datetime(2026, 9, 13, 1, 0, 0)
        self.assertEqual(
            self._records()._dhairvi_calendar_days_since(
                created, today=date(2026, 9, 14)
            ),
            1,
        )

    def test_timezone_changes_calendar_day_near_utc_midnight(self):
        create_date = datetime(2026, 9, 14, 2, 0, 0)
        today = date(2026, 9, 14)
        days_utc = self.env['res.partner'].with_context(
            tz='UTC'
        )._dhairvi_calendar_days_since(create_date, today=today)
        days_pacific = self.env['res.partner'].with_context(
            tz='America/Los_Angeles'
        )._dhairvi_calendar_days_since(create_date, today=today)
        self.assertEqual(days_utc, 0)
        self.assertEqual(days_pacific, 1)

    def test_live_now_is_zero_days(self):
        self.assertEqual(
            self._records()._dhairvi_calendar_days_since(fields.Datetime.now()),
            0,
        )

    def test_optional_views_follow_installed_apps(self):
        mapping = [
            ('crm.lead', 'dhairvi_record_age.view_crm_lead_tree_oppor_record_age'),
            ('sale.order', 'dhairvi_record_age.view_order_tree_record_age'),
            ('purchase.order', 'dhairvi_record_age.purchase_order_tree_record_age'),
            ('account.move', 'dhairvi_record_age.view_invoice_tree_record_age'),
            ('mrp.production', 'dhairvi_record_age.mrp_production_tree_record_age'),
            ('project.task', 'dhairvi_record_age.view_task_tree_record_age'),
            ('helpdesk.ticket', 'dhairvi_record_age.helpdesk_tickets_view_tree_record_age'),
        ]
        for model_name, xmlid in mapping:
            view = self.env.ref(xmlid, raise_if_not_found=False)
            if model_name in self.env:
                self.assertTrue(
                    view,
                    'Expected Record Age view %s when %s is installed'
                    % (xmlid, model_name),
                )
            else:
                self.assertFalse(
                    view,
                    'Did not expect Record Age view %s without %s'
                    % (xmlid, model_name),
                )
