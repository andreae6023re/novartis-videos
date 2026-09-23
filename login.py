from pathlib import Path
from playwright.sync_api import sync_playwright

AUTH_DIR = Path("auth")
AUTH_DIR.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(
        "https://www.pro.novartis.com/es-es/",
        wait_until="domcontentloaded"
    )

    print("\n========================================")
    print("INICIA SESIÓN EN NOVARTIS")
    print("Cuando hayas terminado, vuelve aquí.")
    print("========================================\n")

    input("Pulsa ENTER cuando hayas iniciado sesión... ")

    context.storage_state(path=AUTH_DIR / "session.json")
    print("\nSesión guardada en auth/session.json")

    browser.close()
