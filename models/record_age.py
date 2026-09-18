# -*- coding: utf-8 -*-
# Copyright 2026 Dhairvi / Rootways
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import logging
from datetime import datetime, timezone

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

# Inherit specs applied only when the parent view (and therefore the app)
# exists. This keeps a single module without depending on CRM/Sale/etc.
_RECORD_AGE_VIEWS = [
    # CRM
    {
        'xmlid': 'dhairvi_record_age.view_crm_lead_tree_leads_record_age',
        'name': 'crm.lead.tree.leads.record.age',
        'model': 'crm.lead',
        'inherit': 'crm.crm_case_tree_view_leads',
        'arch': """
            <field name="create_date" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_crm_lead_tree_oppor_record_age',
        'name': 'crm.lead.tree.opportunity.record.age',
        'model': 'crm.lead',
        'inherit': 'crm.crm_case_tree_view_oppor',
        'arch': """
            <field name="create_date" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_crm_lead_form_record_age',
        'name': 'crm.lead.form.record.age',
        'model': 'crm.lead',
        'inherit': 'crm.crm_lead_view_form',
        'arch': """
            <xpath expr="//sheet//field[@name='user_id']" position="after">
                <field name="record_age_days"/>
            </xpath>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_crm_lead_filter_leads_record_age',
        'name': 'crm.lead.search.leads.record.age',
        'model': 'crm.lead',
        'inherit': 'crm.view_crm_case_leads_filter',
        'arch': """
            <xpath expr="//search" position="inside">
                <separator/>
                <filter string="Created Today" name="dhairvi_record_age_today"
                        domain="[('create_date', '&gt;=', context_today().strftime('%Y-%m-%d'))]"/>
                <filter string="Older than 7 Days" name="dhairvi_record_age_gt_7"
                        domain="[('create_date', '&lt;', (context_today() - relativedelta(days=7)).strftime('%Y-%m-%d'))]"/>
                <filter string="Older than 14 Days" name="dhairvi_record_age_gt_14"
                        domain="[('create_date', '&lt;', (context_today() - relativedelta(days=14)).strftime('%Y-%m-%d'))]"/>
                <filter string="Older than 30 Days" name="dhairvi_record_age_gt_30"
                        domain="[('create_date', '&lt;', (context_today() - relativedelta(days=30)).strftime('%Y-%m-%d'))]"/>
            </xpath>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_crm_lead_filter_oppor_record_age',
        'name': 'crm.lead.search.opportunity.record.age',
        'model': 'crm.lead',
        'inherit': 'crm.view_crm_case_opportunities_filter',
        'arch': """
            <xpath expr="//search" position="inside">
                <separator/>
                <filter string="Created Today" name="dhairvi_record_age_today"
                        domain="[('create_date', '&gt;=', context_today().strftime('%Y-%m-%d'))]"/>
                <filter string="Older than 7 Days" name="dhairvi_record_age_gt_7"
                        domain="[('create_date', '&lt;', (context_today() - relativedelta(days=7)).strftime('%Y-%m-%d'))]"/>
                <filter string="Older than 14 Days" name="dhairvi_record_age_gt_14"
                        domain="[('create_date', '&lt;', (context_today() - relativedelta(days=14)).strftime('%Y-%m-%d'))]"/>
                <filter string="Older than 30 Days" name="dhairvi_record_age_gt_30"
                        domain="[('create_date', '&lt;', (context_today() - relativedelta(days=30)).strftime('%Y-%m-%d'))]"/>
            </xpath>
        """,
    },
    # Sales
    {
        'xmlid': 'dhairvi_record_age.view_order_tree_record_age',
        'name': 'sale.order.tree.record.age',
        'model': 'sale.order',
        'inherit': 'sale.view_order_tree',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_quotation_tree_record_age',
        'name': 'sale.order.quotation.tree.record.age',
        'model': 'sale.order',
        'inherit': 'sale.view_quotation_tree',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_order_form_record_age',
        'name': 'sale.order.form.record.age',
        'model': 'sale.order',
        'inherit': 'sale.view_order_form',
        'arch': """
            <xpath expr="//sheet//field[@name='user_id']" position="after">
                <field name="record_age_days"/>
            </xpath>
        """,
    },
    # Purchase
    {
        'xmlid': 'dhairvi_record_age.purchase_order_tree_record_age',
        'name': 'purchase.order.tree.record.age',
        'model': 'purchase.order',
        'inherit': 'purchase.purchase_order_tree',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.purchase_order_kpis_tree_record_age',
        'name': 'purchase.order.kpis.tree.record.age',
        'model': 'purchase.order',
        'inherit': 'purchase.purchase_order_kpis_tree',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.purchase_order_view_tree_record_age',
        'name': 'purchase.order.view.tree.record.age',
        'model': 'purchase.order',
        'inherit': 'purchase.purchase_order_view_tree',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.purchase_order_form_record_age',
        'name': 'purchase.order.form.record.age',
        'model': 'purchase.order',
        'inherit': 'purchase.purchase_order_form',
        'arch': """
            <xpath expr="//sheet//field[@name='user_id']" position="after">
                <field name="record_age_days"/>
            </xpath>
        """,
    },
    # Project
    {
        'xmlid': 'dhairvi_record_age.view_task_tree_record_age',
        'name': 'project.task.tree.record.age',
        'model': 'project.task',
        'inherit': 'project.view_task_tree2',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_task_form_record_age',
        'name': 'project.task.form.record.age',
        'model': 'project.task',
        'inherit': 'project.view_task_form2',
        'arch': """
            <xpath expr="//sheet//field[@name='user_ids']" position="after">
                <field name="record_age_days"/>
            </xpath>
        """,
    },
    # Invoices / vendor bills (Accounting)
    {
        'xmlid': 'dhairvi_record_age.view_invoice_tree_record_age',
        'name': 'account.move.invoice.tree.record.age',
        'model': 'account.move',
        'inherit': 'account.view_invoice_tree',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.view_move_form_record_age',
        'name': 'account.move.form.record.age',
        'model': 'account.move',
        'inherit': 'account.view_move_form',
        'arch': """
            <xpath expr="//sheet//field[@name='invoice_date']" position="after">
                <field name="record_age_days"/>
            </xpath>
        """,
    },
    # Manufacturing orders
    {
        'xmlid': 'dhairvi_record_age.mrp_production_tree_record_age',
        'name': 'mrp.production.tree.record.age',
        'model': 'mrp.production',
        'inherit': 'mrp.mrp_production_tree_view',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.mrp_production_form_record_age',
        'name': 'mrp.production.form.record.age',
        'model': 'mrp.production',
        'inherit': 'mrp.mrp_production_form_view',
        'arch': """
            <xpath expr="//sheet//field[@name='product_id']" position="after">
                <field name="record_age_days"/>
            </xpath>
        """,
    },
    # Helpdesk (Enterprise). Skipped automatically on Community.
    {
        'xmlid': 'dhairvi_record_age.helpdesk_tickets_view_tree_record_age',
        'name': 'helpdesk.ticket.tree.record.age',
        'model': 'helpdesk.ticket',
        'inherit': 'helpdesk.helpdesk_tickets_view_tree',
        'arch': """
            <field name="name" position="after">
                <field name="record_age_days" optional="show"/>
            </field>
        """,
    },
    {
        'xmlid': 'dhairvi_record_age.helpdesk_ticket_view_form_record_age',
        'name': 'helpdesk.ticket.form.record.age',
        'model': 'helpdesk.ticket',
        'inherit': 'helpdesk.helpdesk_ticket_view_form',
        'arch': """
            <xpath expr="//sheet//field[@name='user_id']" position="after">
                <field name="record_age_days"/>
            </xpath>
        """,
    },
]


