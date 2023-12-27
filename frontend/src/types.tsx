enum LocationType {
  conflict_zone = "Conflict Zone",
  town = "Town",
  forwarding_hub = "Forwarding Hub",
  camp = "Camp",
}

enum MapOperatingMode {
  vizualizing = "Visualizing",
  adding_location = "Adding Location",
  adding_route = "Adding Route",
}

interface SimLocation {
  // can not be called Location as that conflicts with MongoDB
  name: string;
  region: string;
  country: string;
  latitude: number;
  longitude: number;
  location_type: LocationType;
  conflict_date?: number;
  population?: number; // or capacity of camp
}

interface Route {
  from: string; // Location?
  to: string; // Location?
  distance: number;
  forced_redirection?: number;
}

interface Input {
  _id: string;
  region: string;
  locations: SimLocation[];
  routes: Route[];
  name: string;
  // TODO: Remove Array (only one sim_period)
  sim_period: {
    date: Date;
    length: number;
  }[];
}

export type { SimLocation, Route, Input };
export { LocationType, MapOperatingMode };
