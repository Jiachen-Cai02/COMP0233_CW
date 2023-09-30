from cities import City, CityCollection
from pathlib import Path
import csv
from cities import City, CityCollection

file_path = Path("attendee_locations.csv")

def read_attendees_file(filepath: Path) -> CityCollection:
    data = []
    city_list = []
    csv_reader = csv.DictReader(open(filepath))
    for line in csv_reader:
        data.append(line)
    for n in range(len(data)):
        city_list.append(City(data[n]['city'], data[n]['country'], int(data[n]['N']), float(data[n]['lat']), float(data[n]['lon'])))
    city_collection = CityCollection(city_list)
    return city_collection
