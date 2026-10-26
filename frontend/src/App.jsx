// App.jsx – izbere, katera stran se prikaže: prijava, začetna stran vloge ali "Nimate dostopa"

import { useState, useEffect } from "react";
import Prijava from "./Prijava";

function App() {
  const vloga = localStorage.getItem("vloga");
  const zeton = localStorage.getItem("zeton");
  // ime strani iz naslova: "/organizator" → "organizator"
  const stran = window.location.pathname.substring(1);
  // rezultat preverjanja: null = še čakamo, true = sme, false = ne sme
  const [dostop, nastaviDostop] = useState(null);

  // ob odprtju strani vpraša backend, ali sme uporabnik videti to stran
  useEffect(() => {
    if (zeton === null || stran === "") return;
    fetch("http://localhost:8000/dostop/" + stran, {
      headers: { Authorization: "Bearer " + zeton },   // žeton pošljemo v glavi
    }).then((odgovor) => nastaviDostop(odgovor.ok));
  }, []);

  // ni prijavljen ali je na naslovu "/" → prijavna stran
  if (zeton === null || stran === "") {
    return <Prijava />;
  }

  // odjava: pobriše žeton in vlogo ter vrne na prijavo
  function odjava() {
    localStorage.clear();
    window.location.href = "/";
  }

  // odgovor backenda še ni prišel → ne prikaže ničesar
  if (dostop === null) {
    return null;
  }

  // stran ni namenjena tej vlogi (US-01)
  if (dostop === false) {
    return (
      <div>
        <h1>Nimate dostopa</h1>
        <button onClick={odjava}>Odjava</button>
      </div>
    );
  }

  // začetna stran vloge – vsebino dodava pri naslednjih zgodbah
  return (
    <div>
      <p>Prijavljen: {vloga} | <button onClick={odjava}>Odjava</button></p>
      <h1>Začetna stran – {vloga}</h1>
    </div>
  );
}

export default App;