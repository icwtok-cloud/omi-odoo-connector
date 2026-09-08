# -*- coding: utf-8 -*-
import base64
import io
import csv

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


# Mismo mapeo módulo OMI -> modelo técnico de Odoo que usa el generador
# de reglas del backend (rules-generator/scripts/module_map.py), para
# que el archivo exportado desde acá siempre respete la misma
# convención que el motor de validación espera del otro lado.
OMI_MODULE_MODELS = {
    "contactos": {
        "label": _("Contacts"),
        "model": "res.partner",
        "default_fields": ["name", "email", "phone", "vat", "street", "city", "country_id"],
    },
    "crm": {
        "label": _("CRM"),
        "model": "crm.lead",
        "default_fields": ["name", "partner_name", "email_from", "phone", "stage_id", "expected_revenue"],
    },
    "ventas": {
        "label": _("Sales"),
        "model": "sale.order",
        "default_fields": ["name", "partner_id", "date_order", "amount_total", "state"],
    },
    "facturacion": {
        "label": _("Invoicing"),
        "model": "account.move",
        "default_fields": ["name", "partner_id", "invoice_date", "amount_total", "state"],
    },
    "inventario": {
        "label": _("Inventory"),
        "model": "stock.quant",
        "default_fields": ["product_id", "location_id", "quantity"],
    },
    "productos": {
        "label": _("Products"),
        "model": "product.template",
        "default_fields": ["name", "default_code", "list_price", "categ_id", "type"],
    },
    "contabilidad": {
        "label": _("Accounting"),
        "model": "account.account",
        "default_fields": ["code", "name", "account_type"],
    },
    "compras": {
        "label": _("Purchase"),
        "model": "purchase.order",
        "default_fields": ["name", "partner_id", "date_order", "amount_total", "state"],
    },
}

class OmiExportWizard(models.TransientModel):
    """Wizard: exporta datos en un CSV con la estructura que el motor de
    validación de OMI (https://omi.lat) espera, y ofrece abrir OMI en el
    navegador para subir el archivo y ver el reporte de validación
    gratis, antes de importar o pagar nada.

    Nota de arquitectura: este módulo NO llama a la API de OMI desde
    Odoo -- OMI autentica solo con sesión de Clerk (JWT de navegador),
    no hay API key todavía. Por eso el flujo es exportar acá + subir a
    mano en la pestaña que se abre. Si en el futuro OMI expone una API
    key, este wizard es el lugar natural para automatizar el upload.
    """

    _name = "omi.export.wizard"
    _description = "Export & Validate Data with OMI"

    omi_module = fields.Selection(
        selection="_selection_omi_module",
        string="OMI Module",
        required=True,
        default="contactos",
        help="Choose the data type you want to export and validate. "
        "This must match the module you'll select on OMI's website. "
        "Only modules whose underlying Odoo app is installed appear here.",
    )

    @api.model
    def _selection_omi_module(self):
        """Solo ofrece los módulos cuyo modelo técnico existe en este
        registry -- es decir, cuya app de Odoo (crm, sale, account,
        stock, purchase) está realmente instalada. 'contactos' siempre
        aparece porque 'contacts' es una dependencia dura del módulo."""
        return [
            (key, val["label"])
            for key, val in OMI_MODULE_MODELS.items()
            if val["model"] in self.env
        ]
    domain_filter = fields.Char(
        string="Filter (optional)",
        help="Optional Odoo domain to restrict which records are exported, "
        "e.g. [('active','=',True)]. Leave empty to export all records "
        "of the selected type.",
    )
    export_file = fields.Binary(string="Exported File", readonly=True)
    export_filename = fields.Char(string="File Name", readonly=True)
    state = fields.Selection(
        [("draft", "Draft"), ("done", "Done")],
        default="draft",
    )

    def _get_model_config(self):
        config = OMI_MODULE_MODELS.get(self.omi_module)
        if not config:
            raise UserError(_("Unknown OMI module selection."))
        return config

    def action_export(self):
        """Genera el CSV y deja el wizard en estado 'done' con el
        archivo adjunto, listo para descargar."""
        self.ensure_one()
        config = self._get_model_config()
        model_name = config["model"]
        field_names = config["default_fields"]

        Model = self.env[model_name].sudo()

        domain = []
        if self.domain_filter:
            try:
                domain = safe_eval(self.domain_filter)
            except Exception as e:
                raise UserError(
                    _("Could not parse the filter. Use a valid Odoo domain, e.g. "
                      "[('active','=',True)]. Error: %s") % e
                )

        records = Model.search(domain)
        if not records:
            raise UserError(_("No records found for the selected module and filter."))

        buffer = io.StringIO()
        writer = csv.writer(buffer)

        # Header: usa el path de campo tal cual (ej. country_id) -- OMI
        # resuelve relaciones Many2one por nombre de columna + valor
        # legible, igual que espera el importador nativo de Odoo.
        writer.writerow(field_names)

        for record in records:
            row = []
            for field_name in field_names:
                value = record[field_name]
                if hasattr(value, "display_name"):
                    # Many2one -> nombre legible (mismo criterio que
                    # exporta el importador nativo de Odoo)
                    row.append(value.display_name if value else "")
                else:
                    row.append(value if value is not False else "")
            writer.writerow(row)

        content = buffer.getvalue().encode("utf-8-sig")  # BOM: Excel-friendly
        filename = "omi_export_%s.csv" % self.omi_module

        self.write(
            {
                "export_file": base64.b64encode(content),
                "export_filename": filename,
                "state": "done",
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "omi.export.wizard",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_open_omi(self):
        """Abre OMI (servicio externo independiente) en una pestaña
        nueva para que el usuario suba el archivo ya exportado y vea el
        reporte de validación gratis. No se manda ningún dato de la
        base del cliente a OMI desde acá -- el upload lo hace el propio
        usuario, a mano, en su navegador."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "https://omi.lat/app",
            "target": "new",
        }
