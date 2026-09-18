# Dhairvi Record Age

Show how many calendar days have passed since an Odoo record was created.

Example: created on 2026-09-01, today 2026-09-14 → **Record Age: 13**.

The value is computed from Odoo’s `create_date` on each read. It is not stored, so it cannot go stale, and the module does not use a cron job.

---

## Features

* Shows the number of whole calendar days since record creation
* One module: `dhairvi_record_age` (depends only on `base`)
* Does not force CRM, Sales, Purchase, Invoicing, Manufacturing, Project, or Helpdesk to be installed
* List/form columns appear when those apps are present
* No external services, APIs, or extra Python packages
* No cron jobs, menus, or configuration pages
* Recalculated automatically whenever the field is displayed

---

## Supported Versions

Single codebase aimed at:

* Odoo 16.0
* Odoo 17.0
* Odoo 18.0
* Odoo 19.0

APIs are limited to ones that exist on all four series (`fields.Date.context_today`, `fields.Datetime.context_timestamp`, inherited views, no `<tree>`/`<list>` xpath). Runtime install and tests in this repo were run on **Odoo 19**. Use `TESTING.md` on 16, 17, and 18 before submitting each Apps Store series.

---

## Architecture

Everything lives in **one** addon: `dhairvi_record_age`.

* `record_age_days` is added on `base`, so every Odoo model has the computed field.
* Inherited list/form/search views are created only if the parent view exists.
  CRM not installed → no CRM views, and no install error.
  Install CRM later → Record Age columns are added on the next registry load.

That is how a single module can support optional apps without listing them in `depends`.

To show the column on another list view, inherit that view and add:

```xml
<field name="record_age_days" optional="show"/>
```

---

## Installation

1. Copy `dhairvi_record_age` into your addons path.
2. Update the Apps list (developer mode → Apps → Update Apps List).
3. Install **Dhairvi Record Age**.
4. Restart the Odoo service if your deployment requires it after adding modules.

Standard Odoo addon installation: the module must be on a path listed in `addons_path`. No extra system packages are required.

If you previously installed the old `dhairvi_record_age_*` bridge modules, uninstall those extras. They are no longer used.

For the Odoo Apps Store, publish **only** this `dhairvi_record_age` folder as its own Git repository on branch `19.0`. Do not scan a parent folder that also contains other addons.

---

## Configuration

No configuration is required. There is no settings page.

Record Age uses the user’s timezone (`tz` on the user, or UTC if unset). It does not use the browser clock.

---

## Usage

After install, open a supported list view, for example **CRM → Sales → My Pipeline**, **Sales → Orders**, **Invoicing → Invoices**, or **Manufacturing → Orders** (list view):

| Opportunity | Created On | Record Age |
|-------------|------------|------------|
| ABC Opportunity | 2026-09-01 | 13 |
| XYZ Opportunity | 2026-09-10 | 4 |
| Test Opportunity | 2026-09-14 | 0 |

The same field is shown on the form, next to the salesperson / buyer / assignees.

On CRM leads and opportunities, search filters are available:

* Created Today
* Older than 7 Days
* Older than 14 Days
* Older than 30 Days

Those filters search on `create_date`, which is equivalent to Record Age without storing a value that would go stale.

---

## Technical Notes

* Field: `record_age_days` (Integer, computed, not stored, not editable).
* Source: Odoo `create_date` (naive UTC datetime).
* Calendar-day math: convert `create_date` to the user’s timezone, take the date, subtract from today’s date in that same timezone.
* Hours are ignored. A record created 23 hours ago today is still **0** days old.
* Missing `create_date` → 0. A future `create_date` → 0 (never negative).
* Access rights: none added. Anyone who can read the record can see Record Age.

---

## License

LGPL-3

---

## Support

* Website: https://www.dhairvi.com
* Email: info@dhairvi.com
