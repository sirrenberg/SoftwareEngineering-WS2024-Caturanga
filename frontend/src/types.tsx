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
    date: string;
    length: number;
  };
}

interface ResultPreview {
  _id: string;
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
    conflict_movechance: number;
    camp_movechance: number;
    default_movechance: number;
    awareness_level: number;
    capacity_scaling: number;
    avoid_short_stints: boolean;
    start_on_foot: boolean;
    weight_power: number;
  };
  optimisations: {
    hasten: number;
  };
}

export type { SimLocation, Route, Input, SimSettings, ResultPreview };
export { LocationType, MapOperatingMode };
