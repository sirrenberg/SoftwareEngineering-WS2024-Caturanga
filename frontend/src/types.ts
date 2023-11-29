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

interface Location {
  name: string;
  region: string;
  country: string;
  latitude: number;
  longitude: number;
  loaction_type: LocationType;
  conflict_date?: bigint;
  population: bigint; // or capacity of camp
}

interface Route {
  from: string; // Location?
  to: string; // Location?
  distance: bigint;
  forced_redirection?: bigint;
}

interface Simulation {
  name: Country;
  locations: Location[];
  routes: Route[]
}
