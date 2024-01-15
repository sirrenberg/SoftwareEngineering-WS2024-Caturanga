import { useParams } from "react-router-dom";
import Map from "../components/Map";
import { useEffect, useState } from "react";
import { useAPI } from "../hooks/useAPI";
import { Input, Result, SimLocation } from "../types";
import { calcMapCenter } from "../helper/misc";
import { LatLngExpression } from "leaflet";
import Slider from "@mui/material/Slider";

function ResultDetails() {
  const { sendRequest } = useAPI();
  const { id } = useParams<{ id: string }>();
  const [input, setInput] = useState<Input | undefined>(undefined);
  const [result, setResult] = useState<Result | undefined>(undefined);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([12.6, 37.4667]); // [lat, lng]
  const [playSimulationIndex, setPlaySimulationIndex] = useState<number>(360);

  useEffect(() => {
    sendRequest(`/simulation_results/${id}`, "GET").then(
      (resultData: Result) => {
        setResult(resultData);
        sendRequest(`/simulations/${resultData.simulation_id}`, "GET").then(
          (inputData: Input) => {
            setInput(inputData);
            if (input) {
              setMapCenter(calcMapCenter(inputData.locations));
            }
          }
        );
      }
    );
  }, []);

  function handleSliderChange(event: any, newValue: number | number[]) {
    setPlaySimulationIndex(newValue as number);
  }

  function formatMapInput(): Input | undefined {
    if (!input || !result) {
      return undefined;
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
              } as SimLocation;
            }
          }
        }
        return inputLocation;
      }),
    };

    return inputForMap;
  }

  return (
    <div className="content-page result-detail-container">
      <h1 className="page-title">{result ? result.name : "Loading..."}</h1>

      <div className="result-map-container">
        <p>
          Day: {playSimulationIndex} -{" "}
          {result?.data[playSimulationIndex]["Date"]}
        </p>

        <Map
          center={mapCenter}
          shouldRecenter={false}
          input={formatMapInput()}
        />

        <Slider
          value={playSimulationIndex}
          onChange={handleSliderChange}
          min={0}
          max={result?.data.length ? result?.data.length - 1 : 0}
          sx={{
            width: "50%",
            marginTop: "20px",
            color: "#f3b391", // Change the color here
            "& .MuiSlider-thumb": {
              backgroundColor: "#f15025", // Change the thumb color here
            },
          }}
        />
      </div>
    </div>
  );
}

export default ResultDetails;
