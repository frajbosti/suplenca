# baza.py – povezava s podatkovno bazo MySQL prek SQLAlchemy

from sqlalchemy import create_engine   # funkcija, ki pripravi povezavo z bazo

# naslov baze: gonilnik pymysql, uporabnik:geslo, "baza" = ime storitve v docker-compose, vrata 3306, ime baze
NASLOV_BAZE = "mysql+pymysql://suplenca:test123@baza:3306/suplenca"

# objekt, prek katerega se bo backend pogovarjal z bazo
povezava = create_engine(NASLOV_BAZE)