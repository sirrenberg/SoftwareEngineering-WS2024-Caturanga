import "../styles/AddInput.css";
import { useParams } from "react-router-dom";
import Map from "../components/Map";
import { simulationData } from "../test-data/data";
import { useState } from "react";
import { Button } from "@mui/material";
import {
  MapOperatingMode,
  Simulation,
  SimLocation,
  LocationType,
} from "../types";

import { useMapEvent } from "react-leaflet/hooks";

function AddInput() {
  const { id } = useParams<{ id: string }>();

  const [simulation, _] = useState<Simulation>(getSimulation());
  //   const [operationMode, setOperationMode] = useState<MapOperatingMode>(
  //     MapOperatingMode.vizualizing
  //   ); // ["visualizing", "add-location", "add-route"]
  //   const [selectedNodes, setSelectedNodes] = useState<SimLocation[]>([]); // [node1, node2]

  function getSimulation() {
    const simulation = simulationData.find((sim) => sim.name === id);

    if (simulation) {
      return simulation;
    } else {
      throw new Error("Simulation not found");
    }
  }

  //   function MapClickHandler(): null {
  //     useMapEvent("click", (event) => {
  //       // Access the clicked coordinates
  //       const { lat, lng } = event.latlng;

  //       //if operation mode is add-location
  //       if (operationMode === MapOperatingMode.adding_location) {
  //         // add a new node to the data
  //         const newNode: SimLocation = {
  //           name: "New Node",
  //           latitude: lat,
  //           longitude: lng,
  //           population: 1000000,
  //           region: "New Region",
  //           country: "New Country",
  //           location_type: LocationType.camp,
  //         };

  //         // reset operation mode
  //         setOperationMode(MapOperatingMode.vizualizing);
  //       }
  //     });
  //     return null;
  //   }

  //   function NodeClickHandler(location: SimLocation): void {
  //     if (
  //       selectedNodes.length < 2 &&
  //       operationMode === MapOperatingMode.adding_route
  //     ) {
  //       setSelectedNodes([...selectedNodes, location]);

  //       // if there are already 2 nodes selected
  //       if (selectedNodes.length === 1) {
  //         // add a new route to the data
  //         const newRoute = {
  //           from: selectedNodes[0].name,
  //           to: location.name,
  //           distance: 100,
  //         };

  //         const newInputs = [...inputs];
  //         newInputs[selectedInputIndex].routes.push(newRoute);
  //         setInputs(newInputs);

  //         // reset operation mode
  //         setOperationMode(MapOperatingMode.vizualizing);
  //         setSelectedNodes([]);
  //       }
  //     }
  //   }

  // get the simulation data

  return (
    <div className="content-page add-input-container">
      <h1>Edit Simulation: {simulation.name}</h1>

      <div className="map-content-container add-input-section">
        <h2 className="add-input-section-title">Locations & Routes</h2>
        <Map
          input={simulation}
          center={[0, 0]}
          // MapClickHandler={MapClickHandler}
          // NodeClickHandler={cl}
        />
        <div className="map-content-buttons">
          <Button variant="contained" sx={{ width: "200px" }}>
            Edit Conflict Input
          </Button>
          <Button variant="contained" sx={{ width: "200px" }}>
            Edit Conflict Input
          </Button>
        </div>
      </div>
    </div>
  );
}

export default AddInput;
