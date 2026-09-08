# -*- coding: utf-8 -*-
{
    # Nombre <=25 caracteres, sin nombre de la empresa (icwtok-cloud),
    # sin adjetivos -- OMI es el nombre del servicio destino, no la
    # empresa vendedora, así que es válido incluirlo (ver guidelines).
    "name": "Export Data to OMI",
    # Semver Odoo: <serie_odoo>.<major>.<minor>.<bugfix> -- se actualiza
    # el prefijo en cada rama de versión (18.0.x en esta rama).
    "version": "14.0.1.0.0",
    "category": "Extra Tools",
    "summary": "Export and pre-validate your data before importing into Odoo",
    "description": """
Export & Validate Data Before Importing Into Odoo
==================================================

Prepares an export of your Contacts, CRM, Sales, Invoicing, Inventory,
Products, Accounting or Purchase records in the exact format OMI's
validation engine expects for your Odoo version.

What this module does
----------------------
* Adds an "Export & Validate" wizard, available from the relevant menus.
* Lets you pick the module (Contacts, CRM, Sales, etc.) and the records
  or filter to export.
* Generates a clean CSV/Excel file with the right headers for your
  Odoo version.
* Opens OMI (an external, independent data-preparation service) in your
  browser so you can upload the file and see a full validation report
  free of charge, before paying for anything.

Why this exists
----------------
Odoo's native import rejects rows with unclear or missing errors. OMI's
validation engine checks your export against the real field
definitions, required fields, and relation values of your specific
Odoo version and module, so you know exactly what to fix before you
import -- or before you migrate from an older, unsupported version.

Requires an external service
------------------------------
This module requires OMI (https://omi.lat), an independent web service,
to perform the actual validation. A free tier is available. No account
or payment is required to install or use the export wizard itself.
""",
    "author": "icwtok-cloud",
    "license": "LGPL-3",
    "website": "https://omi.lat",
    "support": "soporte@omi.lat",
    # URL de instancia demo donde se puede probar el wizard funcionando
    # de verdad antes de instalar -- pedido opcional del manifest.
    "live_test_url": "https://omi.lat/guias/preparar-datos-para-importar-en-odoo",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/omi_export_wizard_views.xml",
    ],
    "images": [
        "static/description/banner.png",
        "static/description/icon.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
