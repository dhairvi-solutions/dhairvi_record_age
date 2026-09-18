# Dhairvi Record Age — Testing Checklist

Run these checks on each target version before packaging for the Apps Store.

## Odoo 16 / 17 / 18 / 19

On a database of that exact series:

### Install

* [ ] Apps list shows **Dhairvi Record Age**
* [ ] Module installs without traceback
* [ ] Server log has no errors after install
* [ ] Upgrade the module (`-u dhairvi_record_age`) without errors
* [ ] Uninstall and reinstall (fresh install) without leftover menus or access errors

### CRM installed

* [ ] Lead list and opportunity list show **Record Age**
* [ ] Lead/opportunity form shows **Record Age**
* [ ] New record → 0
* [ ] Record created yesterday → 1
* [ ] Several records with different `create_date` values show the matching day counts
* [ ] Filters work: Created Today, Older than 7 / 14 / 30 Days
* [ ] A user without CRM access still cannot open CRM records (no extra rights granted)

### Sales / Purchase / Invoicing / Manufacturing / Project installed

* [ ] List view shows Record Age
* [ ] Form view shows Record Age
* [ ] New record → 0

### Helpdesk (Enterprise only)

* [ ] Ticket list and form show Record Age when Helpdesk is installed

### Optional apps not installed

* [ ] CRM not installed → module still installs; no `crm.lead` error
* [ ] Sales not installed → no `sale.order` error
* [ ] Purchase not installed → no `purchase.order` error
* [ ] Invoicing / Accounting not installed → no `account.move` error
* [ ] Manufacturing not installed → no `mrp.production` error
* [ ] Project not installed → no `project.task` error
* [ ] Helpdesk not installed / Community edition → no error
* [ ] Install CRM *after* Record Age → Record Age column appears after restart / registry reload

### Timezone

* [ ] User timezone UTC vs America/Los_Angeles around midnight UTC: calendar day (and therefore Record Age) follows the **user** timezone, not the browser clock

### Automated tests

```bash
odoo-bin -c /path/to/odoo.conf -d DATABASE \
    --test-enable --stop-after-init \
    --test-tags /dhairvi_record_age \
    -i dhairvi_record_age
```
