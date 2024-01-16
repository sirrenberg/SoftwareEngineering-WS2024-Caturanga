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

  const [inputs, setInputs] = useState<Input[] | undefined>(undefined);
  const [selectedInputIndex, setSelectedInputIndex] = useState<number>(-1);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng]
  const [protectedInputIDs, setProtectedInputIDs] = useState<string[]>([]);

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

          {!inputs && 
          <h3>Loading...</h3>
          }

          {inputs && inputs.length === 0 &&
          <h3>Empty</h3>}

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
                  setInputId(inputs[index]._id);
                  setInputName(inputs[index].name);
                }}
              >
                <p>{input.name.length < 10 ? input.name :  input.name.slice(0,10) + "..."}</p>
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
                      //style={{ border: "none" , backgroundColor: "transparent" , padding : 0, color: "inherit"}}
                      onClick={(event) => {
                        event.stopPropagation();
                        console.log("Deleting " + input._id + " ...");
                        // if the input to be deleted is the one that is currently selected, deselect it
                        if (selectedInputIndex === index){
                          console.log("Entered the branch where selectedInputIndex === index", selectedInputIndex, index);
                          setSelectedInputIndex(-1);
                          console.log("selectedInputIndex is now", selectedInputIndex);
                        }
                        sendRequest("/simulations/" + input._id, "DELETE")
                        .then(_ => {
                          // if the input to be deleted is before the currently selected one, decrement the selected index
                          const indexOfDeleted = inputs.findIndex(i => i._id === input._id);
                          if (indexOfDeleted < selectedInputIndex){
                            setSelectedInputIndex(selectedInputIndex - 1);
                          }
                          console.log("Deleted simulation with id " + input._id);
                          setInputs(inputs.filter(i => i._id !== input._id));
                        })
                        .catch(err => {
                          console.log("Deleting simulation with id " + input._id + " lead to an error.");
                          console.log(err);
                        });
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
            !inputs || selectedInputIndex === -1 ? undefined : inputs[selectedInputIndex]
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
