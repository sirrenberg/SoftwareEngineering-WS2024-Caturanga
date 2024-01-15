import "../styles/Menu.css";
import { useEffect, useState } from "react";
import { ResultPreview } from "../types";
import Map from "../components/Map";
import { useAPI } from "../hooks/useAPI";
import { NavLink } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

function Results() {
  const { sendRequest } = useAPI();

  const [resultPreviews, setResultPreviews] = useState<ResultPreview[]>([]);
  const [selectedResultIndex, setSelectedResultIndex] = useState<number>(-1);

  useEffect(() => {
    sendRequest("/simulation_results/summary", "GET").then((data) => {
      setResultPreviews(data);
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
          {resultPreviews.length === 0 && <h3>Loading...</h3>}

          {resultPreviews &&
            resultPreviews.map((resultPreview, index) => {
              return (
                <button
                  key={resultPreview._id}
                  className={
                    "simple-button" +
                    (index === selectedResultIndex ? " selected-item" : "")
                  }
                  onClick={() => {
                    setSelectedResultIndex(index);
                  }}
                >
                  <p>{resultPreview._id}</p>
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
          {selectedResultIndex === -1
            ? "Choose a Simulation Result"
            : resultPreviews[selectedResultIndex]._id}
        </h2>

        <Map center={[0, 0]} shouldRecenter={true} />

        <div className="buttons-container">
          <Link
            to={
              selectedResultIndex === -1
                ? "/results/"
                : "/results/" + resultPreviews[selectedResultIndex]._id
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
