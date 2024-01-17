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
  validationDataByDate,
  validationData,
} from "../types";
import { LatLngExpression } from "leaflet";
import Slider from "@mui/material/Slider";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPlay,
  faPause,
  faInfo,
  faMapLocationDot,
} from "@fortawesome/free-solid-svg-icons";
import { Colors } from "../helper/constants/DesignConstants";
import DataSourceModal from "../components/DataSourceModal";
import MapLegendModal from "../components/MapLegendModal";

// Page for showing details of a result
function ResultDetails() {
  const { sendRequest } = useAPI();
  const { id } = useParams<{ id: string }>();
  const [input, setInput] = useState<Input | undefined>(undefined);
  const [result, setResult] = useState<Result | undefined>(undefined);
  const [mapCenter, _] = useState<LatLngExpression>([12.6, 37.4667]); // [lat, lng]
  const [playSimulationIndex, setPlaySimulationIndex] = useState<number>(0);
  const [playingSimulation, setPlayingSimulation] = useState(false);
  const [isDataSourceModal, setDataSourceModal] = useState(false);
  const [isMapLegendModal, setMapLegendModal] = useState(false);
  const [validationMarks, setValidationMarks] = useState<
    {
      value: number;
      label: string;
    }[]
  >([]);
  const [validationData, setValidationData] = useState<validationDataByDate>(
    {}
  );

  // fetch result and corresponding input
  useEffect(() => {
    sendRequest(`/simulation_results/${id}`, "GET").then(
      (resultData: Result) => {
        setResult(resultData);
        sendRequest(`/simulations/${resultData.simulation_id}`, "GET").then(
          (inputData: Input) => {
            setInput(inputData);

            formatValidationData(inputData);
          }
        );
      }
    );
  }, []);

  function formatValidationData(input: Input) {
    // organize data by date
    const dataByDate = organizeDataByDate(input);

    // get validation dates
    const validationDates = Object.keys(dataByDate);

    // get index of validation date (comparing with start date)
    const validationDateIndexes = validationDates.map((date) => {
      return getDifferenceBetweenDates(date, input.sim_period.date);
    });

    // create marks
    const marks = validationDates.map((date, index) => {
      return {
        value: validationDateIndexes[index],
        label: date.slice(0, 10),
      };
    });

    // set marks
    setValidationMarks(marks);

    // create validationData
    setValidationData(dataByDate);
  }

  function organizeDataByDate(input: Input) {
    let organizedData: validationDataByDate = {};

    for (let campFileName in input.validation.camps) {
      let campRecords = input.validation.camps[campFileName];
      let campName = campFileName.replace(".csv", "").split("-")[1];

      campRecords.forEach((record) => {
        let date = record.date.slice(0, 10);
        let refugeeNumbers = record.refugee_numbers;

        if (!organizedData[date]) {
          organizedData[date] = [];
        }

        organizedData[date].push({
          camp_name: campName,
          refugee_numbers: refugeeNumbers,
        });
      });
    }

    return organizedData;
  }

  // get difference between two dates in days
  function getDifferenceBetweenDates(date1: string, date2: string): number {
    const dateDiff = new Date(date1).getTime() - new Date(date2).getTime();
    const dayDiff = Math.floor(dateDiff / (1000 * 3600 * 24));

    // add 1 to dayDiff because the first day is 0
    return dayDiff + 1;
  }

  // return validation data for map if available for current date (otherwise undefined)
  function getValidationDataForMap(): validationData[] | undefined {
    const currentDate = result?.data[playSimulationIndex]["Date"] as unknown;

    // get validation data for currentDate
    const validationDataForCurrentDate = validationData[currentDate as string];

    return validationDataForCurrentDate;
  }

  function handleSliderChange(_: any, newValue: number | number[]) {
    setPlaySimulationIndex(newValue as number);
  }

  // format input for map
  // (add idp_population to locations and change location_type if conflict has started)
  function formatMapInput(): Input | undefined {
    if (!input || !result || !result?.data) {
      return undefined;
    }

    // get location type based on whether conflict has started in input
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

    // Add idp_population to locations and change location_type if conflict has started
    const inputForMap: Input = {
      ...input,
      locations: input.locations.map((inputLocation) => {
        for (const key in result?.data[playSimulationIndex]) {
          if (result?.data[playSimulationIndex].hasOwnProperty(key)) {
            if (key.includes(inputLocation.name)) {
              return {
                ...inputLocation,
                idp_population: result?.data[playSimulationIndex][key],
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
      <h1 className="page-title">
        {result && input ? result.name : "Loading..."}
      </h1>

      <div className="result-map-container">
        {result?.data && input && (
          <p className="day-label">
            Day {playSimulationIndex}:{" "}
            {result?.data[playSimulationIndex]["Date"]}
          </p>
        )}

        <Map
          center={mapCenter}
          shouldRecenter={false}
          input={formatMapInput()}
          mapMode={MapInputType.results}
          validationData={getValidationDataForMap()}
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
            marks={validationMarks}
            max={result?.data?.length ? result?.data.length - 1 : 0}
            sx={{
              width: "50%",
              marginTop: "20px",
              color: Colors.light_orange,
              "& .MuiSlider-thumb": {
                backgroundColor: Colors.dark_orange,
              },
            }}
          />
        </div>
      </div>

      {input && (
        <>
          <div
            className="simple-button info-button"
            id="sources-button"
            onClick={() => {
              setDataSourceModal(true);
            }}
          >
            <FontAwesomeIcon icon={faInfo} className="sources-icon" />
          </div>
          <div
            className="simple-button info-button"
            id="map-legend-button"
            onClick={() => {
              setMapLegendModal(true);
            }}
          >
            <FontAwesomeIcon
              icon={faMapLocationDot}
              className="map-legend-icon"
            />
          </div>
        </>
      )}

      {isMapLegendModal && (
        <MapLegendModal
          setMapLegendModalOpen={setMapLegendModal}
          mapInputType={MapInputType.results}
        />
      )}

      {isDataSourceModal && input && (
        <DataSourceModal
          setDataSourceModalOpen={setDataSourceModal}
          acled_url={input.data_sources.acled.url}
          acled_last_update_date={input.data_sources.acled.last_update}
          population_url={input.data_sources.population.url}
          population_last_update_date={
            input.data_sources.population.latest_population_date
          }
          camp_url={input.data_sources.camps.url_from_last_update}
          camp_last_update_date={input.data_sources.camps.last_update}
        />
      )}
    </div>
  );
}

export default ResultDetails;
