import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { LatLngExpression } from "leaflet";
import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import Map from "../components/Map";
import { calcMapCenter } from "../helper/misc";
import { useAPI } from "../hooks/useAPI";
import "../styles/Menu.css";
import { ResultPreview } from "../types";
import { Link } from "react-router-dom";

function Results() {
  const { sendRequest } = useAPI();

  const [resultPreviews, setResultPreviews] = useState<
    ResultPreview[] | undefined
  >(undefined);
  const [selectedResultIndex, setSelectedResultIndex] = useState<number>(-1);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng]

  useEffect(() => {
    sendRequest("/simulation_results/summary", "GET").then((resultData) => {
      sendRequest("/simulations/summary", "GET").then((inputData) => {
        const res: ResultPreview[] = [];
        for (var resultElement of resultData) {
          for (var inputElement of inputData) {
            if (inputElement._id === resultElement.simulation_id) {
              res.push({
                id: resultElement._id,
                name: resultElement.name,
                input: inputElement,
                status: resultElement.status,
              });
            }
          }
        }
        setResultPreviews(res);
      });
    });
  }, []);

  return (
    <div
      className="menu-items-container content-page"
      id="outputs-menu-container"
    >
      <div className="items-list-container" id="outputs-list-container">
        <h2 className="items-list-title">Saved Simulation Results</h2>

        <div className="items-list" id="outputs-items-list">
          {!resultPreviews && <h3>Loading...</h3>}

          {resultPreviews && resultPreviews.length === 0 && <h3>Empty</h3>}

          {resultPreviews && resultPreviews.length > 0 &&
          resultPreviews.map((resultPreview, index) => {
            return (
              <button
                key={resultPreview.id}
                className={
                  "simple-button" +
                  (index === selectedResultIndex ? " selected-item" : "")
                }
                onClick={() => {
                  setSelectedResultIndex(index);
                }}
              >
                <p>{resultPreview.id}</p>
                <span className="items-list-item-icons">
                  <FontAwesomeIcon icon={faTrash} className="item-icon" />
                </span>
              </button>
            );
          })}
        </div>

        <NavLink to="/">
          <button className="simple-button">Home</button>
        </NavLink>
      </div>

      <div className="content-section">
        <h2 className="selected-item-title page-title">
          {resultPreviews
            ? resultPreviews.length > 0
              ? selectedResultIndex === -1
                ? "Choose a Simulation Result"
                : resultPreviews[selectedResultIndex].id
              : "Run a New Simulation"
            : ""}
        </h2>

        <Map
          input={!resultPreviews || selectedResultIndex === -1 ? undefined : resultPreviews[selectedResultIndex].input}
          center={mapCenter}
          shouldRecenter={true}
        />

        <div className="buttons-container">
          <Link
            to={
              selectedResultIndex === -1
                ? "/results/"
                : "/results/" +
                  (resultPreviews?.[selectedResultIndex]?._id ?? "")
            }
          >
            <button className="simple-button">Show Details</button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Results;
