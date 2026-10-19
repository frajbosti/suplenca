# 05 – Uporabniške zgodbe

Vsaka zgodba je zapisana v obliki: *Kot [vloga] želim [dejanje], da [razlog].*
Za vsako so navedeni pogoji sprejemljivosti (*acceptance criteria*), torej preverljivi pogoji, kdaj je zgodba izpolnjena.
Zgodbe sledijo kriterijem **INVEST**: neodvisna (*Independent*), dogovorljiva (*Negotiable*), koristna (*Valuable*), ocenljiva (*Estimable*), majhna (*Small*) in preverljiva (*Testable*).

Oznaka **MVP** (*Minimum Viable Product*, prva delujoča različica) pomeni, da zgodba spada v prvo različico.

---

### US-01 – Prijava in dostop glede na vlogo (F1, MVP)
**Vloga:** vsi uporabniki
**Zgodba:** Kot uporabnik želim, da se prijavim z e-pošto in geslom, da vidim samo strani in podatke, ki pripadajo moji vlogi.

**Pogoji sprejemljivosti:**
- Ob pravilni e-pošti in geslu je uporabnik preusmerjen na začetno stran svoje vloge.
- Ob napačnih podatkih se prikaže sporočilo »Napačna e-pošta ali geslo«, uporabnik ostane na prijavni strani.
- Deaktiviran uporabnik se ne more prijaviti.
- Če uporabnik odpre stran, ki ni namenjena njegovi vlogi, sistem prikaže »Nimate dostopa«.

### US-02 – Vnos urnika (F2, MVP)
**Vloga:** administrator
**Zgodba:** Kot administrator želim vnesti oddelke, predmete, učitelje in urnik, da lahko sistem ugotovi, katere ure izpadejo ob odsotnosti.

**Pogoji sprejemljivosti:**
- Administrator lahko doda, uredi in izbriše oddelek, predmet in učitelja.
- Vnos ure urnika zahteva oddelek, predmet, učitelja, dan v tednu in šolsko uro.
- Sistem zavrne vnos, če ima učitelj ali oddelek ob istem dnevu in uri že drugo uro.
- Urnik oddelka je prikazan kot tedenska tabela (dnevi × šolske ure).

### US-03 – Vnos odsotnosti in izpadle ure (F3, MVP)
**Vloga:** organizator nadomeščanj
**Zgodba:** Kot organizator želim vnesti odsotnost učitelja, da sistem sam ugotovi vse njegove izpadle ure.

**Pogoji sprejemljivosti:**
- Vnos zahteva učitelja, datum ali obdobje (od – do) in razlog.
- Po shranjevanju sistem prikaže seznam vseh ur odsotnega učitelja v tem obdobju (datum, ura, oddelek, predmet) s statusom »nepokrita«.
- Za dneve brez pouka (prazniki, počitnice) sistem izpadlih ur ne ustvari.
- Če se odsotnost prekriva z že vneseno odsotnostjo istega učitelja, sistem opozori in je ne shrani.

### US-04 – Predlog kandidatov (F4, MVP)
**Vloga:** organizator nadomeščanj
**Zgodba:** Kot organizator želim za izpadlo uro dobiti razvrščen seznam primernih učiteljev, da hitro izberem najboljšo rešitev.

**Pogoji sprejemljivosti:**
- Seznam vsebuje le učitelje, ki ob tej uri nimajo pouka in niso odsotni ali nerazpoložljivi.
- Učitelji istega predmeta so na vrhu seznama.
- Pri enakem predmetu ima prednost učitelj, ki mu je ura odpadla, nato tisti z manj suplencami v tekočem tednu.
- Pri vsakem kandidatu je prikazana vrsta suplence, ali bo plačana in število suplenc v tem tednu.
- Če ni nobenega kandidata, se prikaže »Ni prostega učitelja« z možnostjo »Ura odpade«.

### US-05 – Potrditev suplence (F5, MVP)
**Vloga:** organizator nadomeščanj
**Zgodba:** Kot organizator želim potrditi izbranega kandidata, da je suplenca dodeljena in pravilno označena za obračun.

**Pogoji sprejemljivosti:**
- Po potrditvi se status ure spremeni v »potrjena«, ura je dodeljena izbranemu učitelju.
- Sistem označi suplenco kot plačano, če je pred prvo ali po zadnji uri učitelja ta dan; sicer kot uro za fond.
- Učitelju ni mogoče dodeliti dveh suplenc ob isti uri.
- Potrjena suplenca se takoj prikaže na strani učitelja in oddelka.

### US-06 – Moje suplence (F6, MVP)
**Vloga:** učitelj
**Zgodba:** Kot učitelj želim videti svoje suplence za danes in naslednje dni, da vem, kdaj in kje moram nadomeščati.

