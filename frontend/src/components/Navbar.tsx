import { NavLink } from "react-router-dom";
import "../styles/Navbar.css";

function Navbar() {
  return (
    <div className="navbar-container">
      <div className="nav-title-container">
        <NavLink to="/" className="nav-link">
          <h2 className="nav-title">CATURANGA</h2>
        </NavLink>
      </div>

      <div className="nav-links-container">
        <NavLink to="/configurations">Configurations</NavLink>
        <NavLink to="/simulations">Simulations</NavLink>
      </div>
    </div>
  );
}

export default Navbar;
