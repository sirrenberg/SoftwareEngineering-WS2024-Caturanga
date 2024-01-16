import { useParams } from "react-router-dom";
import Map from "../components/Map";
import { useEffect, useState } from "react";
import { useAPI } from "../hooks/useAPI";
import {
  Input,
  Result,
  SimLocation,
  MapInputType,
  LocationType,
} from "../types";
import { LatLngExpression } from "leaflet";
import Slider from "@mui/material/Slider";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay, faPause } from "@fortawesome/free-solid-svg-icons";
import { Colors } from "../helper/constants/DesignConstants";

function ResultDetails() {
  const { sendRequest } = useAPI();
  const { id } = useParams<{ id: string }>();
  const [input, setInput] = useState<Input | undefined>(undefined);
  const [result, setResult] = useState<Result | undefined>(undefined);
  const [mapCenter, _] = useState<LatLngExpression>([12.6, 37.4667]); // [lat, lng]
  const [playSimulationIndex, setPlaySimulationIndex] = useState<number>(0);
  const [playingSimulation, setPlayingSimulation] = useState(false);

  // fetch result and corresponding input
  useEffect(() => {
    sendRequest(`/simulation_results/${id}`, "GET").then(
      (resultData: Result) => {
        setResult(resultData);
        sendRequest(`/simulations/${resultData.simulation_id}`, "GET").then(
          (inputData: Input) => {
            setInput(inputData);
          }
        );
      }
    );
  }, []);

  function handleSliderChange(_: any, newValue: number | number[]) {
    setPlaySimulationIndex(newValue as number);
  }

  function formatMapInput(): Input | undefined {
    if (!input || !result || !result?.data) {
      return undefined;
    }

    function getLocationType(location: SimLocation): LocationType {
      if (location.location_type === LocationType.conflict_zone) {
        // check if conflict has started in input
        return input?.conflicts[playSimulationIndex][location.name] === 1
          ? LocationType.conflict_zone
          : LocationType.town;
      } else {
        return location.location_type;
      }
    }

    const inputForMap: Input = {
      ...input,
      locations: input.locations.map((inputLocation) => {
        for (const key in result?.data[playSimulationIndex]) {
          if (result?.data[playSimulationIndex].hasOwnProperty(key)) {
            if (key.includes(inputLocation.name)) {
              return {
                ...inputLocation,
                population: result?.data[playSimulationIndex][key],
                location_type: getLocationType(inputLocation),
              } as SimLocation;
            }
          }
        }
        return inputLocation;
      }),
    };

    return inputForMap;
  }

  // if playingSimulation is true, increment playSimulationIndex every 1000ms
  useEffect(() => {
    if (playingSimulation) {
      if (!result) {
        return;
      }
      const interval = setInterval(() => {
        setPlaySimulationIndex((prev) => {
          if (prev === result?.data.length - 1) {
            setPlayingSimulation(false);
            return prev;
          } else {
            return prev + 1;
          }
        });
      }, 100);
      return () => clearInterval(interval);
    }
  }, [playingSimulation]);

  return (
    <div className="content-page result-detail-container">
      <h1 className="page-title">{result ? result.name : "Loading..."}</h1>

      <div className="result-map-container">
        {result?.data && (
          <p className="day-label">
            Day: {playSimulationIndex} -{" "}
            {result?.data[playSimulationIndex]["Date"]}
          </p>
        )}

        <Map
          center={mapCenter}
          shouldRecenter={false}
          input={formatMapInput()}
          mapMode={MapInputType.results}
        />
        <div className="slider-container">
          <button
            className="play-button simple-button"
            onClick={() => {
              // if no result, do nothing
              if (!result || !result?.data) {
                return;
              }

              if (playingSimulation) {
                setPlayingSimulation(false);
              } else {
                // if playSimulationIndex is at the end, reset it to 0
                if (playSimulationIndex === result?.data.length - 1) {
                  setPlaySimulationIndex(0);
                }
                setPlayingSimulation(true);
              }
            }}
          >
            <FontAwesomeIcon
              className=""
              icon={playingSimulation ? faPause : faPlay}
            />
          </button>

          <Slider
            value={playSimulationIndex}
            onChange={handleSliderChange}
            min={0}
            max={result?.data?.length ? result?.data.length - 1 : 0}
            sx={{
              width: "50%",
              marginTop: "20px",
              color: Colors.light_orange,
              "& .MuiSlider-thumb": {
                backgroundColor: Colors.dark_orange
              },
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default ResultDetails;
