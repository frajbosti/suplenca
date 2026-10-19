# Ločen frontend in REST API

- Status: sprejeto
- Datum: 2026-10-19

## Kontekst in problem

Aplikacijo bodo uporabljali organizator, učitelji in dijaki na računalniku in telefonu, kasneje morda še zaslon v avli šole. Ali naj strežnik sam sestavlja spletne strani ali naj bosta prikaz in logika ločena?

## Obravnavane možnosti

- ločen frontend (React) in backend z REST API
- strani, ki jih sestavi strežnik (FastAPI s predlogami Jinja)
- Django (oboje v enem ogrodju)

## Odločitev

Izbrana možnost: »ločen frontend in backend z REST API«, ker so pravila za izbiro suplenc na enem mestu v backendu, isti API pa lahko kasneje uporabi tudi zaslon v avli ali mobilna aplikacija. Takšno ločitev poznam iz projekta pri drugem predmetu.

### Posledice

- Dobro, ker se frontend in backend lahko razvijata ločeno.
- Dobro, ker je API pripravljen za kasnejše nadgradnje.
- Slabo, ker sta dva dela, ki ju je treba zaganjati in vzdrževati.
- Slabo, ker je treba urediti prijavo med njima (JWT) in dovoljenje za klice med naslovoma (CORS).