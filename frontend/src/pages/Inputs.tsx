import "../styles/Menu.css";
import { useEffect, useState, useContext } from "react";
import { StartSimContext } from "../contexts/StartSimContext";
import { Input } from "../types";
import Map from "../components/Map";
import { LatLngExpression } from "leaflet";
import { Link } from "react-router-dom";
import { useAPI } from "../hooks/useAPI";
import { calcMapCenter, sliceName } from "../helper/misc";
import { NavLink } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPenToSquare,
  faTrash,
  faInfo,
} from "@fortawesome/free-solid-svg-icons";
import DataSourceModal from "../components/DataSourceModal";
import InputDeletionConfirmation from "../components/InputDeletionConfirmation";

const inputNameCutOff : number = 10;

function Inputs() {
  const { sendRequest } = useAPI();

  const [inputs, setInputs] = useState<Input[] | undefined>(undefined);
  const [selectedInputIndex, setSelectedInputIndex] = useState<number>(-1);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng]
  const [isDataSourceModal, setDataSourceModal] = useState(false);
  const [protectedInputIDs, setProtectedInputIDs] = useState<string[]>([]);
  const [indexForDeletion, setIndexForDeletion] = useState<number | undefined>(undefined);
  const [isInputDeletionConfirmationActive, setInputDeletionConfirmation] = useState(false);

  const context = useContext(StartSimContext);
  if (!context) {
    throw new Error("StartSimContext is null");
  }
  const { setInputId, setInputName } = context;

  useEffect(() => {
    sendRequest("/simulations/summary", "GET").then((response) => {
      const { data, protectedIDs } = response;
      setInputs(data);
      setProtectedInputIDs(protectedIDs);
    });
  }, []);

  useEffect(() => {
    if (inputs && selectedInputIndex !== -1) {
      setMapCenter(calcMapCenter(inputs[selectedInputIndex].locations));
    }
  }, []);

  return (
    <div className="menu-items-container content-page">
      <div className="items-list-container">
        <h2 className="items-list-title">Saved Inputs</h2>

        <div className="items-list">
          {!inputs && <h3>Loading...</h3>}

          {inputs && inputs.length === 0 && <h3>Empty</h3>}

          {inputs &&
            inputs.map((input, index) => {
              return (
                <button
                  key={input._id}
                  className={
                    "simple-button" +
                    (index === selectedInputIndex ? " selected-item" : "")
                  }
                  disabled={index === indexForDeletion}
                  onClick={() => {
                    setSelectedInputIndex(index);
                    setMapCenter(calcMapCenter(input.locations));
                    setInputId(inputs[index]._id);
                    setInputName(inputs[index].name);
                  }}
                >
                  <p>{sliceName(input.name, inputNameCutOff)}</p>
                  <span className="items-list-item-icons">
                    <NavLink to={"/inputs/" + input._id}>
                      <FontAwesomeIcon
                        icon={faPenToSquare}
                        className="item-icon"
                      />
                    </NavLink>
                    {!protectedInputIDs.includes(input._id) && (
                      <FontAwesomeIcon
                        icon={faTrash}
                        className="item-icon"
                        onClick={(event) => {
                          event.stopPropagation();
                          setIndexForDeletion(index);
                          setInputDeletionConfirmation(true);
                        }}
                      />
                    )}
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
          {inputs
            ? inputs.length > 0
              ? selectedInputIndex === -1
                ? "Choose an Input"
                : inputs[selectedInputIndex].name
              : "Create a New Input"
            : ""}
        </h2>

        <Map
          input={
            !inputs || selectedInputIndex === -1
              ? undefined
              : inputs[selectedInputIndex]
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

      {inputs && selectedInputIndex !== -1 && (
        <div
          className="simple-button sources-button"
          onClick={() => {
            setDataSourceModal(true);
          }}
        >
          <FontAwesomeIcon icon={faInfo} className="sources-icon" />
        </div>
      )}

      {isInputDeletionConfirmationActive && (
        <InputDeletionConfirmation
          performInputDeletion={() => {
            // if the input to be deleted is currently selected, deselect it
            if (selectedInputIndex === indexForDeletion) {
              setSelectedInputIndex(-1);
            }
            setInputDeletionConfirmation(false);
            const idForDeletion : string = inputs![indexForDeletion!]._id;
            sendRequest("/simulations/" + idForDeletion, "DELETE")
              .then(() => {
                // if the input to be deleted is above the currently selected one,
                // decrement the selected index so that the same index stays selected
                if (indexForDeletion! < selectedInputIndex) {
                  setSelectedInputIndex(selectedInputIndex - 1);
                }
                setIndexForDeletion(undefined);
                const newInputs : Input[] = inputs!.filter((i) => i._id !== idForDeletion);
                setInputs(newInputs);
              })
              .catch((err) => {console.error(err);});
          }}
          abortInputDeletion={() => {
            setIndexForDeletion(undefined);
            setInputDeletionConfirmation(false);
          }}
        />
      )}

      {isDataSourceModal && (
        <DataSourceModal
          setDataSourceModalOpen={setDataSourceModal}
          acled_url={inputs![selectedInputIndex].data_sources.acled.url}
          acled_last_update_date={
            inputs![selectedInputIndex].data_sources.acled.last_update
          }
          population_url={
            inputs![selectedInputIndex].data_sources.population.url
          }
          population_last_update_date={
            inputs![selectedInputIndex].data_sources.population
              .latest_population_date
          }
          camp_url={
            inputs![selectedInputIndex].data_sources.camps.url_from_last_update
          }
          camp_last_update_date={
            inputs![selectedInputIndex].data_sources.camps.last_update
          }
        />
      )}
    </div>
  );
}

export default Inputs;
