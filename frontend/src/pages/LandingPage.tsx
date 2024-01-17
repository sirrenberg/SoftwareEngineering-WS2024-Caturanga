import "../styles/LandingPage.css";
import { NavLink } from "react-router-dom";
import Credits from "../components/Credits.tsx";
import {
  ACLED_LOGO,
  FLEE_LOGO,
  NETLIGHT_LOGO,
  WFP_LOGO,
} from "../helper/constants/CreditsConstants.tsx";
import { CATURANGA_LOGO } from "../helper/constants/DesignConstants.tsx";

function LandingPage() {
  return (
    <div className="lp-container">
      <div id="lp-title-page" className="content-page">
        <div className="logo-container">
          <img className="logo" src={CATURANGA_LOGO} alt="logo" />
        </div>
        <div className="lp-title-page-content">
          <div className="lp-title-container lp-title-content-section">
            <h1 className="main-title">Caturanga</h1>
            <h2 className="sub-title">
              Simplifying Aid while Amplifying Impact
            </h2>

            <p className="lp-title-description">
              A Simulation Framework for Conflict-Driven Displacement
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
          {/*Credits and link to FLEE*/}
          <div className="img-container">
            <a href="https://flee.readthedocs.io/en/master/" target="_blank">
              <img className="source-logo" src={FLEE_LOGO} alt="flee-logo" />
            </a>
          </div>

          {/*Credits and link to ACLED*/}
          <div className="img-container">
            <a href="https://acleddata.com/" target="_blank">
              <img className="source-logo" src={ACLED_LOGO} alt="acled-logo" />
            </a>
          </div>

          {/*Credits and link to WFP*/}
          <div className="img-container">
            <a href="https://www.wfp.org/" target="_blank">
              <img
                id="wfp-logo"
                className="source-logo"
                src={WFP_LOGO}
                alt="wfp-logo"
              />
            </a>
          </div>

          {/* Credits and link to Netlight */}
          <div className="img-container">
            <a href="https://www.netlight.com/" target="_blank">
              <img
                className="source-logo"
                src={NETLIGHT_LOGO}
                alt="netlight-logo"
              />
            </a>
          </div>
        </div>
      </div>

      <div id="lp-simulation-page" className="content-page">
        <h1 id="lp-simulation-title" className="page-title">
          Tutorial
        </h1>
        <div className="video-container">
          <iframe
            src="https://www.youtube.com/embed/_TVtHzm9VpA"
            title="YouTube video player"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      </div>

      <div id="lp-credits-page" className="content-page">
        <h1 id="lp-credits-title" className="page-title">
          Credits
        </h1>
        <Credits />
      </div>
    </div>
  );
}

export default LandingPage;
