import {
  faTrash,
  faInfo,
  faMapLocationDot,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { LatLngExpression } from "leaflet";
import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import Map from "../components/Map";
import { calcMapCenter, sliceName } from "../helper/misc";
import { useAPI } from "../hooks/useAPI";
import "../styles/Menu.css";
import { ResultPreview, SimulationStatus, MapInputType } from "../types";
import { Link } from "react-router-dom";
import DataSourceModal from "../components/DataSourceModal";
import MapLegendModal from "../components/MapLegendModal";

const resultNameCutOff: number = 15;

// Menu page for selecting a result
function Results() {
  const { sendRequest } = useAPI();

  const [resultPreviews, setResultPreviews] = useState<
    ResultPreview[] | undefined
  >(undefined);
  const [selectedResultIndex, setSelectedResultIndex] = useState<number>(-1);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng]
  const [indexForDeletion, setIndexForDeletion] = useState<number | undefined>(
    undefined
  );
  const [isDataSourceModal, setDataSourceModal] = useState(false);
  const [isMapLegendModal, setMapLegendModal] = useState(false);

  useEffect(() => {
    sendRequest("/simulation_results/summary", "GET").then((resultData) => {
      sendRequest("/simulations/summary", "GET").then((inputData) => {
        const res: ResultPreview[] = [];
        for (var resultElement of resultData) {
          for (var inputElement of inputData.data) {
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

          {resultPreviews &&
            resultPreviews.length > 0 &&
            resultPreviews.map((resultPreview, index) => {
              return (
                <button
                  key={resultPreview.id}
                  className={
                    "simple-button" +
                    (index === selectedResultIndex ? " selected-item" : "")
                  }
                  disabled={index === indexForDeletion}
                  onClick={() => {
                    setSelectedResultIndex(index);
                    setMapCenter(
                      calcMapCenter(resultPreviews[index].input.locations)
                    );
                  }}
                >
                  <div className="items-list-item-text">
                    <p className="item-preview-name">
                      {sliceName(resultPreview.name, resultNameCutOff)}
                    </p>
                    <p className="item-preview-status">{`Status: ${resultPreview.status}`}</p>
                  </div>
                  <span className="items-list-item-icons">
                    <FontAwesomeIcon
                      icon={faTrash}
                      className="item-icon"
                      onClick={(event) => {
                        event.stopPropagation();
                        setSelectedResultIndex(-1);
                        setIndexForDeletion(index);
                        const idForDeletion: string = resultPreview.id;
                        sendRequest(
                          `/simulation_results/${idForDeletion}`,
                          "DELETE"
                        )
                          .then(() => {
                            setResultPreviews(
                              resultPreviews.filter(
                                (r) => r.id !== idForDeletion
                              )
                            );
                            setIndexForDeletion(undefined);
                          })
                          .catch((err) => {
                            console.error(err);
                          });
                      }}
                    />
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
                : `${resultPreviews[selectedResultIndex].name}`
              : "Run a New Simulation"
            : ""}
        </h2>
        {resultPreviews &&
          resultPreviews.length > 0 &&
          selectedResultIndex !== -1 && (
            <h3 className="selected-item-subtitle">{`Status: ${resultPreviews[selectedResultIndex].status}`}</h3>
          )}
        <h1>Used Input</h1>

        <Map
          input={
            !resultPreviews || selectedResultIndex === -1
              ? undefined
              : resultPreviews[selectedResultIndex].input
          }
          center={mapCenter}
          shouldRecenter={true}
        />

        <div className="buttons-container">
          <Link
            to={
              selectedResultIndex === -1
                ? "/results/"
                : "/results/" +
                  (resultPreviews?.[selectedResultIndex]?.id ?? "")
            }
          >
            <button
              className="simple-button"
              disabled={
                !resultPreviews ||
                selectedResultIndex === -1 ||
                resultPreviews[selectedResultIndex].status !==
                  SimulationStatus.done
              }
            >
              Show Details
            </button>
          </Link>
        </div>
      </div>

      {selectedResultIndex !== -1 && (
        <>
          <div
            className="simple-button info-button"
            id="sources-button"
            onClick={() => {
              setDataSourceModal(true);
            }}
          >
            <FontAwesomeIcon icon={faInfo} className="sources-icon" />
          </div>
          <div
            className="simple-button info-button"
            id="map-legend-button"
            onClick={() => {
              setMapLegendModal(true);
            }}
          >
            <FontAwesomeIcon
              icon={faMapLocationDot}
              className="map-legend-icon"
            />
          </div>
        </>
      )}

      {isMapLegendModal && (
        <MapLegendModal
          setMapLegendModalOpen={setMapLegendModal}
          mapInputType={MapInputType.inputs}
        />
      )}

      {isDataSourceModal && resultPreviews && selectedResultIndex !== -1 && (
        <DataSourceModal
          setDataSourceModalOpen={setDataSourceModal}
          acled_url={
            resultPreviews[selectedResultIndex].input.data_sources.acled.url
          }
          acled_last_update_date={
            resultPreviews[selectedResultIndex].input.data_sources.acled
              .last_update
          }
          population_url={
            resultPreviews[selectedResultIndex].input.data_sources.population
              .url
          }
          population_last_update_date={
            resultPreviews[selectedResultIndex].input.data_sources.population
              .latest_population_date
          }
          camp_url={
            resultPreviews[selectedResultIndex].input.data_sources.camps
              .url_from_last_update
          }
          camp_last_update_date={
            resultPreviews[selectedResultIndex].input.data_sources.camps
              .last_update
          }
        />
      )}
    </div>
  );
}

export default Results;
