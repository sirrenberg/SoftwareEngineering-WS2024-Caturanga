# Input creation for FLEE simulations

## Preliminary remarks 
In order to use the input data for FLEE, they have to be provided as CSV files. Additionally, they get stored in the database in the correct format.
Build the image and start the docker container.
The main script which starts the extraction is run_data_extraction.py.
You can either manually start it from the terminal and pass (additional) arguments or use the API-endpoint.
In our case we have the validation data for Ethiopia available to extract camp information from.

## Process
The following is executed automatically:\
1. A unique folder is created where the input files (for the simulation) get stored.
2. Get the conflict data from the ACLED API for a country. Additionally create a CSV file (acled.csv)
3. Get the latest population data for the country and store in population.csv
4. The locations are extracted from the ACLED data and store them in locations.csv. They consist of towns and conflict zones.
5. Camps are extracted from Excel files from IOM. They are added to the locations.csv.
6. & 7. extract specific conflict data from acled.csv and create the file conflict_info.csv. With this, we create the file conflicts.csv which has all conflict locations from acled.csv as columns and the rows as days. When the conflict starts, the value changes from 0 to 1.
8. Create the shortest direct routes between locations.
9. Create an empty closures.csv file. This is necessary for FLEE to run but not relevant in our case because we just cover IDP movements.
10. Create an empty registration_correction.csv file. This is necessary for FLEE to run the simulation.
11. Create sim_period.csv with the start date (earliest data fetching date) and the duration of the simulation.
12. Create validation data for the camps.
13. Insert all data into our database so that the frontend can access it.