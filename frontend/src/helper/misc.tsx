import { SimLocation, LocationType } from "../types";
import { LatLngExpression } from "leaflet";
import { Colors } from "../helper/constants/DesignConstants";

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

function pretifyLocationName(locationName: string): string {
  switch (locationName) {
    case LocationType.camp:
      return "Camp";
    case LocationType.town:
      return "Town";
    case LocationType.conflict_zone:
      return "Conflict Zone";
    default:
      return locationName;
  }
}

function getLocationColor(locationType: LocationType) {
  // get the color of the node based on the location type
  switch (locationType) {
    case LocationType.conflict_zone:
      return Colors.medium_orange;
    case LocationType.town:
      return Colors.medium_blue;
    case LocationType.forwarding_hub:
      return Colors.gray;
    case LocationType.camp:
      return Colors.medium_green;
    default:
      return "black";
  }
}

export { calcMapCenter, formatDate, pretifyLocationName, getLocationColor };
