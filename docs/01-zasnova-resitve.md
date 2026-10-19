# 01 – Zasnova rešitve

## Ime rešitve

**Suplenca** – spletna aplikacija za razporejanje nadomeščanj (suplenc) odsotnih učiteljev v srednji šoli.

## Namen in problem

Ko je učitelj odsoten, mora organizator nadomeščanj (pomočnik ravnatelja) njegove ure pokriti. Pri tem upošteva več pravil:

- prednost ima izvedba ure za dijake – snov predmeta mora biti v letu predelana v celoti;
- najprej se išče učitelj istega predmeta, nato drug učitelj, ki vodi uro po navodilih ali v tem terminu nadoknadi svojo izpadlo uro v oddelku;
- prednost ima učitelj, ki mu je ura v tem terminu odpadla, in tisti, ki je imel ta teden manj suplenc;
- suplenca je plačana le, če je izven časa učiteljevega pouka po urniku; sicer šteje v fond ur.

Šola urnik vodi v programu Untis, pravila pa organizator upošteva na pamet. Razporejanje je zato zamudno (odsotnosti se javljajo zjutraj pred poukom), obremenitev učiteljev je neenakomerna, ni pregleda nad zaostanki pri realizaciji predmetov, obračun plačanih suplenc pa se dela ročno.

## Ciljni uporabniki

- **Organizator nadomeščanj** – vsako jutro razporedi suplence, ob koncu meseca pripravi obračun.
- **Učitelji** – javijo načrtovano odsotnost, vidijo svoje suplence in potrdijo izvedbo.
- **Dijaki** – vidijo spremembe urnika svojega oddelka.
- **Administrator** – vnese osnovne podatke in urnik ter upravlja račune.

**Primer:** učitelj programiranja ob 6.45 javi bolniško. Organizator vnese odsotnost, sistem prikaže njegovih 5 ur in za vsako predlaga najprimernejše kandidate. Organizator predloge potrdi, učitelji vidijo svoje suplence, dijaki pa spremembe urnika.

## Kratek opis delovanja

1. Administrator vnese oddelke, predmete, učitelje in urnik.
2. Organizator (ali učitelj za načrtovano odsotnost) vnese odsotnost.
3. Sistem iz urnika ugotovi izpadle ure.
4. Za vsako uro predlaga razvrščene kandidate po pravilih šole.
5. Organizator predlog potrdi ali izbere drugega kandidata.
6. Nadomeščajoči učitelj po uri potrdi izvedbo in vpiše obravnavano snov.
7. Sistem vodi realizacijo predmetov ter evidenco plačanih suplenc in ur za fond.
