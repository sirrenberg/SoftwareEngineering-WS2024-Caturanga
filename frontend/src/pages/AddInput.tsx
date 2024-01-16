import "../styles/AddInput.css";
import { useParams } from "react-router-dom";
import Map from "../components/Map";
import { useEffect, useState } from "react";
import {
  MapOperatingMode,
  Input,
  SimLocation,
  LocationType,
  Route,
} from "../types";
import { useMapEvent } from "react-leaflet/hooks";
import { LatLngExpression } from "leaflet";
import { v4 as uuidv4 } from "uuid";
import { useForm } from "../hooks/useForm";
import { calcMapCenter, formatDate } from "../helper/misc";
import LocationModal from "../components/LocationModal";
import RouteModal from "../components/RouteModal";

function AddInput() {
  const { id } = useParams<{ id: string }>();

  const isNewInput = id === "new";

  const initialValues: Input = {
    region: "",
    sim_period: {
      date: new Date().toISOString().slice(0, 10),
      length: 0,
    },
    locations: [],
    routes: [],
    name: "",
    _id: "",
    conflicts: [],
    data_sources: {
      acled: {
        url: "",
        last_update: "",
      },
      population: {
        url: "",
        latest_population_date: "",
      },
      camps: {
        url_from_last_update: "",
        last_update: "",
      },
    },
  };

  const {
    values,
    setValues,
    handleInputChange,
    handlePrefillData,
    handleSubmit,
  } = useForm(initialValues);

  const [operationMode, setOperationMode] = useState<MapOperatingMode>(
    MapOperatingMode.vizualizing
  ); // ["visualizing", "add-location", "add-route"]
  const [selectedNode, setSelectedNode] = useState<SimLocation | null>(null);
  const [selectedRoute, setSelectedRoute] = useState<Route | null>(null);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>(
    calcMapCenter(values.locations)
  ); // [lat, lng]

  // use state for modal
  const [isLocationModalOpen, setLocationModalOpen] = useState(false);
  const [isRouteModalOpen, setRouteModalOpen] = useState(false);

  useEffect(() => {
    if (!isNewInput) {
      handlePrefillData(`/simulations/${id}`);
    }

    if (values.locations.length > 0) {
      setMapCenter(calcMapCenter(values.locations));
    }
  }, []);

  function MapClickHandler(): null {
    useMapEvent("click", (event) => {
      // Access the clicked coordinates
      const { lat, lng } = event.latlng;

      //if operation mode is add-location
      if (operationMode === MapOperatingMode.adding_location) {
        // add a new node to the data
        const newNode: SimLocation = {
          name: "New Node" + uuidv4(),
          latitude: lat,
          longitude: lng,
          population: 1000000,
          region: "New Region",
          country: "New Country",
          location_type: LocationType.camp,
        };

        const newLocations = [...values.locations];
        newLocations.push(newNode);
        setValues({ ...values, locations: newLocations });

        // reset operation mode
        setOperationMode(MapOperatingMode.vizualizing);
      }
    });
    return null;
  }

  function NodeClickHandler(location: SimLocation): void {
    if (operationMode === MapOperatingMode.adding_route) {
      if (selectedNode === null) {
        setSelectedNode(location);
      }
      // already 1 node selected
      else {
        const newRoute = {
          from: selectedNode.name,
          to: location.name,
          distance: 100,
        };

        const newRoutes = [...values.routes];
        newRoutes.push(newRoute);
        setValues({ ...values, routes: newRoutes });

        // reset operation mode
        setOperationMode(MapOperatingMode.vizualizing);
        setSelectedNode(null);
      }
    }
  }

  function NodeDoubleClickHandler(location: SimLocation): void {
    // open modal
    setSelectedNode(location);
    setLocationModalOpen(true);
  }

  function RouteDoubleClickHandler(route: Route): void {
    // open modal
    setSelectedRoute(route);
    setRouteModalOpen(true);
  }

  // if editing existing input and data is not loaded yet
  if (!isNewInput && values._id === "") {
    return <div>Loading...</div>;
  }

  return (
    <div className="add-input-container content-page">
      <h1 className="page-title">
        {isNewInput ? "New Input: " : "Edit Input: "}
        {values.region}
      </h1>

      <div className="duration-container add-input-section">
        <h2 className="page-subtitle">Name & Region</h2>
        <div className="name-fields-container fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Name: <br />
              <input
                className="input-field"
                type="text"
                placeholder="Input Name"
                onChange={handleInputChange}
                name="name"
                value={values.name}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Region: <br />
              <input
                className="input-field"
                type="text"
                placeholder="Region"
                onChange={handleInputChange}
                name="region"
                value={values.region}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="sim-period-container add-input-section">
        <h2 className="page-subtitle">Simulation Period</h2>

        <div className="sim-period-fields-container fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Start Date: <br />
              <input
                className="input-field"
                type="date"
                placeholder="Start Date"
                onChange={handleInputChange}
                name="date"
                value={formatDate(values.sim_period["date"])}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Duration: <br />
              <input
                className="input-field"
                type="number"
                placeholder="Duration"
                onChange={handleInputChange}
                name="length"
                min={1}
                max={800}
                value={values.sim_period["length"]}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="map-content-container add-input-section">
        <h2 className="page-subtitle">Locations & Routes</h2>
        <h4>Mode: {operationMode}</h4>
        <Map
          input={values}
          center={mapCenter}
          MapClickHandler={MapClickHandler}
          NodeClickHandler={NodeClickHandler}
          NodeDoubleClickHandler={NodeDoubleClickHandler}
          RouteDoubleClickHandler={RouteDoubleClickHandler}
        />
        <div className="map-content-buttons">
          <button
            className="simple-button"
            onClick={() => {
              setOperationMode(MapOperatingMode.adding_location);
            }}
          >
            Add Location
          </button>
          <button
            className="simple-button"
            onClick={() => {
              setOperationMode(MapOperatingMode.adding_route);
              setSelectedNode(null);
            }}
          >
            Add Route
          </button>
        </div>
      </div>

      <div className="add-input-section">
        <h2 className="page-subtitle">Conflicts</h2>

        {/* create conflict table */}
        <table className="conflict-table">
          <thead>
            <tr>
              <th>Location</th>
              <th> Start Date</th>
              <th> End Date</th>
              <th>Intensity</th>
            </tr>
          </thead>
          <tbody>
            {values.locations.map((location: SimLocation) => {
              return (
                <tr>
                  <td>{location.name}</td>
                  <td>
                    <input type="date" />
                  </td>
                  <td>
                    <input type="date" />
                  </td>
                  <td>
                    <input type="number" />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="submit-button-container add-input-section">
        <button
          className="simple-button"
          onClick={(e) => {
            handleSubmit(e, "/inputs/", "POST");
          }}
        >
          Save
        </button>
      </div>

      {isLocationModalOpen && (
        <LocationModal
          location={selectedNode}
          setLocationModalOpen={setLocationModalOpen}
          setSimValues={setValues}
          simValues={values}
        />
      )}

      {isRouteModalOpen && (
        <RouteModal
          route={selectedRoute}
          setRouteModalOpen={setRouteModalOpen}
          setSimValues={setValues}
          simValues={values}
        />
      )}
    </div>
  );
}

export default AddInput;
