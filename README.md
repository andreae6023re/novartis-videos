# Novartis Kaltura Scanner

## 1. Instalar dependencias

```bash
pip install -r requirements.txt
playwright install chromium
```

## 2. Crear la sesión

```bash
python login.py
```

Se abrirá Chromium. Inicia sesión manualmente y pulsa ENTER en el terminal.

La sesión se guardará en `auth/session.json`.

IMPORTANTE: `auth/session.json` contiene información sensible de sesión.
No lo subas a GitHub.

## 3. Ejecutar el detector

```bash
python scanner.py
```

Esta primera versión prueba las URLs de `urls.txt` y busca:

- kalturaPlayer.loadMedia(...)
- entryId
- data-entry-id
- bloques Kaltura

La siguiente versión añadirá captura de peticiones de red y exportación a Excel.
