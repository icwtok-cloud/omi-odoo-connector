# Export Data to OMI

Odoo connector module for [OMI](https://omi.lat) — an independent,
deterministic data-validation engine for Odoo imports/migrations.

## What this module does

Adds an **"Export & Validate with OMI"** wizard (menu: Contacts →
Export & Validate with OMI) that:

1. Lets the user pick an OMI module (Contacts, CRM, Sales, Invoicing,
   Inventory, Products, Accounting, Purchase) — only modules whose
   underlying Odoo app is installed are shown.
2. Exports the matching records to a CSV file with headers matching
   the field structure OMI's validation engine expects.
3. Opens `https://omi.lat/app` in a new browser tab so the user can
   upload the file and get a free validation report before importing
   anything or paying for anything.

## Why it doesn't call the OMI API directly

OMI's backend authenticates exclusively via short-lived Clerk session
JWTs (browser-based login) — there is no API key mechanism yet. A
server-side Odoo module has no practical way to obtain a valid Clerk
session token non-interactively. Until OMI exposes an API-key-based
auth path, this module's job ends at "export a clean file + open OMI
in the browser" — the user does the upload step themselves, with their
own OMI account/session.

If OMI adds API key auth in the future, `action_export` /
`action_open_omi` in `wizards/omi_export_wizard.py` are the natural
place to wire up an automatic upload + inline result instead.

## Module ↔ Odoo model mapping

Mirrors `rules-generator/scripts/module_map.py` in the OMI backend
repo, so the exported column structure stays consistent with what the
validation engine expects on the other side:

| OMI module    | Odoo model         |
|---------------|---------------------|
| contactos     | res.partner         |
| crm           | crm.lead             |
| ventas        | sale.order           |
| facturacion   | account.move         |
| inventario    | stock.quant          |
| productos     | product.template     |
| contabilidad  | account.account      |
| compras       | purchase.order       |

## Multi-version support (14.0 - 19.0)

This repository follows the standard Odoo Apps Store convention: **one
branch per Odoo series**, each containing this same module adapted to
that version's API where needed (field names/APIs are stable for this
wizard's scope across 14.0-19.0, so branch diffs should mostly be the
`version` string in `__manifest__.py`).

Branches: `14.0`, `15.0`, `16.0`, `17.0`, `18.0`, `19.0`.

## Local install (dev/testing)

```bash
cp -r omi_export_connector /path/to/odoo/addons/
# Restart Odoo with -u omi_export_connector, or Apps > Update Apps List
# then search "Export Data to OMI" and install.
```

## Demo video (YouTube Short)

`static/description/index.html` has a placeholder `VIDEO_ID_AQUI` embed.
Once the Short is uploaded:

1. Copy the video ID from the Short's URL: `youtube.com/shorts/<ID>`.
2. Replace both occurrences of `VIDEO_ID_AQUI` in
   `static/description/index.html` with that ID.

The embed uses Bootstrap 4's `embed-responsive-1by1` (square) container
instead of a custom 9:16 wrapper, because Odoo's Store guidelines only
allow Bootstrap 4 classes plus `color`/`font-*`/`margin-*`/`padding-*`/
`border-*` inline attributes in the description page — a hand-rolled
`position: absolute` vertical-video wrapper risks being flagged as
"harmful style" and unpublishing the whole listing. `1by1` isn't a
perfect fit for a vertical video but stays fully within the whitelisted
classes.

## License

LGPL-3
