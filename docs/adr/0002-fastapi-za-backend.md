# FastAPI za backend

- Status: sprejeto
- Datum: 2026-10-19

## Kontekst in problem

Backend mora ponuditi REST API za frontend in izvajati pravila za izbiro suplenc. Projekt bo med semestrom prevzel drug razvijalec. V katerem ogrodju napisati backend?

## Obravnavane možnosti

- FastAPI (Python)
- Flask (Python)
- ASP.NET Core (C#)

## Odločitev

Izbrana možnost: »FastAPI«, ker je narejen posebej za API, sam preverja vhodne podatke in sam ustvari dokumentacijo API-ja (stran /docs), kjer prevzemnik vidi in preizkusi vse klice. Python že uporabljam tudi pri drugih predmetih.

### Posledice

- Dobro, ker je manj kode za preverjanje podatkov.
- Dobro, ker samodejna dokumentacija olajša prevzem projekta.
- Slabo, ker nima vgrajene prijave, zato jo z JWT uredim sam.