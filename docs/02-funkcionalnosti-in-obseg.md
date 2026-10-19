# 02 – Funkcionalnosti in obseg

## Uporabniške vloge

| Vloga | Kaj lahko počne | Česa ne sme |
|---|---|---|
| **Administrator** | vnaša oddelke, predmete, učitelje in urnik; ustvarja račune in dodeljuje vloge | razporejati suplenc, videti razlogov odsotnosti |
| **Organizator nadomeščanj** | vnaša odsotnosti, potrjuje suplence, odobri odklonitve, pregleduje realizacijo in pripravi obračun | spreminjati urnika in uporabniških računov |
| **Učitelj** | javi načrtovano odsotnost in nerazpoložljivost, vidi svoje suplence, potrdi izvedbo in vpiše snov | dodeljevati suplenc, videti podatkov drugih učiteljev |
| **Dijak** | vidi spremembe urnika svojega oddelka | vpogleda v druge oddelke, kakršnih koli sprememb |

## Predvidene funkcionalnosti

| # | Funkcionalnost | MVP |
|---|---|:-:|
| F1 | Prijava in dostop glede na vlogo | ✔ |
| F2 | Vnos oddelkov, predmetov, učiteljev in urnika | ✔ |
| F3 | Vnos odsotnosti in samodejni izračun izpadlih ur iz urnika | ✔ |
| F4 | Predlog razvrščenih kandidatov za vsako izpadlo uro po pravilih šole | ✔ |
| F5 | Potrditev suplence s samodejno določitvijo vrste in plačljivosti | ✔ |
| F6 | Dnevni pregled sprememb za učitelja in oddelek | ✔ |
| F7 | Potrditev izvedbe suplence in vpis obravnavane snovi | |
| F8 | Javljanje nerazpoložljivosti vsaj 2 dni vnaprej | |
| F9 | Odklonitev suplence z utemeljitvijo in nov predlog kandidatov | |
| F10 | Pregled realizacije ur po oddelkih in predmetih | |
| F11 | Mesečni obračun plačanih suplenc (izvoz CSV) | |
| F12 | Seznam ur, ki štejejo v fond ur (izvoz CSV) | |

Domensko specifične funkcionalnosti v MVP: **F3, F4, F5**.

**Netrivialen delovni proces** – vsaka izpadla ura gre skozi stanja:
*nepokrita → predlagana → potrjena → izvedena* (ali *odklonjena* → nazaj med nepokrite, ali *odpadla*).

## Kasnejše nadgradnje

1. Uvoz urnika iz programa Untis
2. Prijava s šolskim računom Microsoft 365
3. Obveščanje po e-pošti ali s potisnimi obvestili
4. Prikaz suplenc na informacijskem zaslonu v avli
5. Statistika odsotnosti in obremenitve učiteljev

## Izven obsega

- Izdelava urnika (to dela Untis)
- E-dnevnik: ocene in prisotnost dijakov
- Izračun plač in vodenje fonda ur (interna aplikacija šole)
- Kadrovske evidence (bolniške, dopusti)
