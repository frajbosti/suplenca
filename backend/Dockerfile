# Dockerfile – navodila, kako Docker zgradi sliko backenda

# osnovna slika z že nameščenim Pythonom
FROM python:3.13-slim

# delovna mapa znotraj kontejnerja
WORKDIR /app

# najprej kopira samo seznam knjižnic in jih namesti
COPY requirements.txt .
RUN pip install -r requirements.txt

# nato kopira še vso kodo backenda
COPY . .

# ob zagonu kontejnerja zažene strežnik uvicorn: datoteka main, objekt aplikacija, vrata 8000
CMD ["uvicorn", "main:aplikacija", "--host", "0.0.0.0", "--port", "8000"]