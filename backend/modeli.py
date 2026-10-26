# Tabele v bazi, opisane kot Python razredi (SQLAlchemy)

from sqlalchemy import Column, Integer, String, Boolean
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