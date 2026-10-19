# MySQL za podatkovno bazo

- Status: sprejeto
- Datum: 2026-10-19

## Kontekst in problem

Aplikacija hrani uporabnike, urnik, odsotnosti in nadomeščanja. Podatki so tesno povezani: vsako nadomeščanje kaže na uro urnika, odsotnost in učitelja. Katero podatkovno bazo uporabiti?

## Obravnavane možnosti

- MySQL
- PostgreSQL
- MongoDB
- SQLite

## Odločitev

Izbrana možnost: »MySQL«, ker so podatki relacijski in potrebujejo tuje ključe in transakcije, MySQL pa je razširjen, brezplačen in ga pozna večina razvijalcev. MySQL in MariaDB uporabljam tudi pri poučevanju SQL.

### Posledice

- Dobro, ker baza sama prepreči napačne povezave (npr. nadomeščanje za neobstoječo uro).
- Dobro, ker deluje tudi z MariaDB.
- Slabo, ker nima nekaterih naprednih funkcij PostgreSQL, zato del preverjanja (npr. dve suplenci ob isti uri) naredi backend.