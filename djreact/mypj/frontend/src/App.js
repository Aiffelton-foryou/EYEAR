// import logo from './logo.svg';
// import './App.css';
import './Hang.css';
import Hang from "./Hang.js";
import React from "react";

function App() {
  return (
    <div className="App">
      <link rel="preconnect" href="https://fonts.gstatic.com"></link>
      <link href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&amp;display=swap" rel="stylesheet"></link>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossOrigin="anonymous"></link>
      <header className="App-header">
        <Hang />
      </header>
    </div>
  );
}

export default App;
