# main.py – vstopna točka backenda (FastAPI)

from fastapi import FastAPI        # ogrodje za REST API
from sqlalchemy import text        # text() omogoča izvedbo navadnega SQL ukaza
from baza import povezava          # povezava z bazo iz baza.py

# ustvari aplikacijo; samodejna dokumentacija bo na /docs (ADR 0002)
aplikacija = FastAPI(title="Suplenca API")


# preizkusni klic GET / – preveri, ali backend doseže bazo
@aplikacija.get("/")
def preveri_bazo():
    # odpre povezavo, izvede najpreprostejši SQL in povezavo ob koncu zapre (with)
    with povezava.connect() as p:
        p.execute(text("SELECT 1"))
    # FastAPI slovar samodejno pretvori v JSON
    return {"stanje": "backend deluje, baza dosegljiva"}