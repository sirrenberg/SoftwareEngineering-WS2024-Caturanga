import "../styles/Map.css";
import {
  MapContainer,
  TileLayer,
  Popup,
  Circle,
  Polyline,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import {
  LocationType,
  SimLocation,
  Input,
  Route,
  MapInputType,
  validationData,
} from "../types";
import { LatLngExpression } from "leaflet";
import { useMap } from "react-leaflet/hooks";
import { useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { prettifyLocationTypeName, getLocationTypeColor } from "../helper/misc";

function Map({
  input,
  center,
  MapClickHandler,
  NodeClickHandler,
  NodeDoubleClickHandler,
  RouteDoubleClickHandler,
  shouldRecenter,
  mapMode,
  validationData,
}: {
  input?: Input;
  center?: LatLngExpression;
  MapClickHandler?: () => null;
  NodeClickHandler?: (location: SimLocation) => void;
  NodeDoubleClickHandler?: (location: SimLocation) => void;
  RouteDoubleClickHandler?: (route: Route) => void;
  shouldRecenter?: boolean;
  mapMode?: string;
  validationData?: validationData[];
}) {
  const zoomLevel = 5;

  function Recenter() {
    if (!shouldRecenter) {
      return null;
    }

    const map = useMap();

    if (!center) {
      return null;
    }

    useEffect(() => {
      map.flyTo(center, zoomLevel, { duration: 1 });
    }, [center]);

    return null;
  }

  function calculateSize(input: number | undefined) {
    if (!input) {
      return 5000;
    }

    if (mapMode === MapInputType.results) {
      return 5000 + input;
    } else {
      return 5000 + input / 10;
    }
  }

  // if no click handlers are passed
  if (!MapClickHandler) {
    MapClickHandler = () => null;
  }

  return (
    <div className="map-background">
      <MapContainer
        center={center}
        zoom={zoomLevel}
        // scrollWheelZoom={false}
        doubleClickZoom={false}
      >
        <MapClickHandler />
        <Recenter />
        {/* Add a tile layer */}
        {/* GOOGLE MAPS TILES */}
        <TileLayer
          attribution="Google Maps"
          url="http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}" // terrain
          maxZoom={20}
          subdomains={["mt0", "mt1", "mt2", "mt3"]}
        />

        {/* Add locations */}
        {input?.locations.map((location) => {
          return (
            <Circle
              key={uuidv4()}
              center={[location.latitude, location.longitude]}
              radius={calculateSize(
                mapMode === MapInputType.results
                  ? location.idp_population
                  : location.population
              )}
              color={getLocationTypeColor(location.location_type)}
              eventHandlers={{
                click: () => {
                  if (NodeClickHandler) {
                    NodeClickHandler(location);
                  }
                },
                dblclick: () => {
                  if (NodeDoubleClickHandler) {
                    NodeDoubleClickHandler(location);
                  }
                },
              }}
            >
              <Popup>
                <strong>{location.name}</strong>
                <br />
                Type: {prettifyLocationTypeName(location.location_type)}
                <br />
                Initial Population:{" "}
                {location.population === 0 ? "N/A" : location.population}
                <br />
                {mapMode === MapInputType.results ? (
                  <>
                    Simulated IDP Count:{" "}
                    {location.idp_population === 0
                      ? "N/A"
                      : location.idp_population}
                  </>
                ) : null}
                {validationData &&
                  location.location_type === LocationType.camp && (
                    <>
                      <br />
                      Validation Data:{" "}
                      {
                        validationData.find(
                          (data) => data.camp_name === location.name
                        )?.refugee_numbers
                      }
                    </>
                  )}
              </Popup>
            </Circle>
          );
        })}

        {/* Add routes */}
        {input?.routes.map((route) => {
          // search for from and to locations
          const fromLocation = input.locations.find(
            (location) => location.name === route.from
          );

          const toLocation = input.locations.find(
            (location) => location.name === route.to
          );

          // should not happen
          if (!fromLocation || !toLocation) {
            return null;
          }

          return (
            <Polyline
              key={uuidv4()}
              positions={[
                [fromLocation.latitude, fromLocation.longitude],
                [toLocation.latitude, toLocation.longitude],
              ]}
              eventHandlers={{
                dblclick: () => {
                  if (RouteDoubleClickHandler) {
                    RouteDoubleClickHandler(route);
                  }
                },
              }}
            >
              <Popup>
                <strong>{fromLocation.name}</strong> to{" "}
                <strong>{toLocation.name}</strong>: {route.distance} km
              </Popup>
            </Polyline>
          );
        })}
      </MapContainer>
    </div>
  );
}

export default Map;
