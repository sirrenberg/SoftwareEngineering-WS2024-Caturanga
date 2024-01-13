import "../styles/Menu.css";
import { useEffect, useState, useContext } from "react";
import { StartSimContext } from "../contexts/StartSimContext";
import { Input } from "../types";
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

  const [inputs, setInputs] = useState<Input[]>([]);
  const [selectedInputIndex, setSelectedInputIndex] = useState<number>(-1);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng]

  const context = useContext(StartSimContext);
  if (!context) {
    throw new Error("StartSimContext is null");
  }
  const { setInput_id } = context;

  useEffect(() => {
    sendRequest("/simulations/summary", "GET").then((data) => {
      setInputs(data);
    });
  }, []);

  useEffect(() => {
    if (inputs.length > 0 && selectedInputIndex !== -1) {
      setMapCenter(calcMapCenter(inputs[selectedInputIndex].locations));
    }
  }, []);

  return (
    <div className="menu-items-container content-page">
      <div className="items-list-container">
        <h2 className="items-list-title">Saved Inputs</h2>

        <div className="items-list">

          {inputs.length === 0 && 
          <h3>Loading...</h3>
          }

          {inputs &&
          inputs.map((input, index) => {
            return (
              <button
                key={input._id}
                className={
                  "simple-button" +
                  (index === selectedInputIndex ? " selected-item" : "")
                }
                onClick={() => {
                  setSelectedInputIndex(index);
                  setMapCenter(calcMapCenter(input.locations));
                  setInput_id(inputs[index]._id);
                }}
              >
                <p>{input.name}</p>
                <span className="items-list-item-icons">
                  <NavLink to={"/inputs/" + input._id}>
                    <FontAwesomeIcon
                      icon={faPenToSquare}
                      className="item-icon"
                    />
                  </NavLink>
                  <FontAwesomeIcon icon={faTrash} className="item-icon" />
                </span>
              </button>
            );
          })}
        </div>

        <NavLink to="/inputs/new">
          <button className="simple-button">Add New Input</button>
        </NavLink>
      </div>

      <div className="content-section">
        <h2 className="selected-item-title page-title">
          {selectedInputIndex === -1
            ? "Choose an Input"
            : inputs[selectedInputIndex].region}
        </h2>

        <Map
          input={
            selectedInputIndex === -1 ? undefined : inputs[selectedInputIndex]
          }
          center={mapCenter}
          shouldRecenter={true}
        />

        <div className="buttons-container">
          <Link to={selectedInputIndex === -1 ? "/inputs/" : "/settings"}>
            <button
              className="simple-button"
              disabled={selectedInputIndex === -1}
            >
              Continue
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Inputs;
