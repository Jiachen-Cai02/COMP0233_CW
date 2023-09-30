from typing import Dict, List, Tuple
import math
import matplotlib.pyplot as plt

class City:

    def __init__(self, city:str, country:str, number:int, lat:float, lon:float) -> None:
        self.city = city
        self.country = country
        self.number = number
        self.lat = lat
        self.lon = lon

        if not isinstance(city, str) or city == '':
            raise ValueError('City should be string and not empty')
        
        if not isinstance(country, str) or country =='':
            raise ValueError('Country should be string and not empty')

        if not isinstance(number, int) or number < 0:
            raise ValueError('Attendee should be positive integers')

        if lat > 90 or lat < -90:
            raise ValueError('Latitude should be larger than -90 and less than 90')

        if lon > 180 or lon < -180:
            raise ValueError('Longitude should be larger than -180 and less than 180')   

    def distance_to(self, other: 'City') -> float:
        lat_diff = math.radians((self.lat - other.lat)/2)
        lon_diff = math.radians((self.lon - other.lon)/2)
        d = 2 * 6371 * math.asin(math.sqrt((math.sin(lat_diff))**2 + math.cos(math.radians(self.lat)) * math.cos(math.radians(other.lat)) * (math.sin(lon_diff))**2))
        return d
        

    def co2_to(self, other: 'City') -> float:
        d = self.distance_to(other)
        if d <= 1000:
            emit = 200 * d * self.number
        elif d > 1000 and d <= 8000:
            emit = 250 * d * self.number
        elif d > 8000:
            emit = 300 * d * self.number
        
        return emit
        


class CityCollection:
    ...
    def __init__(self, cities:list[City]) -> None:
        self.cities = cities

    def countries(self) -> List[str]:
        countries_collection = []
        for city in self.cities:
            if city.country not in countries_collection:
                countries_collection.append(city.country)
        return countries_collection
        

    def total_attendees(self) -> int:
        total = 0
        for city in self.cities:
            total += city.number
        return total
        

    def total_distance_travel_to(self, city: City) -> float:
        total_distance = 0
        for cit in self.cities:
            if cit.city != city.city:
                total_distance += cit.distance_to(city) * cit.number
        return total_distance
        

    def travel_by_country(self, city: City) -> Dict[str, float]:
        distance_dic = {}
        for cit in self.cities:
            if cit.city != city.city:
                distance_city = cit.distance_to(city) * cit.number
                if cit.country in distance_dic.keys():
                    distance_dic[cit.country] += distance_city
                else:
                    distance_dic[cit.country] = distance_city
        return distance_dic
        

    def total_co2(self, city: City) -> float:
        total_co2 = 0
        for cit in self.cities:
            if cit.city != city.city:
                total_co2 += cit.co2_to(city)
        return total_co2
        

    def co2_by_country(self, city: City) -> Dict[str, float]:
        co2_dic = {}
        for cit in self.cities:
            if cit.city != city.city:
                co2_city = cit.co2_to(city) * 0.001
                if cit.country in co2_dic.keys():
                    co2_dic[cit.country] += co2_city
                else:
                    co2_dic[cit.country] = co2_city
        return co2_dic
        

    def summary(self, city: City):
        print ('Host city: %s (%s)' %(city.city, city.country))
        print ('Total CO2: %d tonnes' %(self.total_co2(city)))
        print ('Total attendees travelling to %s from %d different cities: %d' %(city.city, (len(self.cities) - 1), self.total_attendees()))

        

    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        co2_country = {}
        for city in self.cities:
            co2_country[city.city] = self.total_co2(city) * 0.001
        sort = sorted(co2_country.items(), key = lambda item:item[1])
        return sort
        

    def plot_top_emitters(self, city: City, n: int, save: bool):
        co2_country = self.co2_by_country(city)
        sort = sorted(co2_country.items(), key = lambda item:item[1])
        else_co2 = 0
        i = 0
        label = []
        for n in range(n):
            plt.bar(sort[-n-1][0], sort[-n-1][1])
            label.append(sort[-n-1][0])
        while i < (len(co2_country) - n):
            else_co2 += sort[i][1]
            i += 1
        n = n+1
        name = str.lower(city.city)
        name = name.replace(' ', '_')
        label.append('Everywhere else')
        plt.bar("Everywhere else", else_co2)
        plt.title("Total emissions from each country (top %i)" %n)
        plt.xticks(range(len(label)), label, rotation = 50)
        plt.ylabel("Total emissions (tonnes CO2)")
        if save:
            plt.savefig(name, bbox_inches = 'tight')
        else:
            plt.show()

        

