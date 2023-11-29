enum Country {
  burundi,
  car,
  ethiopia,
  mali,
  ssudan,
}

enum LocationType {
  conflict_zone,
  town,
  forwarding_hub,
  camp,
}

interface SimLocation {  // can not be called Location as that conflicts with MongoDB
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
  name: Country;
  locations: SimLocation[];
  routes: Route[]
}
