enum LocationType {
  conflict_zone = "Conflict Zone",
  town = "Town",
  forwarding_hub = "Forwarding Hub",
  camp = "Camp",
}

enum MapOperatingMode {
  vizualizing = "Vizualizing",
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

interface Simulation {
  _id: string;
  region: string;
  locations: SimLocation[];
  routes: Route[];
}

export type { SimLocation, Route, Simulation };
export { LocationType, MapOperatingMode };
