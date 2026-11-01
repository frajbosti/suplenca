# main.py – vstopna točka backenda (FastAPI)

import bcrypt                                  # preverjanje gesla
import jwt                                     # izdelava žetona JWT
from fastapi import FastAPI, HTTPException, Depends            # Depends = FastAPI sam pokliče podano funkcijo
from fastapi.security import HTTPBearer                        # branje žetona "Bearer" iz glave poverilnice
from pydantic import BaseModel                 # opis podatkov, ki jih pošlje frontend
from sqlalchemy import text
from baza import povezava, Seja, Osnova
from modeli import Uporabnik, Oddelek, Predmet, UraUrnika, Odsotnost, ProstDan, Nadomescanje, OdsotnostOddelka
from fastapi.middleware.cors import CORSMiddleware   # dovoljenje za klice iz frontenda
from datetime import date, timedelta           # tip za datum; timedelta = premik za en dan


# ključ, s katerim backend podpiše žeton (samo backend ga pozna)
SKRIVNI_KLJUC = "suplenca-skrivni-kljuc"

# prebere glavo "poverilnice: Bearer <žeton>"; v /docs doda gumb Authorize
varnost = HTTPBearer()

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

# prebere žeton iz glave "poverilnice: Bearer <žeton>" in vrne njegovo vsebino (id, vloga)
def preberi_zeton(poverilnice):
    try:
        # poverilnice.credentials = sam žeton brez besede "Bearer"
        return jwt.decode(poverilnice.credentials, SKRIVNI_KLJUC, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Niste prijavljeni")

# GET /dostop/{stran} – ali sme prijavljeni uporabnik odpreti stran (US-01)
@aplikacija.get("/dostop/{stran}")
def preveri_dostop(stran: str, poverilnice=Depends(varnost)):
    uporabnik = preberi_zeton(poverilnice)
    # stran pripada vlogi z enakim imenom (npr. /organizator → organizator)
    if uporabnik["vloga"] != stran:
        raise HTTPException(status_code=403, detail="Nimate dostopa")
    return {"dostop": True}

# preveri, ali je prijavljeni uporabnik administrator – samo on ureja osnovne podatke (US-02)
def samo_administrator(poverilnice):
    uporabnik = preberi_zeton(poverilnice)
    if uporabnik["vloga"] != "administrator":
        raise HTTPException(status_code=403, detail="Nimate dostopa")


# ---------- ODDELKI (US-02) ----------

class PodatkiOddelka(BaseModel):
    oznaka: str


# GET /oddelki – seznam vseh oddelkov
@aplikacija.get("/oddelki")
def seznam_oddelkov(poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    oddelki = seja.query(Oddelek).all()
    seja.close()
    # vsak oddelek pretvorimo v slovar, ki ga FastAPI vrne kot JSON
    return [{"id": o.id, "oznaka": o.oznaka} for o in oddelki]


# POST /oddelki – doda nov oddelek
@aplikacija.post("/oddelki")
def dodaj_oddelek(podatki: PodatkiOddelka, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    seja.add(Oddelek(oznaka=podatki.oznaka))
    seja.commit()                      # shrani spremembo v bazo
    seja.close()
    return {"sporocilo": "Oddelek dodan"}


# PUT /oddelki/{id} – uredi obstoječi oddelek
@aplikacija.put("/oddelki/{id}")
def uredi_oddelek(id: int, podatki: PodatkiOddelka, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    oddelek = seja.get(Oddelek, id)    # poišče vrstico po id
    oddelek.oznaka = podatki.oznaka
    seja.commit()
    seja.close()
    return {"sporocilo": "Oddelek urejen"}


# DELETE /oddelki/{id} – izbriše oddelek
@aplikacija.delete("/oddelki/{id}")
def izbrisi_oddelek(id: int, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    seja.delete(seja.get(Oddelek, id))
    seja.commit()
    seja.close()
    return {"sporocilo": "Oddelek izbrisan"}


# ---------- PREDMETI (US-02) ----------

class PodatkiPredmeta(BaseModel):
    kratica: str
    naziv: str


@aplikacija.get("/predmeti")
def seznam_predmetov(poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    predmeti = seja.query(Predmet).all()
    seja.close()
    return [{"id": p.id, "kratica": p.kratica, "naziv": p.naziv} for p in predmeti]


@aplikacija.post("/predmeti")
def dodaj_predmet(podatki: PodatkiPredmeta, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    seja.add(Predmet(kratica=podatki.kratica, naziv=podatki.naziv))
    seja.commit()
    seja.close()
    return {"sporocilo": "Predmet dodan"}


@aplikacija.put("/predmeti/{id}")
def uredi_predmet(id: int, podatki: PodatkiPredmeta, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    predmet = seja.get(Predmet, id)
    predmet.kratica = podatki.kratica
    predmet.naziv = podatki.naziv
    seja.commit()
    seja.close()
    return {"sporocilo": "Predmet urejen"}


@aplikacija.delete("/predmeti/{id}")
def izbrisi_predmet(id: int, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    seja.delete(seja.get(Predmet, id))
    seja.commit()
    seja.close()
    return {"sporocilo": "Predmet izbrisan"}


# ---------- UČITELJI (US-02) – uporabniki z vlogo "ucitelj" ----------

class PodatkiUcitelja(BaseModel):
    ime: str
    priimek: str
    email: str
    geslo: str = ""                    # obvezno pri dodajanju; pri urejanju prazno = geslo ostane


@aplikacija.get("/ucitelji")
def seznam_uciteljev(poverilnice=Depends(varnost)):
    uporabnik = preberi_zeton(poverilnice)
    # seznam učiteljev potrebujeta administrator (US-02) in organizator (US-03)
    if uporabnik["vloga"] not in ["administrator", "organizator"]:
        raise HTTPException(status_code=403, detail="Nimate dostopa")
    seja = Seja()
    ucitelji = seja.query(Uporabnik).filter(Uporabnik.vloga == "ucitelj").all()
    seja.close()
    return [{"id": u.id, "ime": u.ime, "priimek": u.priimek, "email": u.email} for u in ucitelji]


@aplikacija.post("/ucitelji")
def dodaj_ucitelja(podatki: PodatkiUcitelja, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    # geslo shranimo kot bcrypt zgoščeno vrednost, nikoli v čistem besedilu
    geslo_hash = bcrypt.hashpw(podatki.geslo.encode(), bcrypt.gensalt()).decode()
    seja = Seja()
    seja.add(Uporabnik(ime=podatki.ime, priimek=podatki.priimek, email=podatki.email,
                       geslo_hash=geslo_hash, vloga="ucitelj", aktiven=True))
    seja.commit()
    seja.close()
    return {"sporocilo": "Učitelj dodan"}


@aplikacija.put("/ucitelji/{id}")
def uredi_ucitelja(id: int, podatki: PodatkiUcitelja, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    ucitelj = seja.get(Uporabnik, id)
    ucitelj.ime = podatki.ime
    ucitelj.priimek = podatki.priimek
    ucitelj.email = podatki.email
    seja.commit()
    seja.close()
    return {"sporocilo": "Učitelj urejen"}


@aplikacija.delete("/ucitelji/{id}")
def izbrisi_ucitelja(id: int, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    seja.delete(seja.get(Uporabnik, id))
    seja.commit()
    seja.close()
    return {"sporocilo": "Učitelj izbrisan"}

# ---------- URNIK (US-02) ----------

# vsa polja razen učilnice so obvezna – če kakšno manjka, FastAPI sam vrne napako 422 (US-02)
class PodatkiUre(BaseModel):
    oddelek_id: int
    predmet_id: int
    ucitelj_id: int
    dan_v_tednu: int
    solska_ura: int
    ucilnica: str = ""


# POST /urnik – doda uro v urnik, če učitelj in oddelek ob tem času še nimata pouka
@aplikacija.post("/urnik")
def dodaj_uro(podatki: PodatkiUre, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()

    # ali ima učitelj ob istem dnevu in uri že drugo uro (US-02)
    ucitelj_zaseden = seja.query(UraUrnika).filter(
        UraUrnika.ucitelj_id == podatki.ucitelj_id,
        UraUrnika.dan_v_tednu == podatki.dan_v_tednu,
        UraUrnika.solska_ura == podatki.solska_ura,
    ).first()

    # ali ima oddelek ob istem dnevu in uri že drugo uro (US-02)
    oddelek_zaseden = seja.query(UraUrnika).filter(
        UraUrnika.oddelek_id == podatki.oddelek_id,
        UraUrnika.dan_v_tednu == podatki.dan_v_tednu,
        UraUrnika.solska_ura == podatki.solska_ura,
    ).first()

    if ucitelj_zaseden is not None:
        seja.close()
        raise HTTPException(status_code=400, detail="Učitelj ima ob tem času že pouk – ure ni mogoče shraniti")
    if oddelek_zaseden is not None:
        seja.close()
        raise HTTPException(status_code=400, detail="Oddelek ima ob tem času že drugo uro – ure ni mogoče shraniti")

    # termin je prost → shrani uro
    seja.add(UraUrnika(
        oddelek_id=podatki.oddelek_id,
        predmet_id=podatki.predmet_id,
        ucitelj_id=podatki.ucitelj_id,
        dan_v_tednu=podatki.dan_v_tednu,
        solska_ura=podatki.solska_ura,
        ucilnica=podatki.ucilnica,
    ))
    seja.commit()
    seja.close()
    return {"sporocilo": "Ura dodana"}



# GET /urnik/{oddelek_id} – vse ure izbranega oddelka za tedensko tabelo (US-02, WF-02)
@aplikacija.get("/urnik/{oddelek_id}")
def urnik_oddelka(oddelek_id: int, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    ure = seja.query(UraUrnika).filter(UraUrnika.oddelek_id == oddelek_id).all()

    # namesto številk (id) vrnemo ime predmeta in priimek učitelja, kot na WF-02 ("Matematika · Zupan")
    rezultat = []
    for ura in ure:
        predmet = seja.get(Predmet, ura.predmet_id)
        ucitelj = seja.get(Uporabnik, ura.ucitelj_id)
        rezultat.append({
            "dan_v_tednu": ura.dan_v_tednu,
            "solska_ura": ura.solska_ura,
            "predmet": predmet.naziv,
            "ucitelj": ucitelj.priimek,
        })
    seja.close()
    return rezultat

# GET /urnik/{oddelek_id} – vse ure izbranega oddelka za tedensko tabelo (US-02, WF-02)
@aplikacija.get("/urnik/{oddelek_id}")
def urnik_oddelka(oddelek_id: int, poverilnice=Depends(varnost)):
    samo_administrator(poverilnice)
    seja = Seja()
    ure = seja.query(UraUrnika).filter(UraUrnika.oddelek_id == oddelek_id).all()

    # namesto številk (id) vrnemo ime predmeta in priimek učitelja, kot na WF-02 ("Matematika · Zupan")
    rezultat = []
    for ura in ure:
        predmet = seja.get(Predmet, ura.predmet_id)
        ucitelj = seja.get(Uporabnik, ura.ucitelj_id)
        rezultat.append({
            "dan_v_tednu": ura.dan_v_tednu,
            "solska_ura": ura.solska_ura,
            "predmet": predmet.naziv,
            "ucitelj": ucitelj.priimek,
        })
    seja.close()
    return rezultat

# ---------- ODSOTNOSTI (US-03) ----------

# preveri, ali je prijavljeni uporabnik organizator nadomeščanj
def samo_organizator(poverilnice):
    uporabnik = preberi_zeton(poverilnice)
    if uporabnik["vloga"] != "organizator":
        raise HTTPException(status_code=403, detail="Nimate dostopa")


# učitelj, od, do in razlog so obvezni (US-03); navodila niso
class PodatkiOdsotnosti(BaseModel):
    ucitelj_id: int
    datum_od: date
    datum_do: date
    razlog: str
    navodila: str = ""


# POST /odsotnosti – shrani odsotnost in iz urnika ustvari izpadle ure (US-03)
@aplikacija.post("/odsotnosti")
def dodaj_odsotnost(podatki: PodatkiOdsotnosti, poverilnice=Depends(varnost)):
    samo_organizator(poverilnice)
    seja = Seja()

    # dve obdobji se prekrivata, če se prvo začne pred koncem drugega in konča po začetku drugega
    prekrivanje = seja.query(Odsotnost).filter(
        Odsotnost.ucitelj_id == podatki.ucitelj_id,
        Odsotnost.datum_od <= podatki.datum_do,
        Odsotnost.datum_do >= podatki.datum_od,
    ).first()

    if prekrivanje is not None:
        seja.close()
        raise HTTPException(status_code=400, detail="Učitelj ima v tem obdobju že vneseno odsotnost – odsotnost ni shranjena")

    odsotnost = Odsotnost(
        ucitelj_id=podatki.ucitelj_id,
        datum_od=podatki.datum_od,
        datum_do=podatki.datum_do,
        razlog=podatki.razlog,
        navodila=podatki.navodila,
    )
    seja.add(odsotnost)
    seja.commit()                              # po shranjevanju dobi odsotnost svoj id

    # seznam dni brez pouka (US-03)
    prosti_dnevi = [p.datum for p in seja.query(ProstDan).all()]

    # gre čez vse dni od – do in za vsak dan poišče ure učitelja v urniku
    izpadle = []
    datum = podatki.datum_od
    while datum <= podatki.datum_do:
        if datum not in prosti_dnevi:
            # weekday(): ponedeljek = 0, zato +1, da se ujema z dan_v_tednu v urniku (ponedeljek = 1)
            ure = seja.query(UraUrnika).filter(
                UraUrnika.ucitelj_id == podatki.ucitelj_id,
                UraUrnika.dan_v_tednu == datum.weekday() + 1,
            ).order_by(UraUrnika.solska_ura).all()

            for ura in ure:
                # vsaka izpadla ura postane nadomeščanje s statusom "nepokrita"
                seja.add(Nadomescanje(odsotnost_id=odsotnost.id, ura_urnika_id=ura.id, datum=datum, status="nepokrita"))
                # podatki za prikaz po WF-03
                izpadle.append({
                    "datum": datum,
                    "solska_ura": ura.solska_ura,
                    "oddelek": seja.get(Oddelek, ura.oddelek_id).oznaka,
                    "predmet": seja.get(Predmet, ura.predmet_id).naziv,
                    "ucilnica": ura.ucilnica,
                    "status": "nepokrita",
                })
        datum = datum + timedelta(days=1)      # naslednji dan

    seja.commit()
    seja.close()
    return {"sporocilo": "Odsotnost shranjena", "izpadle_ure": izpadle}

# ---------- DNEVNI PREGLED IN PREDLOG KANDIDATOV (US-04, WF-04) ----------

# GET /dnevni-pregled/{datum} – vse izpadle ure izbranega dne
@aplikacija.get("/dnevni-pregled/{datum}")
def dnevni_pregled(datum: date, poverilnice=Depends(varnost)):
    samo_organizator(poverilnice)
    seja = Seja()
    nadomescanja = seja.query(Nadomescanje).filter(Nadomescanje.datum == datum).all()

    rezultat = []
    for n in nadomescanja:
        ura = seja.get(UraUrnika, n.ura_urnika_id)
        odsotni = seja.get(Uporabnik, ura.ucitelj_id)
        # nadomeščajoči je prazen, dokler ura ni pokrita
        nadomesca = seja.get(Uporabnik, n.nadomescajoci_id).priimek if n.nadomescajoci_id else "–"
        rezultat.append({
            "id": n.id,
            "solska_ura": ura.solska_ura,
            "oddelek": seja.get(Oddelek, ura.oddelek_id).oznaka,
            "predmet": seja.get(Predmet, ura.predmet_id).naziv,
            "odsoten": odsotni.priimek,
            "nadomesca": nadomesca,
            "status": n.status,
        })
    seja.close()
    # urejeno po šolski uri
    rezultat.sort(key=lambda r: r["solska_ura"])
    return rezultat


# GET /kandidati/{nadomescanje_id} – razvrščen seznam primernih učiteljev za izpadlo uro (US-04)
@aplikacija.get("/kandidati/{nadomescanje_id}")
def predlog_kandidatov(nadomescanje_id: int, poverilnice=Depends(varnost)):
    samo_organizator(poverilnice)
    seja = Seja()

    n = seja.get(Nadomescanje, nadomescanje_id)
    izpadla = seja.get(UraUrnika, n.ura_urnika_id)
    dan = izpadla.dan_v_tednu
    solska_ura = izpadla.solska_ura

    # oddelki, ki so ta dan odsotni – njihovim učiteljem ura odpade
    odsotni_oddelki = [o.oddelek_id for o in seja.query(OdsotnostOddelka).filter(OdsotnostOddelka.datum == n.datum).all()]

    # tekoči teden: od ponedeljka do nedelje okoli datuma izpadle ure
    ponedeljek = n.datum - timedelta(days=n.datum.weekday())
    nedelja = ponedeljek + timedelta(days=6)

    kandidati = []
    for u in seja.query(Uporabnik).filter(Uporabnik.vloga == "ucitelj", Uporabnik.aktiven == True).all():

        # 1. odsoten učitelj ne more nadomeščati (US-04)
        odsoten = seja.query(Odsotnost).filter(
            Odsotnost.ucitelj_id == u.id,
            Odsotnost.datum_od <= n.datum,
            Odsotnost.datum_do >= n.datum,
        ).first()
        if odsoten is not None:
            continue

        # 2. učitelj s poukom ob tej uri ni prost – razen če je njegov oddelek odsoten (ura mu je odpadla)
        pouk = seja.query(UraUrnika).filter(
            UraUrnika.ucitelj_id == u.id,
            UraUrnika.dan_v_tednu == dan,
            UraUrnika.solska_ura == solska_ura,
        ).first()
        ura_odpadla = pouk is not None and pouk.oddelek_id in odsotni_oddelki
        if pouk is not None and not ura_odpadla:
            continue

        # vrsta: isti predmet, če ga učitelj po urniku kjerkoli poučuje
        isti_predmet = seja.query(UraUrnika).filter(
            UraUrnika.ucitelj_id == u.id,
            UraUrnika.predmet_id == izpadla.predmet_id,
        ).first() is not None

        # plačljivost: plačana, če je ura pred prvo ali po zadnji uri učitelja ta dan (dokument 01)
        ure_dneva = [x.solska_ura for x in seja.query(UraUrnika).filter(
            UraUrnika.ucitelj_id == u.id,
            UraUrnika.dan_v_tednu == dan,
        ).all()]
        placana = len(ure_dneva) == 0 or solska_ura < min(ure_dneva) or solska_ura > max(ure_dneva)

        # število potrjenih suplenc v tekočem tednu
        suplenc = seja.query(Nadomescanje).filter(
            Nadomescanje.nadomescajoci_id == u.id,
            Nadomescanje.status == "potrjena",
            Nadomescanje.datum >= ponedeljek,
            Nadomescanje.datum <= nedelja,
        ).count()

        kandidati.append({
            "id": u.id,
            "ucitelj": u.priimek + " " + u.ime,
            "isti_predmet": isti_predmet,
            "ura_odpadla": ura_odpadla,
            "vrsta": "strokovno" if isti_predmet else "po navodilih",
            "placana": placana,
            "suplenc_ta_teden": suplenc,
        })

    seja.close()

    # razvrstitev (US-04): najprej isti predmet, nato ura odpadla, nato manj suplenc
    # (False se razvrsti pred True, zato "not")
    kandidati.sort(key=lambda k: (not k["isti_predmet"], not k["ura_odpadla"], k["suplenc_ta_teden"]))
    return kandidati

# PUT /nadomescanja/{id}/odpade – organizator označi, da izpadla ura odpade (US-04)
@aplikacija.put("/nadomescanja/{id}/odpade")
def ura_odpade(id: int, poverilnice=Depends(varnost)):
    samo_organizator(poverilnice)
    seja = Seja()
    n = seja.get(Nadomescanje, id)
    n.status = "odpadla"
    seja.commit()
    seja.close()
    return {"sporocilo": "Ura odpade"}