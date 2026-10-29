// Urnik.jsx – vnos ure urnika (WF-02, US-02); tedenski prikaz dodava pri #9

import { useState, useEffect } from "react";

// imena dni za spustni meni; dan v bazi = položaj v seznamu + 1 (ponedeljek = 1)
const DNEVI = ["Ponedeljek", "Torek", "Sreda", "Četrtek", "Petek"];
const URE = [1, 2, 3, 4, 5, 6, 7, 8];

function Urnik() {
  // seznami za spustne menije
  const [oddelki, nastaviOddelke] = useState([]);
  const [predmeti, nastaviPredmete] = useState([]);
  const [ucitelji, nastaviUcitelje] = useState([]);
  // vrednosti obrazca in sporočilo po shranjevanju
  const [ura, nastaviUro] = useState({});
  const [sporocilo, nastaviSporocilo] = useState("");
    // ure izbranega oddelka za tedensko tabelo
  const [urnik, nastaviUrnik] = useState([]);

  const glava = {
    "Content-Type": "application/json",
    Authorization: "Bearer " + localStorage.getItem("zeton"),
  };

  // ob odprtju strani naloži oddelke, predmete in učitelje
  useEffect(() => {
    fetch("http://localhost:8000/oddelki", { headers: glava }).then((o) => o.json()).then(nastaviOddelke);
    fetch("http://localhost:8000/predmeti", { headers: glava }).then((o) => o.json()).then(nastaviPredmete);
    fetch("http://localhost:8000/ucitelji", { headers: glava }).then((o) => o.json()).then(nastaviUcitelje);
  }, []);

  // spremeni eno polje obrazca
  function spremeni(polje, vrednost) {
    nastaviUro({ ...ura, [polje]: vrednost });
  }

    // naloži urnik izbranega oddelka (GET /urnik/{id})
  function naloziUrnik(oddelekId) {
    fetch("http://localhost:8000/urnik/" + oddelekId, { headers: glava })
      .then((o) => o.json())
      .then(nastaviUrnik);
  }

  // besedilo za eno celico tabele: "Predmet · Priimek" ali prazno, če ure ni
  function celica(dan, solskaUra) {
    const najdena = urnik.find((u) => u.dan_v_tednu === dan && u.solska_ura === solskaUra);
    return najdena ? najdena.predmet + " · " + najdena.ucitelj : "";
  }

  // gumb + Dodaj uro: pošlje uro backendu in prikaže odgovor ali opozorilo
  async function dodaj(dogodek) {
    dogodek.preventDefault();
    const odgovor = await fetch("http://localhost:8000/urnik", {
      method: "POST",
      headers: glava,
      body: JSON.stringify(ura),
    });
    const podatki = await odgovor.json();
        nastaviSporocilo(odgovor.ok ? podatki.sporocilo : "Opozorilo: " + podatki.detail);
    // po uspešnem vnosu osveži tabelo
    if (odgovor.ok) naloziUrnik(ura.oddelek_id);
  }

  return (
    <div>
      <h2>Urnik oddelka</h2>

      {/* required = brskalnik ne pusti oddaje, dokler polje ni izbrano (US-02) */}
      <form onSubmit={dodaj}>
        <select required onChange={(e) => { spremeni("oddelek_id", e.target.value); naloziUrnik(e.target.value); }}>
          <option value="">Oddelek</option>
          {oddelki.map((o) => <option key={o.id} value={o.id}>{o.oznaka}</option>)}
        </select>

        <select required onChange={(e) => spremeni("predmet_id", e.target.value)}>
          <option value="">Predmet</option>
          {predmeti.map((p) => <option key={p.id} value={p.id}>{p.naziv}</option>)}
        </select>

        <select required onChange={(e) => spremeni("ucitelj_id", e.target.value)}>
          <option value="">Učitelj</option>
          {ucitelji.map((u) => <option key={u.id} value={u.id}>{u.priimek} {u.ime}</option>)}
        </select>

        <select required onChange={(e) => spremeni("dan_v_tednu", e.target.value)}>
          <option value="">Dan</option>
          {DNEVI.map((dan, i) => <option key={dan} value={i + 1}>{dan}</option>)}
        </select>

        <select required onChange={(e) => spremeni("solska_ura", e.target.value)}>
          <option value="">Ura</option>
          {URE.map((u) => <option key={u} value={u}>{u}.</option>)}
        </select>

        <input placeholder="Učilnica" onChange={(e) => spremeni("ucilnica", e.target.value)} />

        <button type="submit">+ Dodaj uro</button>
      </form>

      {sporocilo && <p>{sporocilo}</p>}
            {/* tedenska tabela: vrstice = šolske ure, stolpci = dnevi (US-02, WF-02) */}
        <table border="1">
            <thead>
            <tr>
                <th>Ura</th>
                {DNEVI.map((dan) => <th key={dan}>{dan}</th>)}
            </tr>
            </thead>
            <tbody>
            {URE.map((u) => (
                <tr key={u}>
                <td>{u}.</td>
                {DNEVI.map((dan, i) => <td key={dan}>{celica(i + 1, u)}</td>)}
                </tr>
            ))}
            </tbody>
        </table>
    </div>
  );
}

export default Urnik;