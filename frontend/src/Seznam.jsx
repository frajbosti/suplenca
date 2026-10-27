// Seznam.jsx – tabela z dodajanjem, urejanjem in brisanjem (oddelki, predmeti, učitelji – US-02)

import { useState, useEffect } from "react";

// naslov = besedilo nad tabelo, pot = naslov v API (npr. "oddelki"), polja = imena stolpcev
function Seznam({ naslov, pot, polja }) {
  const [vrstice, nastaviVrstice] = useState([]);      // podatki iz baze
  const [obrazec, nastaviObrazec] = useState({});      // vrednosti v poljih obrazca
  const [urejamId, nastaviUrejamId] = useState(null);  // null = dodajanje, sicer id vrstice, ki jo urejamo

  // glava, ki jo pošljemo pri vsakem klicu: oblika podatkov in žeton
  const glava = {
    "Content-Type": "application/json",
    Authorization: "Bearer " + localStorage.getItem("zeton"),
  };

  // prebere seznam iz backenda (GET)
  function nalozi() {
    fetch("http://localhost:8000/" + pot, { headers: glava })
      .then((odgovor) => odgovor.json())
      .then((podatki) => nastaviVrstice(podatki));
  }

  // ob prvem prikazu in ob menjavi strani (npr. iz oddelkov na predmete) pobriše obrazec in naloži seznam
  useEffect(() => {
    nastaviObrazec({});
    nastaviUrejamId(null);
    nalozi();
  }, [pot]);

  // gumb Dodaj/Shrani: POST za novo vrstico, PUT za urejanje obstoječe
  async function shrani(dogodek) {
    dogodek.preventDefault();
    const naslovKlica = urejamId === null ? pot : pot + "/" + urejamId;
    await fetch("http://localhost:8000/" + naslovKlica, {
      method: urejamId === null ? "POST" : "PUT",
      headers: glava,
      body: JSON.stringify(obrazec),
    });
    nastaviObrazec({});
    nastaviUrejamId(null);
    nalozi();
  }

  // gumb Uredi: podatke vrstice prepiše v obrazec
  function uredi(vrstica) {
    nastaviObrazec(vrstica);
    nastaviUrejamId(vrstica.id);
  }

  // gumb Izbriši: DELETE in ponovno nalaganje seznama
  async function izbrisi(id) {
    await fetch("http://localhost:8000/" + pot + "/" + id, { method: "DELETE", headers: glava });
    nalozi();
  }

  // geslo je samo v obrazcu, v tabeli ga ne prikazujemo
  const stolpci = polja.filter((polje) => polje !== "geslo");

  return (
    <div>
      <h2>{naslov}</h2>

      <table border="1">
        <thead>
          <tr>
            {stolpci.map((polje) => <th key={polje}>{polje}</th>)}
            <th></th>
          </tr>
        </thead>
        <tbody>
          {vrstice.map((vrstica) => (
            <tr key={vrstica.id}>
              {stolpci.map((polje) => <td key={polje}>{vrstica[polje]}</td>)}
              <td>
                <button onClick={() => uredi(vrstica)}>Uredi</button>
                <button onClick={() => izbrisi(vrstica.id)}>Izbriši</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* obrazec: za vsako polje eno vnosno polje */}
      <form onSubmit={shrani}>
        {polja.map((polje) => (
          <input
            key={polje}
            placeholder={polje}
            value={obrazec[polje] || ""}
            onChange={(e) => nastaviObrazec({ ...obrazec, [polje]: e.target.value })}
          />
        ))}
        <button type="submit">{urejamId === null ? "Dodaj" : "Shrani"}</button>
      </form>
    </div>
  );
}

export default Seznam;