**Pogoji sprejemljivosti:**
- Seznam prikazuje datum, šolsko uro, oddelek, predmet, učilnico in vrsto suplence.
- Prikazane so samo suplence prijavljenega učitelja, urejene po datumu in uri.
- Pri vsaki suplenci so vidna navodila odsotnega učitelja, če obstajajo.
- Če suplenc ni, se prikaže »Ta teden nimate suplenc«.

### US-07 – Spremembe urnika oddelka (F6, MVP)
**Vloga:** dijak
**Zgodba:** Kot dijak želim videti spremembe urnika svojega oddelka, da vem, kdo bo imel uro in ali ura odpade.

**Pogoji sprejemljivosti:**
- Dijak vidi spremembe samo za svoj oddelek, za danes in jutri.
- Pri vsaki spremembi so prikazani šolska ura, predmet, nadomeščajoči učitelj ali oznaka »odpade«.
- Razlog odsotnosti učitelja ni prikazan.
- Če sprememb ni, se prikaže »Danes ni sprememb urnika«.

### US-08 – Potrditev izvedbe (F7)
**Vloga:** učitelj
**Zgodba:** Kot učitelj želim po suplenci potrditi izvedbo in vpisati obravnavano snov, da se ura šteje v realizacijo predmeta.

**Pogoji sprejemljivosti:**
- Izvedbo je mogoče potrditi šele po začetku ure.
- Polje »obravnavana snov« je obvezno.
- Po potrditvi se status spremeni v »izvedena« in ure ni več mogoče urejati.

### US-09 – Nerazpoložljivost vnaprej (F8)
**Vloga:** učitelj
**Zgodba:** Kot učitelj želim vnaprej javiti termin, ko ne morem nadomeščati, da me sistem takrat ne predlaga.

**Pogoji sprejemljivosti:**
- Vnos zahteva datum, šolske ure in razlog.
- Datum mora biti vsaj 2 dni po dnevu vnosa, sicer sistem vnos zavrne.
- Nerazpoložljivost začne veljati, ko jo organizator odobri.
- Odobrena nerazpoložljivost izloči učitelja iz predlogov za te ure.

### US-10 – Odklonitev suplence (F9)
**Vloga:** učitelj
**Zgodba:** Kot učitelj želim odkloniti dodeljeno suplenco z utemeljitvijo, da organizator pravočasno najde drugo rešitev.

**Pogoji sprejemljivosti:**
- Odklonitev zahteva vpis razloga.
- Status suplence se spremeni v »odklonjena«, organizator jo vidi na svojem pregledu.
- Ko organizator odklonitev odobri, se ura vrne med nepokrite in sistem pripravi nov predlog brez tega učitelja.
- Če organizator odklonitev zavrne, suplenca ostane dodeljena učitelju.

### US-11 – Realizacija ur (F10)
**Vloga:** organizator nadomeščanj
**Zgodba:** Kot organizator želim videti realizacijo ur po oddelkih in predmetih, da pravočasno opazim predmete, ki zaostajajo.

**Pogoji sprejemljivosti:**
- Za vsak predmet v oddelku so prikazane načrtovane ure, izvedene ure in odstotek realizacije.
- Ura, ki jo drug učitelj vodi po navodilih, šteje v realizacijo predmeta odsotnega učitelja.
- Predmeti z realizacijo pod 90 % glede na načrt do danes so označeni z opozorilom.

### US-12 – Mesečni obračun (F11)
**Vloga:** organizator nadomeščanj
**Zgodba:** Kot organizator želim za izbrani mesec izvoziti plačane suplence po učiteljih, da jih posredujem računovodstvu.

**Pogoji sprejemljivosti:**
- Organizator izbere mesec in leto.
- Pregled vsebuje le izvedene suplence, označene kot plačane.
- Za vsakega učitelja je prikazano število plačanih suplenc.
- Gumb »Izvozi CSV« prenese datoteko s stolpci: učitelj, datum, ura, oddelek, predmet.

### US-13 – Ure za fond (F12)
**Vloga:** organizator nadomeščanj
**Zgodba:** Kot organizator želim izvoziti suplence, ki niso plačane, ampak štejejo v fond ur, da jih vnesem v šolsko aplikacijo za prisotnost.

**Pogoji sprejemljivosti:**
- Organizator izbere obdobje (od – do) in po želji učitelja.
- Pregled vsebuje le izvedene suplence, ki štejejo v fond ur.
- Gumb »Izvozi CSV« prenese datoteko s stolpci: učitelj, datum, ura, oddelek, vrsta suplence.