class Base(models.AbstractModel):
    """Add Record Age to every Odoo model.

    The field is computed and not stored. It is only displayed on views we
    inject for CRM, Sales, Purchase, Invoices, Manufacturing, Project, and
    Helpdesk when those apps are installed. Other models still have the field
    available (for example via Studio).
    """

    _inherit = 'base'

    record_age_days = fields.Integer(
        string='Record Age',
        compute='_compute_record_age_days',
        readonly=True,
        help='Whole calendar days between this record creation date and '
             'today, in the current user timezone. Recalculated on each '
             'read; it is not stored.',
    )

    def _dhairvi_record_age_as_utc_datetime(self, create_date):
        """Normalize ORM ``create_date`` to a naive UTC datetime, or False."""
        if not create_date:
            return False
        if isinstance(create_date, datetime):
            value = create_date
        else:
            value = fields.Datetime.to_datetime(create_date)
        if not value:
            return False
        if value.tzinfo:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    @api.model
    def _dhairvi_calendar_days_since(self, create_date, today=None):
        """Return whole calendar days from ``create_date`` until today.

        Calendar-day semantics (not elapsed hours):
        - created today → 0
        - created yesterday → 1
        - created 10 calendar days ago → 10

        ``create_date`` is stored naive UTC. It is converted with
        ``fields.Datetime.context_timestamp`` (context tz, else the user's
        tz, else UTC). Today comes from ``fields.Date.context_today``.
        The browser clock is never used.

        Missing or future create dates return 0 (never negative).
        """
        utc_dt = self._dhairvi_record_age_as_utc_datetime(create_date)
        if not utc_dt:
            return 0
        local_dt = fields.Datetime.context_timestamp(self, utc_dt)
        created_on = local_dt.date()
        if today is None:
            today = fields.Date.context_today(self)
        return max(0, (today - created_on).days)

    @api.depends_context('tz')
    def _compute_record_age_days(self):
        # Not stored, so this runs on each read. Do not @depends('create_date'):
        # models with _log_access = False have no create_date and would crash
        # registry setup if that dependency were declared on base.
        for record in self:
            create_date = (
                record.create_date if 'create_date' in record._fields else False
            )
            record.record_age_days = record._dhairvi_calendar_days_since(
                create_date
            )


