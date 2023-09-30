from cities import *
#from utils import read_attendees_file
import pytest
from pathlib import Path
import csv
import math
from typing import Dict, List, Tuple

file_path = Path("attendee_locations.csv")
data = []
csv_reader = csv.reader(open(file_path))
for line in csv_reader:
    data.append(line)

citydata = data[1:]


#Test City
def test_input_city():
    with pytest.raises(ValueError) as Exception:
        City('', citydata[0][1], int(citydata[0][0]), float(citydata[0][4]), float(citydata[0][5]))
    assert str(Exception.value) ==  'City should be string and not empty'

    with pytest.raises(ValueError) as Exception:
        City(list(citydata[0][3]), citydata[0][1], int(citydata[0][0]), float(citydata[0][4]), float(citydata[0][5]))
    assert str(Exception.value) ==  'City should be string and not empty'


def test_input_country():
    with pytest.raises(ValueError) as Exception:
        City(citydata[0][3], '', int(citydata[0][0]), float(citydata[0][4]), float(citydata[0][5]))
    assert str(Exception.value) == 'Country should be string and not empty'

    with pytest.raises(ValueError) as Exception:
        City(citydata[0][3], list(citydata[0][1]), int(citydata[0][0]), float(citydata[0][4]), float(citydata[0][5]))
    assert str(Exception.value) == 'Country should be string and not empty'


def test_input_attendee():
    with pytest.raises (ValueError) as Exception:
        City(citydata[0][3], citydata[0][1], citydata[0][0], float(citydata[0][4]), float(citydata[0][5]))
    assert str(Exception.value) == 'Attendee should be positive integers'

    with pytest.raises (ValueError) as Exception: 
        City(citydata[0][3], citydata[0][1], -int(citydata[0][0]), float(citydata[0][4]), float(citydata[0][5]))
    assert str(Exception.value) == 'Attendee should be positive integers'


def test_input_latitude():
    with pytest.raises (ValueError) as Exception:
        City(citydata[0][3], citydata[0][1], int(citydata[0][0]), float(citydata[0][4]) * 1000, float(citydata[0][5]))
    assert str(Exception.value) == 'Latitude should be larger than -90 and less than 90'

def test_input_longitude():
    with pytest.raises (ValueError) as Exception:
        City(citydata[0][3], citydata[0][1], int(citydata[0][0]), float(citydata[0][4]), float(citydata[0][5]) * 10000)
    assert str(Exception.value) == 'Longitude should be larger than -180 and less than 180'

#Test Citycollection
zurich = City(citydata[889][3], citydata[889][1], int(citydata[889][0]), float(citydata[889][4]), float(citydata[889][5]))
san_francisco = City(citydata[1115][3], citydata[1115][1], int(citydata[1115][0]), float(citydata[1115][4]), float(citydata[1115][5]))
test_list = [zurich, san_francisco]
test = CityCollection(test_list)

def test_countries():
    con_list = test.countries()
    assert con_list == ['Switzerland', 'United States']

def test_total_attendees():
    total_n = test.total_attendees()
    assert total_n == 173

def test_total_distance():
    total_distance = test.total_distance_travel_to(san_francisco)
    single_distance = 2 * 6371 * math.asin(math.sqrt(math.sin(math.radians((zurich.lat - san_francisco.lat)/2)) ** 2 + math.cos(math.radians(zurich.lat)) * math.cos(math.radians(san_francisco.lat)) * math.sin(math.radians((zurich.lon - san_francisco.lon)/2))**2))
    assert total_distance == single_distance * zurich.number

def test_travel_by_country():
    travel_by_country = test.travel_by_country(san_francisco)
    assert list(travel_by_country.keys()) == ['Switzerland']
    assert list(travel_by_country.values())[0] == 2 * 6371 * math.asin(math.sqrt(math.sin(math.radians((zurich.lat - san_francisco.lat)/2)) ** 2 + math.cos(math.radians(zurich.lat)) * math.cos(math.radians(san_francisco.lat)) * math.sin(math.radians((zurich.lon - san_francisco.lon)/2))**2)) * zurich.number

def test_total_co2():
    total_co2 = test.total_co2(san_francisco)
    d = 2 * 6371 * math.asin(math.sqrt(math.sin(math.radians((zurich.lat - san_francisco.lat)/2)) ** 2 + math.cos(math.radians(zurich.lat)) * math.cos(math.radians(san_francisco.lat)) * math.sin(math.radians((zurich.lon - san_francisco.lon)/2)) **2))
    emit = 0
    if d <= 1000:
        emit = 200 * d * zurich.number
    elif d > 1000 and d <= 8000:
        emit = 250 * d * zurich.number
    elif d > 8000:
        emit = 300 * d * zurich.number
    
    emit = emit
    assert emit == total_co2

def test_co2_by_country():
    co2_by_country = test.co2_by_country(san_francisco)

    d = 2 * 6371 * math.asin(math.sqrt(math.sin(math.radians((zurich.lat - san_francisco.lat)/2)) ** 2 + math.cos(math.radians(zurich.lat)) * math.cos(math.radians(san_francisco.lat)) * math.sin(math.radians((zurich.lon - san_francisco.lon)/2))**2))
    emit = 0
    if d <= 1000:
        emit = 200 * d * zurich.number
    elif d > 1000 and d <= 8000:
        emit = 250 * d * zurich.number
    elif d > 8000:
        emit = 300 * d * zurich.number

    assert list(co2_by_country.keys()) == ['Switzerland']
    assert list(co2_by_country.values())[0] == emit * 0.001

def test_sorted_by_emissions():
    sort = test.sorted_by_emissions()

    assert sort[0][1] < sort[1][1]
    assert type(sort[0][0]) == str
    assert type(sort[1][0]) == str