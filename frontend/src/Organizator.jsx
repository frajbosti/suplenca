// Organizator.jsx – stran organizatorja z menijem (WF-03, WF-04)

import { useState } from "react";
import DnevniPregled from "./DnevniPregled";
import Odsotnost from "./Odsotnost";

function Organizator() {
  // katera stran iz menija je izbrana
  const [izbira, nastaviIzbiro] = useState("pregled");

  return (
    <div>
      {/* meni (WF-03, WF-04); Realizacija, Obračun in Ure za fond niso v MVP */}
      <p>
        <button onClick={() => nastaviIzbiro("pregled")}>Dnevni pregled</button>
        <button onClick={() => nastaviIzbiro("odsotnosti")}>Odsotnosti</button>
      </p>

      {izbira === "pregled" && <DnevniPregled />}
      {izbira === "odsotnosti" && <Odsotnost />}
    </div>
  );
}

export default Organizator;