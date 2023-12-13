import "../styles/AddInput.css";
import { useParams } from "react-router-dom";
import Map from "../components/Map";
import { useEffect, useState } from "react";
import { Button } from "@mui/material";
import {
  MapOperatingMode,
  Simulation,
  SimLocation,
  LocationType,
} from "../types";

import { useMapEvent } from "react-leaflet/hooks";
import { useAPI } from "../hooks/useAPI";
import { calcMapCenter } from "../helper/misc";
import { LatLngExpression } from "leaflet";

function AddInput() {
  const { id } = useParams<{ id: string }>();

  const [simulation, setSimulation] = useState<Simulation>(null!);
  const { sendRequest } = useAPI();
  const [operationMode, setOperationMode] = useState<MapOperatingMode>(
    MapOperatingMode.vizualizing
  ); // ["visualizing", "add-location", "add-route"]
  const [selectedNodes, setSelectedNodes] = useState<SimLocation[]>([]); // [node1, node2]
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng]

  useEffect(() => {
    sendRequest(`/simulations/${id}`, "GET").then((data) => {
      setSimulation(data);

      // set the map center
      setMapCenter(calcMapCenter(data.locations));

      console.log("useEffect");
    });
  }, []);

  function MapClickHandler(): null {
    useMapEvent("click", (event) => {
      // Access the clicked coordinates
      const { lat, lng } = event.latlng;

      //if operation mode is add-location
      if (operationMode === MapOperatingMode.adding_location) {
        // add a new node to the data
        const newNode: SimLocation = {
          name: "New Node",
          latitude: lat,
          longitude: lng,
          population: 1000000,
          region: "New Region",
          country: "New Country",
          location_type: LocationType.camp,
        };

        const newLocations = [...simulation.locations];
        newLocations.push(newNode);
        setSimulation({ ...simulation, locations: newLocations });

        // reset operation mode
        setOperationMode(MapOperatingMode.vizualizing);
      }
    });
    return null;
  }

  function NodeClickHandler(location: SimLocation): void {
    if (
      selectedNodes.length < 2 &&
      operationMode === MapOperatingMode.adding_route
    ) {
      setSelectedNodes([...selectedNodes, location]);
      console.log(selectedNodes);

      // if there are already 2 nodes selected
      if (selectedNodes.length === 1) {
        // add a new route to the data
        const newRoute = {
          from: selectedNodes[0].name,
          to: location.name,
          distance: 100,
        };

        const newRoutes = [...simulation.routes];
        newRoutes.push(newRoute);
        setSimulation({ ...simulation, routes: newRoutes });

        // reset operation mode
        setOperationMode(MapOperatingMode.vizualizing);
        setSelectedNodes([]);
      }
    }
  }

  // get the simulation data

  if (!simulation) {
    return <div>Loading...</div>;
  }

  return (
    <div className="content-page add-input-container">
      <h1>Edit Simulation: {simulation.region}</h1>

      <div className="map-content-container add-input-section">
        <h2 className="add-input-section-title">Locations & Routes</h2>
        <h4>Mode: {operationMode}</h4>
        <Map
          input={simulation}
          center={mapCenter}
          MapClickHandler={MapClickHandler}
          NodeClickHandler={NodeClickHandler}
        />
        <div className="map-content-buttons">
          <Button
            variant="contained"
            sx={{ width: "200px" }}
            onClick={() => {
              setOperationMode(MapOperatingMode.adding_location);
            }}
          >
            Add Location
          </Button>
          <Button
            variant="contained"
            sx={{ width: "200px" }}
            onClick={() => {
              setOperationMode(MapOperatingMode.adding_route);
            }}
          >
            Add Route
          </Button>
        </div>
      </div>
    </div>
  );
}

export default AddInput;
