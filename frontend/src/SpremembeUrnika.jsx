// SpremembeUrnika.jsx – spremembe urnika dijakovega oddelka za danes in jutri (WF-06, US-07)

import { useState, useEffect } from "react";

// datum v obliki "2026-11-03"; zamik = 0 za danes, 1 za jutri
function datumCez(zamik) {
  const d = new Date();
  d.setDate(d.getDate() + zamik);
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}

function SpremembeUrnika() {
  const [zamik, nastaviZamik] = useState(0);        // 0 = Danes, 1 = Jutri
  const [spremembe, nastaviSpremembe] = useState([]);

  // ob odprtju strani in ob kliku Danes/Jutri naloži spremembe za izbrani dan
  useEffect(() => {
    fetch("http://localhost:8000/spremembe/" + datumCez(zamik), {
      headers: { Authorization: "Bearer " + localStorage.getItem("zeton") },
    })
      .then((o) => o.json())
      .then(nastaviSpremembe);
  }, [zamik]);

  return (
    <div>
      <h2>Spremembe urnika</h2>
      <button onClick={() => nastaviZamik(0)}>Danes</button>
      <button onClick={() => nastaviZamik(1)}>Jutri</button>

      {/* ni sprememb (US-07) */}
      {spremembe.length === 0 && <p>{zamik === 0 ? "Danes" : "Jutri"} ni sprememb urnika</p>}

      {/* ena sprememba = en okvir, kot na WF-06 */}
      {spremembe.map((s) => (
        <div key={s.solska_ura} style={{ border: "1px solid gray", margin: "5px", padding: "5px" }}>
          <b>{s.solska_ura}. ura · {s.predmet}</b>
          <br />
          {s.odpade ? "Ura odpade" : "Nadomešča: " + s.nadomesca + " · " + s.ucilnica}
        </div>
      ))}
    </div>
  );
}

export default SpremembeUrnika;