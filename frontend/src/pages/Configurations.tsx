import "../styles/Configurations.css";
import "leaflet/dist/leaflet.css";
import {
  MapContainer,
  TileLayer,
  Popup,
  Circle,
  Polyline,
} from "react-leaflet";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import { simulationData } from "../test-data/data";
import { useState } from "react";
import { ListItemButton, ListItemText, Button } from "@mui/material";
import { useMapEvent } from "react-leaflet/hooks";
import {
  MapOperatingMode,
  Simulation,
  SimLocation,
  LocationType,
} from "../types";

// TODO: center the map around the biggest location
// TODO: create a component for the map

function Configurations() {
  const [configs, setConfigs] = useState<Simulation[]>(simulationData);

  const [selectedConfigIndex, setSelectedConfigIndex] = useState<number>(0);
  const [operationMode, setOperationMode] = useState<MapOperatingMode>(
    MapOperatingMode.vizualizing
  ); // ["visualizing", "add-location", "add-route"]
  const [selectedNodes, setSelectedNodes] = useState<SimLocation[]>([]); // [node1, node2

  function ClickHandler() {
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

        const newConfigs = [...configs];
        newConfigs[selectedConfigIndex].locations.push(newNode);
        setConfigs(newConfigs);

        // reset operation mode
        setOperationMode(MapOperatingMode.vizualizing);
      }
    });
    return null;
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
        <MapContainer
          center={[14, 40]}
          zoom={5}
          // scrollWheelZoom={false}
          doubleClickZoom={false}
        >
          <ClickHandler />
          {/* OPEN STREEN MAPS TILES */}
          {/* <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          /> */}
          {/* WATERCOLOR CUSTOM TILES */}
          {/* <TileLayer
            attribution='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg"
          /> */}
          {/* GOOGLE MAPS TILES */}
          <TileLayer
            attribution="Google Maps"
            url="http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}" // regular
            // url="http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}" // satellite
            // url="http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}" // terrain
            maxZoom={20}
            subdomains={["mt0", "mt1", "mt2", "mt3"]}
          />

          {/* Add locations */}
          {configs[selectedConfigIndex].locations.map((location) => {
            return (
              <Circle
                center={[location.latitude, location.longitude]}
                radius={location.population ? location.population / 100 : 10000}
                eventHandlers={{
                  click: () => {
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
                  },
                }}
              >
                <Popup>
                  {location.name}: {location.population}
                </Popup>
              </Circle>
            );
          })}

          {/* Add routes */}
          {configs[selectedConfigIndex].routes.map((route) => {
            // search for from and to locations
            const fromLocation = configs[selectedConfigIndex].locations.find(
              (location) => location.name === route.from
            );

            const toLocation = configs[selectedConfigIndex].locations.find(
              (location) => location.name === route.to
            );

            // should not happen
            if (!fromLocation || !toLocation) {
              return null;
            }

            return (
              <Polyline
                positions={[
                  [fromLocation.latitude, fromLocation.longitude],
                  [toLocation.latitude, toLocation.longitude],
                ]}
              >
                <Popup>
                  {fromLocation.name} to {toLocation.name}: {route.distance} km
                </Popup>
              </Polyline>
            );
          })}
        </MapContainer>

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
