enum LocationType {
  conflict_zone = "conflict_zone",
  town = "town",
  forwarding_hub = "forwarding_hub",
  camp = "camp",
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

interface SimSettings {
  _id: string;
  name: string;
  log_levels: {
    agent: number;
    link: number;
    camp: number;
    conflict: number;
    init: number;
    idp_totals: number;
    granularity: string;
  };
  spawn_rules: {
    take_from_population: boolean;
    insert_day0: boolean;
  };
  move_rules: {
    max_move_speed: number;
    max_walk_speed: number;
    foreign_weight: number;
    conflict_weight: number;
    camp_weight: number;
  };
}

export type { SimLocation, Route, Input, SimSettings };
export { LocationType, MapOperatingMode };
