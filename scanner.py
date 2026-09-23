from pathlib import Path
import re
from playwright.sync_api import sync_playwright

AUTH_FILE = Path("auth/session.json")
URLS_FILE = Path("urls.txt")

PATTERNS = [
    re.compile(r'kalturaPlayer\.loadMedia\s*\(\s*\{\s*entryId\s*:\s*["\']([^"\']+)["\']', re.I),
    re.compile(r'["\']entryId["\']\s*:\s*["\']([^"\']+)["\']', re.I),
    re.compile(r'data-entry-id\s*=\s*["\']([^"\']+)["\']', re.I),
]

def unique(items):
    return list(dict.fromkeys(items))

urls = [
    line.strip()
    for line in URLS_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        storage_state=str(AUTH_FILE) if AUTH_FILE.exists() else None
    )

    for url in urls:
        print("\n" + "=" * 80)
        print(url)
        print("=" * 80)

        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000)

            html = page.content()

            all_ids = []

            for pattern in PATTERNS:
                all_ids.extend(pattern.findall(html))

            all_ids = unique(all_ids)

            kaltura_blocks = page.locator(
                ".contextual-region.nc-kaltura-media.media--type-kaltura-entity"
            ).count()

            print(f"Kaltura blocks: {kaltura_blocks}")
            print(f"Entry IDs encontrados: {len(all_ids)}")

            for entry_id in all_ids:
                print(f"  - {entry_id}")

            if not all_ids:
                print("\nNo se encontró entryId en el HTML.")
                print("La siguiente versión inspeccionará también las peticiones de red.")

        except Exception as e:
            print(f"ERROR: {e}")

        finally:
            page.close()

    browser.close()
