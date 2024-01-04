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

export { calcMapCenter, formatDate };
