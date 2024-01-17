import { SimLocation } from "../types";
import { LatLngExpression } from "leaflet";

function calcMapCenter(locations: SimLocation[]): LatLngExpression {
  // Returns the location of the biggest location

  if (locations.length === 0) {
    return [0, 0];
  }

  let maxPopulation = 0;

  let maxLocation = locations[0];
  locations.forEach((location) => {
    if (location.population && location.population > maxPopulation) {
      maxPopulation = location.population;
      maxLocation = location;
    }
  });

  return [maxLocation.latitude, maxLocation.longitude];
}

function formatDate(dateToFormat: string): string {
  if (!dateToFormat) {
    return "";
  }
  if (dateToFormat.length < 10) {
    return dateToFormat;
  }

  return dateToFormat.slice(0, 10);
}

function sliceName(name: string, cutOff: number) : string {
  // if the name is short enough, we do not have to slice it
  // we cut off if it is at least two characters too much
  if (name.length <= cutOff + 1) {
    return name;
  } else {
    return `${name.slice(0, cutOff)}...`
  }
}

export { calcMapCenter, formatDate, sliceName};
