# Suplenca

Spletna aplikacija za razporejanje nadomeščanj (suplenc) odsotnih učiteljev v srednji šoli.
Organizator ob odsotnosti učitelja dobi seznam izpadlih ur in predlog primernih kandidatov
po pravilih šole, učitelji vidijo svoje suplence, dijaki pa spremembe urnika svojega oddelka.

Projekt nastaja pri predmetu Razvoj informacijskih rešitev in storitev (FERI, 2026/27).

## Tehnologije

| Del | Tehnologija |
|---|---|
| Frontend | React + Vite |
| Backend | Python, FastAPI |
| Podatkovna baza | MySQL |
| Avtentikacija | JWT, bcrypt |
| Lokalni razvoj | Docker Compose, Git + GitHub |

## Dokumentacija

- [Zasnova rešitve](docs/01-zasnova-resitve.md)
- [Funkcionalnosti in obseg](docs/02-funkcionalnosti-in-obseg.md)
- [Podatkovni model](docs/03-podatkovni-model.md)
- [Arhitektura in tehnološki sklad](docs/04-arhitektura-in-tehnoloski-sklad.md)
- [Uporabniške zgodbe](docs/05-uporabniske-zgodbe.md)
- [Wireframes](docs/06-wireframes.md)
- [Arhitekturne odločitve (ADR)](docs/adr/)

## Lokalni zagon

Potrebno: [Docker Desktop](https://www.docker.com/products/docker-desktop/) in Git.

1. Kloniraj repozitorij in se premakni v mapo projekta:
   ```
   git clone https://github.com/frajbosti/suplenca.git
   cd suplenca
   ```
2. Zaženi bazo, backend in frontend:
   ```
   docker compose up -d --build
   ```
3. Ob prvem zagonu vnesi testne uporabnike (geslo za MySQL: `test123`):
   ```
   docker compose exec baza mysql -u suplenca -p suplenca
   ```
   in v `mysql>` prilepi:
   ```sql
   INSERT INTO uporabnik (ime, priimek, email, geslo_hash, vloga, aktiven) VALUES
   ('Ana', 'Admin', 'admin@sola.si', '$2b$12$kK44OnKnxjq4N3kL1eboe.QpTVOTHAKIzl7eokHDARj0cCq8JJxVO', 'administrator', 1),
   ('Olga', 'Organizator', 'organizator@sola.si', '$2b$12$kK44OnKnxjq4N3kL1eboe.QpTVOTHAKIzl7eokHDARj0cCq8JJxVO', 'organizator', 1),
   ('Janez', 'Novak', 'novak@sola.si', '$2b$12$kK44OnKnxjq4N3kL1eboe.QpTVOTHAKIzl7eokHDARj0cCq8JJxVO', 'ucitelj', 1),
   ('Dejan', 'Dijak', 'dijak@sola.si', '$2b$12$kK44OnKnxjq4N3kL1eboe.QpTVOTHAKIzl7eokHDARj0cCq8JJxVO', 'dijak', 1),
   ('Bojan', 'Bivsi', 'bivsi@sola.si', '$2b$12$kK44OnKnxjq4N3kL1eboe.QpTVOTHAKIzl7eokHDARj0cCq8JJxVO', 'ucitelj', 0);
   exit
   ```
4. Odpri:
   - aplikacija: http://localhost:5173
   - dokumentacija API: http://localhost:8000/docs

Testni uporabniki (geslo `test123`): `admin@sola.si`, `organizator@sola.si`, `novak@sola.si`, `dijak@sola.si`, `bivsi@sola.si` (deaktiviran).

Po spremembi kode ponovno zaženi `docker compose up -d --build`. Ustavitev: `docker compose stop`.
