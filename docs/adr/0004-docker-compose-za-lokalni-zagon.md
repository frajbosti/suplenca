# Docker Compose za lokalni zagon

- Status: sprejeto
- Datum: 2026-10-19

## Kontekst in problem

Projekt ima tri dele (frontend, backend, MySQL), ki morajo teči hkrati. Med semestrom ga bo prevzel drug razvijalec.

## Obravnavane možnosti

- Docker Compose
- ročna namestitev na računalnik
- posamezni Docker ukazi (docker run)

## Odločitev

Izbrana možnost: »Docker Compose«, ker so vsi trije deli opisani v eni datoteki in se zaženejo z enim ukazom (docker compose up), vsak razvijalec pa ima enake različice MySQL, Pythona in Node.js. Docker Compose uporabljam tudi pri drugem predmetu.

### Posledice

- Dobro, ker prevzemnik zažene projekt z enim ukazom.
- Dobro, ker ni razlik med računalniki (»pri meni deluje, pri tebi ne«).
- Slabo, ker je potreben Docker Desktop, ki porabi nekaj pomnilnika.