class DhairviRecordAgeSetup(models.AbstractModel):
    """Load inherited views only when the parent app is installed."""

    _name = 'dhairvi.record.age.setup'
    _description = 'Record Age view setup'

    def _register_hook(self):
        super()._register_hook()
        self._ensure_record_age_views()

    def _ensure_record_age_views(self):
        View = self.env['ir.ui.view'].sudo()
        Imd = self.env['ir.model.data'].sudo()
        for spec in _RECORD_AGE_VIEWS:
            if spec['model'] not in self.env:
                continue
            parent = self.env.ref(spec['inherit'], raise_if_not_found=False)
            if not parent:
                continue
            existing = self.env.ref(spec['xmlid'], raise_if_not_found=False)
            if existing:
                continue
            vals = {
                'name': spec['name'],
                'model': spec['model'],
                'inherit_id': parent.id,
                'mode': 'extension',
                'arch': spec['arch'].strip(),
            }
            try:
                view = View.create(vals)
                module, name = spec['xmlid'].split('.', 1)
                xmlid = Imd.search([
                    ('module', '=', module),
                    ('name', '=', name),
                ], limit=1)
                if xmlid:
                    xmlid.write({
                        'model': 'ir.ui.view',
                        'res_id': view.id,
                    })
                else:
                    Imd.create({
                        'module': module,
                        'name': name,
                        'model': 'ir.ui.view',
                        'res_id': view.id,
                        'noupdate': False,
                    })
            except Exception as exc:
                _logger.warning(
                    'Dhairvi Record Age: skipped view %s (%s)',
                    spec['xmlid'],
                    exc,
                )
