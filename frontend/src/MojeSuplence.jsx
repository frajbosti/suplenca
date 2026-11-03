// MojeSuplence.jsx – suplence prijavljenega učitelja (WF-05, US-06)

import { useState, useEffect } from "react";

function MojeSuplence() {
  const [suplence, nastaviSuplence] = useState([]);

  // ob odprtju strani naloži suplence; backend ve iz žetona, kateri učitelj je prijavljen
  useEffect(() => {
    fetch("http://localhost:8000/moje-suplence", {
      headers: { Authorization: "Bearer " + localStorage.getItem("zeton") },
    })
      .then((o) => o.json())
      .then(nastaviSuplence);
  }, []);

  return (
    <div>
      <h2>Moje suplence</h2>

      {/* ni suplenc (US-06) */}
      {suplence.length === 0 && <p>Ta teden nimate suplenc</p>}

      {/* ena suplenca = en okvir, kot na WF-05 */}
      {suplence.map((s) => (
        <div key={s.datum + "-" + s.solska_ura} style={{ border: "1px solid gray", margin: "5px", padding: "5px" }}>
          <b>{s.datum} · {s.solska_ura}. ura · {s.oddelek} · {s.predmet}</b>
          <br />
          Učilnica {s.ucilnica} · {s.vrsta} · {s.placana ? "plačana" : "šteje v fond"}
          {/* navodila samo, če obstajajo (US-06) */}
          {s.navodila && <p>Navodila: {s.navodila}</p>}
        </div>
      ))}
    </div>
  );
}

export default MojeSuplence;