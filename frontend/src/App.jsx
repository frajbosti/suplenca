// App.jsx – izbere, katera stran se prikaže (prijava ali začetna stran vloge)

import Prijava from "./Prijava";

function App() {
  // vloga prijavljenega uporabnika, shranjena ob prijavi (null = ni prijavljen)
  const vloga = localStorage.getItem("vloga");

  // ni prijavljen ali je na naslovu "/" → prijavna stran
  if (vloga === null || window.location.pathname === "/") {
    return <Prijava />;
  }

  // odjava: pobriše žeton in vlogo ter vrne na prijavo (gumb Odjava na vseh WF)
  function odjava() {
    localStorage.clear();
    window.location.href = "/";
  }

  // začetna stran vloge – vsebino dodava pri naslednjih zgodbah (US-02 …)
  return (
    <div>
      <p>Prijavljen: {vloga} | <button onClick={odjava}>Odjava</button></p>
      <h1>Začetna stran – {vloga}</h1>
    </div>
  );
}

export default App;