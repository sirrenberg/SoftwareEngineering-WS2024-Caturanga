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
import { LatLngExpression } from "leaflet";
import { Link } from "react-router-dom";

function Inputs() {
  const [inputs, setInputs] = useState<Simulation[]>(simulationData);
  const [selectedInputIndex, setSelectedInputIndex] = useState<number>(0);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng

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
          Preview: {inputs[selectedInputIndex].name}
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
