// Prijava.jsx – prijavna stran (WF-01, US-01)

import { useState } from "react";

function Prijava() {
  // stanja: kar uporabnik vpiše v obrazec in morebitno sporočilo o napaki
  const [email, nastaviEmail] = useState("");
  const [geslo, nastaviGeslo] = useState("");
  const [napaka, nastaviNapako] = useState("");

  // ob kliku na gumb Prijava pošlje podatke backendu (POST /prijava)
  async function prijavi(dogodek) {
    dogodek.preventDefault(); // obrazec ne osveži strani

    const odgovor = await fetch("http://localhost:8000/prijava", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, geslo: geslo }),
    });
    const podatki = await odgovor.json();

    // napačni podatki ali deaktiviran uporabnik → prikaže sporočilo backenda, ostane na prijavi
    if (!odgovor.ok) {
      nastaviNapako(podatki.detail);
      return;
    }

    // uspešna prijava → shrani žeton in vlogo v brskalnik ter preusmeri na stran vloge
    localStorage.setItem("zeton", podatki.zeton);
    localStorage.setItem("vloga", podatki.vloga);
    window.location.href = "/" + podatki.vloga;
  }

  return (
    <form onSubmit={prijavi}>
      <h1>Prijava</h1>

      <p>E-pošta</p>
      <input value={email} onChange={(e) => nastaviEmail(e.target.value)} />

      <p>Geslo</p>
      <input type="password" value={geslo} onChange={(e) => nastaviGeslo(e.target.value)} />

      <p><button type="submit">Prijava</button></p>

      {/* sporočilo se prikaže samo, če napaka obstaja */}
      {napaka && <p>{napaka}</p>}

      <p>Račune ustvari administrator šole.</p>
    </form>
  );
}

export default Prijava;