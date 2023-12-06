import "../styles/Configurations.css";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import { simulationData } from "../test-data/data";
import { useState } from "react";
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

// TODO: center the map around the biggest location
// TODO: create a component for the map

function Configurations() {
  const [configs, setConfigs] = useState<Simulation[]>(simulationData);
  const [selectedConfigIndex, setSelectedConfigIndex] = useState<number>(0);
  const [operationMode, setOperationMode] = useState<MapOperatingMode>(
    MapOperatingMode.vizualizing
  ); // ["visualizing", "add-location", "add-route"]
  const [selectedNodes, setSelectedNodes] = useState<SimLocation[]>([]); // [node1, node2]

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

        const newConfigs = { ...configs };
        configs[selectedConfigIndex].locations.push(newNode);
        setConfigs(newConfigs);
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

        const newConfigs = [...configs];
        newConfigs[selectedConfigIndex].routes.push(newRoute);
        setConfigs(newConfigs);

        // reset operation mode
        setOperationMode(MapOperatingMode.vizualizing);
        setSelectedNodes([]);
      }
    }
  }

  function getMapCenter(): LatLngExpression {
    // Returns the location of the biggest location
    let maxPopulation = 0;
    let maxLocation = configs[selectedConfigIndex].locations[0];
    configs[selectedConfigIndex].locations.forEach((location) => {
      if (location.population && location.population > maxPopulation) {
        maxPopulation = location.population;
        maxLocation = location;
      }
    });
    return [maxLocation.latitude, maxLocation.longitude] as LatLngExpression;
  }

  return (
    <div className="configs-container">
      <div className="configs-list-container">
        <List
          sx={{
            width: "100%",
            height: "100%",
            maxWidth: 360,
            bgcolor: "background.paper",
          }}
        >
          {configs.map((config, index) => {
            return (
              <ListItem
                button
                key={index}
                onClick={() => setSelectedConfigIndex(index)}
              >
                <ListItemButton selected={selectedConfigIndex === index}>
                  <ListItemText primary={config.name} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </div>

      <div className="map-section">
        <h2 className="selected-config-title">
          {configs[selectedConfigIndex].name}, Mode: {operationMode}
        </h2>

        <Map
          config={configs[selectedConfigIndex]}
          MapClickHandler={MapClickHandler}
          NodeClickHandler={NodeClickHandler}
          center={getMapCenter()}
        />

        <div className="buttons-container">
          <Button
            variant="contained"
            sx={{ width: "200px" }}
            onClick={() => setOperationMode(MapOperatingMode.adding_location)}
          >
            Add Location
          </Button>
          <Button
            variant="contained"
            sx={{ width: "200px" }}
            onClick={() => setOperationMode(MapOperatingMode.adding_route)}
          >
            Add Route
          </Button>
        </div>
      </div>
    </div>
  );
}

export default Configurations;
