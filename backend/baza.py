# baza.py – povezava s podatkovno bazo MySQL prek SQLAlchemy

from sqlalchemy import create_engine   # funkcija, ki pripravi povezavo z bazo

# naslov baze: gonilnik pymysql, uporabnik:geslo, "baza" = ime storitve v docker-compose, vrata 3306, ime baze
NASLOV_BAZE = "mysql+pymysql://suplenca:test123@baza:3306/suplenca"

# objekt, prek katerega se bo backend pogovarjal z bazo
povezava = create_engine(NASLOV_BAZE)

from sqlalchemy.orm import sessionmaker, declarative_base

# Seja: z njo beremo in pišemo podatke (ena seja = en pogovor z bazo)
Seja = sessionmaker(bind=povezava)

# Osnova: iz nje izpeljemo vse tabele (modele)
Osnova = declarative_base()