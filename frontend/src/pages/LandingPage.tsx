import Map from "../components/Map";
import "../styles/LandingPage.css";
import { NavLink } from "react-router-dom";

function LandingPage() {
  return (
    <div className="lp-container">
      <div id="lp-title-page" className="content-page">
        <div className="logo-container">
          <img className="logo" src="./generic-logo.png" alt="logo" />
        </div>
        <div className="lp-title-page-content">
          <div className="lp-title-container lp-title-content-section">
            <h1 className="main-title">
              Caturanga
              <h2 className="sub-title">A Humanitarian Logistics Tool</h2>
            </h1>

            <p className="lp-title-description">
              Experience the power of Compassion in Crisis through Interactive
              Refugee Movement Mapping
            </p>

            <div className="lp-title-buttons-container">
              <NavLink to="/inputs">
                <button className="lp-title-button simple-button">
                  Start new Simulation
                </button>
              </NavLink>

              <NavLink to="/results">
                <button className="lp-title-button simple-button">
                  Analyze past Simulations
                </button>
              </NavLink>
            </div>
          </div>
          <div className="lp-title-map-container lp-title-content-section">
            <img
              className="lp-title-map"
              src="./dotted-world-map.png"
              alt="map"
            />
          </div>
        </div>
      </div>
      <div className="lp-sources">
        <p className="sources-description">Powered by</p>
        <div className="sources-logos-container">
          <div className="img-container">
            <img className="source-logo" src="./flee.png" alt="flee-logo" />
          </div>
          <div className="img-container">
            <img
              className="source-logo"
              src="./acled-logo.png"
              alt="acled-logo"
            />
          </div>
          <div className="img-container">
            <img
              id="wfp-logo"
              className="source-logo"
              src="./wfp-logo.png"
              alt="wfp-logo"
            />
          </div>
        </div>
      </div>

      <div id="lp-simulation-page" className="content-page">
        <h1 id="lp-simulation-title" className="page-title">
          Latest Simulation
        </h1>
        <Map />
      </div>
    </div>
  );
}

export default LandingPage;
