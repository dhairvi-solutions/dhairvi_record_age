# -*- coding: utf-8 -*-
# Copyright 2026 Dhairvi Solutions LLP
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, SUPERUSER_ID


def _env_from_hook(cr_or_env, registry=None):
    """Odoo 16/17 pass (cr, registry); 18/19 may pass env as the first argument."""
    if registry is None and hasattr(cr_or_env, 'cr'):
        return cr_or_env
    return api.Environment(cr_or_env, SUPERUSER_ID, {})


def post_init_hook(cr_or_env, registry=None):
    env = _env_from_hook(cr_or_env, registry)
    env['dhairvi.record.age.setup']._ensure_record_age_views()
