from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import os

app = FastAPI()

# Le dossier à l'intérieur du conteneur qui sera lié à votre ordi
DATA_DIR = "/app/shared_data"

@app.post("/convert")
async def convert_html_to_pdf(filename: str):
    html_path = os.path.join(DATA_DIR, filename)
    pdf_path = html_path.replace(".html", ".pdf")

    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Fichier HTML introuvable")

    async with async_playwright() as p:
        # Lancement de Chromium en mode headless (sans interface)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # On ouvre le fichier HTML local
        await page.goto(f"file://{html_path}")

        # Génération du PDF
        await page.pdf(path=pdf_path, format="A4", print_background=True, margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"})
        await browser.close()

    return {"status": "success", "message": f"PDF généré : {pdf_path}"}
