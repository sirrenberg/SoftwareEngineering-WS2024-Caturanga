import "../styles/Inputs.css";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import { simulationData } from "../test-data/data";
import { useEffect, useState } from "react";
import { ListItemButton, ListItemText, Button } from "@mui/material";
import {
  MapOperatingMode,
  Simulation,
  SimLocation,
  LocationType,
} from "../types";
import Map from "../components/Map";
import { useMapEvent } from "react-leaflet/hooks";
import { LatLngExpression } from "leaflet";
import { Link } from "react-router-dom";

function Inputs() {
  const [inputs, setInputs] = useState<Simulation[]>(simulationData);
  const [selectedInputIndex, setSelectedInputIndex] = useState<number>(0);
  const [operationMode, setOperationMode] = useState<MapOperatingMode>(
    MapOperatingMode.vizualizing
  ); // ["visualizing", "add-location", "add-route"]
  const [selectedNodes, setSelectedNodes] = useState<SimLocation[]>([]); // [node1, node2]
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng

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

        const newInputs = [...inputs];
        newInputs[selectedInputIndex].locations.push(newNode);
        setInputs(newInputs);
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

      // if there are already 2 nodes selected
      if (selectedNodes.length === 1) {
        // add a new route to the data
        const newRoute = {
          from: selectedNodes[0].name,
          to: location.name,
          distance: 100,
        };

        const newInputs = [...inputs];
        newInputs[selectedInputIndex].routes.push(newRoute);
        setInputs(newInputs);

        // reset operation mode
        setOperationMode(MapOperatingMode.vizualizing);
        setSelectedNodes([]);
      }
    }
  }

  function calcMapCenter(): void {
    // Returns the location of the biggest location

    // if not in vizualizing mode, return
    if (operationMode !== MapOperatingMode.vizualizing) {
      return;
    }

    let maxPopulation = 0;
    let maxLocation = inputs[selectedInputIndex].locations[0];
    inputs[selectedInputIndex].locations.forEach((location) => {
      if (location.population && location.population > maxPopulation) {
        maxPopulation = location.population;
        maxLocation = location;
      }
    });
    setMapCenter([maxLocation.latitude, maxLocation.longitude]);
  }

  useEffect(() => {
    calcMapCenter();
  }, [selectedInputIndex]);

  return (
    <div className="inputs-container content-page">
      <div className="inputs-list-container">
        <List
          sx={{
            width: "100%",
            height: "100%",
            maxWidth: 360,
            bgcolor: "background.paper",
          }}
        >
          {inputs.map((input, index) => {
            return (
              <ListItem
                button
                key={index}
                onClick={() => setSelectedInputIndex(index)}
              >
                <ListItemButton selected={selectedInputIndex === index}>
                  <ListItemText primary={input.name} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </div>

      <div className="map-section">
        <h2 className="selected-input-title">
          {inputs[selectedInputIndex].name}, Mode: {operationMode}
        </h2>

        <Map
          input={inputs[selectedInputIndex]}
          MapClickHandler={MapClickHandler}
          NodeClickHandler={NodeClickHandler}
          center={mapCenter}
        />

        <div className="buttons-container">
          <Link to={"/inputs/" + inputs[selectedInputIndex].name}>
            <Button variant="contained" sx={{ width: "200px" }}>
              Edit Conflict Input
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Inputs;
