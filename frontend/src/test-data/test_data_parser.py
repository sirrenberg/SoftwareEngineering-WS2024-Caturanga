import csv

countries = ['burundi', 'car', 'ethiopia', 'mali', 'ssudan']

def parse_csv(input_file):
    data = []
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


input_file = "your_input_file.csv"
output_file = "data.ts"

with open(output_file, 'w') as tsfile:
  tsfile.write('export const simulationData: Simulation[] = [\n')
  
  for country in countries:
    tsfile.write('  {\n')
    tsfile.write(f'    name: Country.{country},\n')

    locations = parse_csv(f'{country}/locations.csv')
    tsfile.write('    locations: [\n')

    for row in locations:
      tsfile.write('      {\n')

      for field, value in row.items():
        if field == '#name':
          field = 'name'
        if field == 'lat':
          field = 'latitude'
        if field == 'lon':
          field = 'longitude'
        if field == 'location_type':
          value = f'LocationType.{value}'

        if field in ['name', 'region', 'country']:
          value = f'"{value}"'

        if value:
          tsfile.write(f'        {field}: {value},\n')

      tsfile.write('      },\n')
    tsfile.write('    ],\n')

    routes = parse_csv(f'{country}/routes.csv')
    tsfile.write('    routes: [\n')

    for row in routes:
      tsfile.write('      {\n')

      for field, value in row.items():
        if field == '#name1':
          field = 'from'
        if field == 'name2':
          field = 'to'

        if field in ['from', 'to']:
          value = f'"{value}"'

        if value:
          tsfile.write(f'        {field}: {value},\n')

      tsfile.write('      },\n')
    tsfile.write('    ],\n')

    tsfile.write('  },\n')

  tsfile.write('];\n')
  print(f'TypeScript file generated: {output_file}')
