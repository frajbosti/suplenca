// Administrator.jsx – stran administratorja z menijem (WF-02, US-02)

import { useState } from "react";
import Seznam from "./Seznam";

function Administrator() {
  // katera stran iz menija je izbrana
  const [izbira, nastaviIzbiro] = useState("oddelki");

  return (
    <div>
      {/* meni (WF-02); Urnik dodava pri #8 */}
      <p>
        <button onClick={() => nastaviIzbiro("oddelki")}>Oddelki</button>
        <button onClick={() => nastaviIzbiro("predmeti")}>Predmeti</button>
        <button onClick={() => nastaviIzbiro("ucitelji")}>Učitelji</button>
      </p>

      {izbira === "oddelki" && <Seznam naslov="Oddelki" pot="oddelki" polja={["oznaka"]} />}
      {izbira === "predmeti" && <Seznam naslov="Predmeti" pot="predmeti" polja={["kratica", "naziv"]} />}
      {izbira === "ucitelji" && <Seznam naslov="Učitelji" pot="ucitelji" polja={["ime", "priimek", "email", "geslo"]} />}
    </div>
  );
}

export default Administrator;