// DnevniPregled.jsx – izpadle ure izbranega dne in predlog kandidatov (WF-04, US-04)

import { useState } from "react";

function DnevniPregled() {
  const [datum, nastaviDatum] = useState("");
  const [ure, nastaviUre] = useState([]);              // izpadle ure izbranega dne
  const [izbrana, nastaviIzbrano] = useState(null);    // ura, za katero prikazujemo kandidate
  const [kandidati, nastaviKandidate] = useState([]);

  const glava = { Authorization: "Bearer " + localStorage.getItem("zeton") };

  // ob izbiri datuma naloži izpadle ure tega dne
  function naloziDan(izbranDatum) {
    nastaviDatum(izbranDatum);
    nastaviIzbrano(null);
    fetch("http://localhost:8000/dnevni-pregled/" + izbranDatum, { headers: glava })
      .then((o) => o.json())
      .then(nastaviUre);
  }

  // klik na nepokrito uro: naloži razvrščen seznam kandidatov
  function izberiUro(ura) {
    nastaviIzbrano(ura);
    fetch("http://localhost:8000/kandidati/" + ura.id, { headers: glava })
      .then((o) => o.json())
      .then(nastaviKandidate);
  }

    // gumb Ura odpade: status ure postane "odpadla", nato osveži pregled dneva
  async function uraOdpade() {
    await fetch("http://localhost:8000/nadomescanja/" + izbrana.id + "/odpade", {
      method: "PUT",
      headers: glava,
    });
    naloziDan(datum);
  }

  // število nepokritih ur (WF-04: "Nepokrite ure: 3")
  const nepokrite = ure.filter((u) => u.status === "nepokrita").length;

  return (
    <div>
      <h2>Dnevni pregled</h2>
      Datum: <input type="date" value={datum} onChange={(e) => naloziDan(e.target.value)} />
      {" "}Nepokrite ure: {nepokrite}

      <table border="1">
        <thead>
          <tr><th>Ura</th><th>Oddelek</th><th>Predmet</th><th>Odsoten</th><th>Nadomešča</th><th>Status</th></tr>
        </thead>
        <tbody>
          {ure.map((u) => (
            // samo nepokrito uro je mogoče izbrati
            <tr key={u.id} onClick={() => u.status === "nepokrita" && izberiUro(u)}>
              <td>{u.solska_ura}.</td>
              <td>{u.oddelek}</td>
              <td>{u.predmet}</td>
              <td>{u.odsoten}</td>
              <td>{u.nadomesca}</td>
              <td>{u.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* predlog kandidatov za izbrano uro (US-04) */}
      {izbrana && (
        <div>
          <h3>Predlog kandidatov – {izbrana.solska_ura}. ura, {izbrana.oddelek}, {izbrana.predmet}</h3>
          <table border="1">
            <thead>
              <tr><th>#</th><th>Učitelj</th><th>Vrsta suplence</th><th>Plačana</th><th>Suplenc ta teden</th></tr>
            </thead>
            <tbody>
              {kandidati.map((k, i) => (
                <tr key={k.id}>
                  <td>{i + 1}</td>
                  <td>{k.ucitelj}{k.ura_odpadla && " (ura mu je odpadla)"}</td>
                  <td>{k.vrsta}</td>
                  <td>{k.placana ? "da" : "ne – fond"}</td>
                  <td>{k.suplenc_ta_teden}</td>
                </tr>
              ))}
            </tbody>
          </table>          
          {/* ni nobenega kandidata (US-04) */}
          {kandidati.length === 0 && <p>Ni prostega učitelja</p>}
          <button onClick={uraOdpade}>Ura odpade</button>
        </div>
      )}
    </div>
  );
}

export default DnevniPregled;