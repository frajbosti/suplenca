// Odsotnost.jsx – vnos odsotnosti učitelja (WF-03, US-03)

import { useState, useEffect } from "react";

// razlogi za spustni meni (WF-03)
const RAZLOGI = ["Bolniška", "Izobraževanje", "Službena pot", "Drugo"];

function Odsotnost() {
  const [ucitelji, nastaviUcitelje] = useState([]);   // za spustni meni
  const [odsotnost, nastaviOdsotnost] = useState({}); // vrednosti obrazca
  const [sporocilo, nastaviSporocilo] = useState("");
  const [izpadle, nastaviIzpadle] = useState([]);    // izpadle ure, ki jih vrne backend

  const glava = {
    "Content-Type": "application/json",
    Authorization: "Bearer " + localStorage.getItem("zeton"),
  };

  // ob odprtju strani naloži seznam učiteljev
  useEffect(() => {
    fetch("http://localhost:8000/ucitelji", { headers: glava }).then((o) => o.json()).then(nastaviUcitelje);
  }, []);

  // spremeni eno polje obrazca
  function spremeni(polje, vrednost) {
    nastaviOdsotnost({ ...odsotnost, [polje]: vrednost });
  }

  // gumb Shrani odsotnost: pošlje podatke backendu in prikaže odgovor ali opozorilo
  async function shrani(dogodek) {
    dogodek.preventDefault();
    const odgovor = await fetch("http://localhost:8000/odsotnosti", {
      method: "POST",
      headers: glava,
      body: JSON.stringify(odsotnost),
    });
    const podatki = await odgovor.json();
    nastaviSporocilo(odgovor.ok ? podatki.sporocilo : "Opozorilo: " + podatki.detail);
        // po uspešnem shranjevanju prikaže izpadle ure; ob napaki seznam pobriše
    nastaviIzpadle(odgovor.ok ? podatki.izpadle_ure : []);
  }

  return (
    <div>
      <h2>Nova odsotnost</h2>

      {/* required = brez izpolnjenega polja obrazca ni mogoče oddati (US-03) */}
      <form onSubmit={shrani}>
        <select required onChange={(e) => spremeni("ucitelj_id", e.target.value)}>
          <option value="">Učitelj</option>
          {ucitelji.map((u) => <option key={u.id} value={u.id}>{u.priimek} {u.ime}</option>)}
        </select>

        Od <input type="date" required onChange={(e) => spremeni("datum_od", e.target.value)} />
        Do <input type="date" required onChange={(e) => spremeni("datum_do", e.target.value)} />

        <select required onChange={(e) => spremeni("razlog", e.target.value)}>
          <option value="">Razlog</option>
          {RAZLOGI.map((r) => <option key={r} value={r}>{r}</option>)}
        </select>

        <input placeholder="Navodila za nadomeščanje" onChange={(e) => spremeni("navodila", e.target.value)} />

        <button type="submit">Shrani odsotnost</button>
      </form>

      {sporocilo && <p>{sporocilo}</p>}
            {/* izpadle ure po shranjevanju odsotnosti (WF-03, US-03) */}
      {sporocilo === "Odsotnost shranjena" && (
        <div>
          <p>Izpadle ure (izračunano iz urnika): {izpadle.length}</p>
          <table border="1">
            <thead>
              <tr><th>Datum</th><th>Ura</th><th>Oddelek</th><th>Predmet</th><th>Učilnica</th><th>Status</th></tr>
            </thead>
            <tbody>
              {izpadle.map((i) => (
                <tr key={i.datum + "-" + i.solska_ura}>
                  <td>{i.datum}</td>
                  <td>{i.solska_ura}.</td>
                  <td>{i.oddelek}</td>
                  <td>{i.predmet}</td>
                  <td>{i.ucilnica}</td>
                  <td>{i.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Odsotnost;