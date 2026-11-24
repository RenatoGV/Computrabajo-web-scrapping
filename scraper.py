import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = "https://pe.computrabajo.com/trabajo-de-software"

HEADERS = {
   "User-Agent": (
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36"
   ),
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
   "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
   "Referer": "https://pe.computrabajo.com/"
}

session = requests.Session()
response = requests.get(URL, headers=HEADERS, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
ofertas = []

for box in soup.select("article.box_offer, .box_offer"):
   titulo = box.select_one(".fs18.fwB.prB, h2 a, a.js-o-link")

   empresa_box = box.select_one("p.dFlex.vm_fx.fs16.fc_base.mt5")
   if empresa_box:
      empresa_link = empresa_box.select_one("a.fc_base.t_ellipsis, a")
      empresa = (
         empresa_link.get_text(" ", strip=True)
         if empresa_link
         else empresa_box.get_text(" ", strip=True)
      )
   else:
      empresa = ""

   ubicacion = box.select_one(".fs16.fc_base.mt5:not(.dFlex) span.mr10, p.fs16.fc_base.mt5:not(.dFlex)")

   link_tag = None
   if titulo:
      link_tag = titulo if titulo.name == "a" else titulo.select_one("a")

   enlace = link_tag.get("href", "") if link_tag else ""

   ofertas.append({
      "puesto": titulo.get_text(" ", strip=True) if titulo else "",
      "empresa": empresa,
      "ubicacion": ubicacion.get_text(" ", strip=True) if ubicacion else "",
      "url": urljoin(URL, enlace) if enlace else ""
   })

with open("data/ofertas.json", "w", encoding="utf-8") as file:
   json.dump(ofertas, file, ensure_ascii=False, indent=3)

print(f"Se guardaron {len(ofertas)} ofertas.")