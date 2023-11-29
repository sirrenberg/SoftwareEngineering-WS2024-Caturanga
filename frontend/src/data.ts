import * as csvParser from 'csv-parser';
import * as fs from 'fs';

export default getSimulationData;

function getSimulationData(country: Country) : Simulation {
  const dataDir = 'test-data/' + country + '/';

  const locations: Location[] = [];
  fs.createReadStream(dataDir + "locations.csv")
    .pipe(csvParser())
    .on('data', (data: Location) => {
      locations.push(data);
    });

  const routes: Route[] = [];
  fs.createReadStream(dataDir + "routes.csv")
    .pipe(csvParser())
    .on('data', (data: Route) => {
      routes.push(data);
     });
  
  const simulation: Simulation = {name: country, locations: locations, routes: routes};
  console.log(simulation)
  return simulation;
}
