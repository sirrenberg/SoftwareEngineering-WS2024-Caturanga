import { NavLink } from "react-router-dom";
import "../styles/Navbar.css";

function Navbar() {
  return (
    <div className="navbar-container">
      <div className="logo-container">
        <NavLink to="/" className="nav-link">
          <img src="./bayern-wappen.png" alt="Bayern wappen" className="logo" />
        </NavLink>
      </div>

      <div className="nav-links-container">
        <NavLink to="/results">Ergebnisse</NavLink>
        <NavLink to="/seats">Sitzverteilung</NavLink>
        <NavLink to="/overview">Übersicht</NavLink>
      </div>
    </div>
  );
}

export default Navbar;
