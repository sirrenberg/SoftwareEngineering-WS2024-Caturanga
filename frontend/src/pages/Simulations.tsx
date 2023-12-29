import "../styles/Menu.css";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import { useEffect, useState } from "react";
import { ListItemButton, ListItemText, Slider, Box } from "@mui/material";
import { Input } from "../types";
import Map from "../components/Map";
import { LatLngExpression } from "leaflet";
import { useAPI } from "../hooks/useAPI";
import { calcMapCenter } from "../helper/misc";

function Simulations() {
  const { sendRequest } = useAPI();

  const [inputs, setInputs] = useState<Input[]>([]);
  const [selectedInputIndex, setSelectedInputIndex] = useState<number>(0);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([0, 0]); // [lat, lng

  useEffect(() => {
    sendRequest("/simulations", "GET").then((data) => {
      setInputs(data);
    });
  }, []);

  useEffect(() => {
    if (inputs.length > 0) {
      setMapCenter(calcMapCenter(inputs[selectedInputIndex].locations));
    }
  }, []);

  if (inputs.length === 0) {
    return <div>Loading...</div>;
  }

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
                  <ListItemText primary={input.region} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </div>

      <div className="map-section">
        <h2 className="selected-input-title">
          Result: {inputs[selectedInputIndex].region}
        </h2>

        <Map input={inputs[selectedInputIndex]} center={mapCenter} />

        <div className="slider-container">
          <Box sx={{ width: 300 }}>
            <Slider valueLabelDisplay="auto" step={1} marks min={0} max={14} />
          </Box>
        </div>
      </div>
    </div>
  );
}

export default Simulations;
