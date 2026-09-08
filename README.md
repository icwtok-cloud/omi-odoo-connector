# omi-odoo-connector — paquete de push

Este zip contiene el módulo "Export Data to OMI" ya preparado para las
6 versiones de Odoo que soporta el motor (14.0 a 19.0), cada una en su
propia carpeta bajo `versions/`, con el `__manifest__.py` ya ajustado
al prefijo de versión correspondiente.

    versions/
    ├── 14.0/omi_export_connector/
    ├── 15.0/omi_export_connector/
    ├── 16.0/omi_export_connector/
    ├── 17.0/omi_export_connector/
    ├── 18.0/omi_export_connector/
    └── 19.0/omi_export_connector/

Cada carpeta `omi_export_connector/` es IDÉNTICA salvo por la línea
`"version"` del manifest -- el wizard/vistas/lógica son estables en
todo ese rango de versiones de Odoo.

## Por qué una rama de git por versión

Odoo Apps Store escanea el repo por RAMA -- cada rama debe llamarse
igual que la serie de Odoo que soporta ("14.0", "15.0", etc.) y debe
contener la(s) carpeta(s) de módulo directamente en la raíz de esa
rama. El script de PowerShell que te paso hace esto automáticamente:
crea una rama por versión, copia SOLO la carpeta de esa versión a la
raíz del repo en esa rama, y la pushea.

Ver PUSH_STEPS.md para los comandos exactos.
