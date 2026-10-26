# main.py – vstopna točka backenda (FastAPI)

import bcrypt                                  # preverjanje gesla
import jwt                                     # izdelava žetona JWT
from fastapi import FastAPI, HTTPException     # HTTPException = vrnemo napako s kodo
from pydantic import BaseModel                 # opis podatkov, ki jih pošlje frontend
from sqlalchemy import text
from baza import povezava, Seja, Osnova
from modeli import Uporabnik
from fastapi.middleware.cors import CORSMiddleware   # dovoljenje za klice iz frontenda

# ključ, s katerim backend podpiše žeton (samo backend ga pozna)
SKRIVNI_KLJUC = "suplenca-skrivni-kljuc"

aplikacija = FastAPI(title="Suplenca API")

# CORS: dovoli klice iz frontenda, ki teče na drugem naslovu (ADR 0001)
aplikacija.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # naslov frontenda
    allow_methods=["*"],                       # vse metode (GET, POST …)
    allow_headers=["*"],                       # vse glave (npr. žeton)
)

# ob zagonu ustvari tabele iz modeli.py, če še ne obstajajo
Osnova.metadata.create_all(povezava)


# preizkusni klic GET / – preveri, ali backend doseže bazo (#3)
@aplikacija.get("/")
def preveri_bazo():
    with povezava.connect() as p:
        p.execute(text("SELECT 1"))
    return {"stanje": "backend deluje, baza dosegljiva"}


# podatki, ki jih pošlje prijavni obrazec
class PodatkiPrijave(BaseModel):
    email: str
    geslo: str


# POST /prijava – preveri e-pošto in geslo ter vrne žeton (US-01)
@aplikacija.post("/prijava")
def prijava(podatki: PodatkiPrijave):
    # poišče uporabnika z vpisano e-pošto
    seja = Seja()
    uporabnik = seja.query(Uporabnik).filter(Uporabnik.email == podatki.email).first()
    seja.close()

    # uporabnik ne obstaja ali geslo ni pravilno → enako sporočilo za oba primera (US-01)
    if uporabnik is None or not bcrypt.checkpw(podatki.geslo.encode(), uporabnik.geslo_hash.encode()):
        raise HTTPException(status_code=401, detail="Napačna e-pošta ali geslo")

    # deaktiviran uporabnik se ne more prijaviti (US-01)
    if not uporabnik.aktiven:
        raise HTTPException(status_code=403, detail="Uporabnik je deaktiviran")

    # žeton vsebuje id in vlogo; frontend ga pošilja pri vsakem naslednjem klicu
    zeton = jwt.encode({"id": uporabnik.id, "vloga": uporabnik.vloga}, SKRIVNI_KLJUC, algorithm="HS256")
    return {"zeton": zeton, "vloga": uporabnik.vloga}