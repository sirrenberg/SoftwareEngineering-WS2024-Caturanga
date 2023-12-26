import "../styles/Inputs.css";
import { useEffect, useState } from "react";
import { Simulation } from "../types";
import Map from "../components/Map";
import { LatLngExpression } from "leaflet";
import { Link } from "react-router-dom";
import { useAPI } from "../hooks/useAPI";
import { calcMapCenter } from "../helper/misc";
import { NavLink } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPenToSquare, faTrash } from "@fortawesome/free-solid-svg-icons";

function Inputs() {
  const { sendRequest } = useAPI();

  const [inputs, setInputs] = useState<Simulation[]>([]);
  const [selectedInputIndex, setSelectedInputIndex] = useState<number>(0);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng

  useEffect(() => {
    sendRequest("/simulations", "GET").then((data) => {
      setInputs(data);
    });
  }, []);

  useEffect(() => {
    if (inputs.length > 0) {
      setMapCenter(calcMapCenter(inputs[selectedInputIndex].locations));
    }
  }, []);

  if (inputs.length === 0) {
    return <div>Loading...</div>;
  }

  return (
    <div className="inputs-container content-page">
      <div className="inputs-list-container">
        <h2 className="inputs-list-title">Saved Inputs</h2>

        <div className="inputs-list">
          {inputs.map((input, index) => {
            return (
              <button
                key={input._id}
                className={
                  "simple-button" +
                  (index === selectedInputIndex ? " selected-input" : "")
                }
                onClick={() => {
                  setSelectedInputIndex(index);
                  setMapCenter(calcMapCenter(input.locations));
                }}
              >
                <p>{input.region}</p>
                <span className="inputs-list-item-icons">
                  <NavLink to={"/inputs/" + input._id}>
                    <FontAwesomeIcon
                      icon={faPenToSquare}
                      className="input-icon"
                    />
                  </NavLink>
                  <FontAwesomeIcon icon={faTrash} className="input-icon" />
                </span>
              </button>
            );
          })}
        </div>

        <NavLink to="/inputs/new">
          <button className="simple-button">Add New Input</button>
        </NavLink>
      </div>

      <div className="map-section">
        <h2 className="selected-input-title page-title">
          Preview: {inputs[selectedInputIndex].region}
        </h2>

        <Map input={inputs[selectedInputIndex]} center={mapCenter} />

        <div className="buttons-container">
          <Link to={"/inputs/" + inputs[selectedInputIndex]._id}>
            <button className="simple-button">Continue</button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Inputs;
