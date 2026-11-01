# Tabele v bazi, opisane kot Python razredi (SQLAlchemy)

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from baza import Osnova



# tabela uporabnik (dokument 03) + polje aktiven za deaktivacijo (US-01)
class Uporabnik(Osnova):
    __tablename__ = "uporabnik"

    id = Column(Integer, primary_key=True)        # samodejna številka
    ime = Column(String(50))
    priimek = Column(String(50))
    email = Column(String(100), unique=True)      # e-pošta se ne sme ponoviti
    geslo_hash = Column(String(100))              # ne geslo, ampak njegova bcrypt zgoščena vrednost
    vloga = Column(String(20))                    # administrator, organizator, ucitelj, dijak
    aktiven = Column(Boolean, default=True)       # False = se ne more prijaviti

    # tabela oddelek (dokument 03), npr. "3. b"
class Oddelek(Osnova):
    __tablename__ = "oddelek"

    id = Column(Integer, primary_key=True)
    oznaka = Column(String(10), unique=True)      # oznaka se ne sme ponoviti


# tabela predmet (dokument 03), npr. "PRO" – Programiranje
class Predmet(Osnova):
    __tablename__ = "predmet"

    id = Column(Integer, primary_key=True)
    kratica = Column(String(10), unique=True)
    naziv = Column(String(100))

# tabela ura_urnika (dokument 03) – ena vrstica = ena ura v tedenskem urniku oddelka
class UraUrnika(Osnova):
    __tablename__ = "ura_urnika"

    id = Column(Integer, primary_key=True)
    oddelek_id = Column(Integer, ForeignKey("oddelek.id"))     # tuji ključ: ura mora pripadati obstoječemu oddelku
    predmet_id = Column(Integer, ForeignKey("predmet.id"))
    ucitelj_id = Column(Integer, ForeignKey("uporabnik.id"))   # učitelj je uporabnik z vlogo ucitelj
    dan_v_tednu = Column(Integer)                              # 1 = ponedeljek … 5 = petek
    solska_ura = Column(Integer)                               # 1. … 8. šolska ura
    ucilnica = Column(String(10))                              # npr. R12 (WF-03, US-06)

    # tabela odsotnost (dokument 03) – ena vrstica = ena odsotnost učitelja v obdobju od – do
class Odsotnost(Osnova):
    __tablename__ = "odsotnost"

    id = Column(Integer, primary_key=True)
    ucitelj_id = Column(Integer, ForeignKey("uporabnik.id"))
    datum_od = Column(Date)                   # "od" in "do" sta v MySQL rezervirani besedi
    datum_do = Column(Date)
    razlog = Column(String(50))               # npr. Bolniška (WF-03)
    navodila = Column(String(500))            # navodila za nadomeščajočega učitelja (US-06)

    # tabela prost_dan – dnevi brez pouka (prazniki, počitnice); zanje se izpadle ure ne ustvarijo (US-03)
class ProstDan(Osnova):
    __tablename__ = "prost_dan"

    id = Column(Integer, primary_key=True)
    datum = Column(Date, unique=True)
    opis = Column(String(100))                 # npr. Božič


# tabela nadomescanje (dokument 03) – ena vrstica = ena izpadla ura na določen datum in njena rešitev
class Nadomescanje(Osnova):
    __tablename__ = "nadomescanje"

    id = Column(Integer, primary_key=True)
    odsotnost_id = Column(Integer, ForeignKey("odsotnost.id"))
    ura_urnika_id = Column(Integer, ForeignKey("ura_urnika.id"))
    datum = Column(Date)
    nadomescajoci_id = Column(Integer, ForeignKey("uporabnik.id"))   # prazno, dokler ura ni pokrita (US-05)
    vrsta = Column(String(30))                 # strokovno / po navodilih (US-04)
    placana = Column(Boolean)                  # plačana ali fond ur (US-05)
    status = Column(String(20))                # nepokrita, potrjena, odpadla

# tabela odsotnost_oddelka – oddelek ta dan nima pouka (ekskurzija, športni dan);
# njegovim učiteljem ura odpade in imajo prednost pri suplenci (US-04)
class OdsotnostOddelka(Osnova):
    __tablename__ = "odsotnost_oddelka"

    id = Column(Integer, primary_key=True)
    oddelek_id = Column(Integer, ForeignKey("oddelek.id"))
    datum = Column(Date)
    razlog = Column(String(100))               # npr. Ekskurzija

    