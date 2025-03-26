"""
This script manages the construction of "card" objects, used by players during the game.
The cards are mainly divided into 3 types:

- Property
- Station
- Corporation

Each class corresponding to a card type contains a main method called get_attributes,
which is used to extract the specific information related to each card.

Written by: Roberto Parodo
"""
class Property(object):
    def __init__(self, name, rent, house_1, house_2, house_3, house_4, hotel, house_cost, mortgage_value, color, position, cost, path, retro):
        self.name = name
        self.rent = rent
        self.house_1 = house_1
        self.house_2 = house_2
        self.house_3 = house_3
        self.house_4 = house_4
        self.hotel = hotel
        self.house_cost = house_cost
        self.mortgage_value = mortgage_value
        self.color = color
        self.position = position
        self.cost = cost
        self.path = path
        self.retro = retro

    def get_attributes(self) -> dict:
        return {
            "name": self.name,
            "rent": self.rent,
            "house_1": self.house_1,
            "house_2": self.house_2,
            "house_3": self.house_3,
            "house_4": self.house_4,
            "hotel": self.hotel,
            "house_cost": self.house_cost,
            "mortgage_value": self.mortgage_value,
            "color": self.color,
            "position": self.position,
            "cost": self.cost,
            "path": self.path,
            "retro": self.retro
        }

class Station(object):
    def __init__(self, name, rent, station_2, station_3, station_4, mortgage_value, position, cost, path, color, retro):
        self.name = name
        self.rent = rent
        self.station_2 = station_2
        self.station_3 = station_3
        self.station_4 = station_4
        self.mortgage_value = mortgage_value
        self.position = position
        self.cost = cost
        self.path = path
        self.color = color
        self.retro = retro

    def get_attributes(self) -> dict:
        return {
            "name": self.name,
            "rent": self.rent,
            "station_2": self.station_2,
            "station_3": self.station_3,
            "station_4": self.station_4,
            "mortgage_value": self.mortgage_value,
            "position": self.position,
            "cost": self.cost,
            "path": self.path,
            "color": self.color,
            "retro": self.retro
        }

class Corporation(object):
    def __init__(self,name, rent, corporation_2, mortgage_value, position, cost, path, color, retro):
        self.name = name
        self.rent = rent
        self.corporation_2 = corporation_2
        self.mortgage_value = mortgage_value
        self.position = position
        self.cost = cost
        self.path = path
        self.color = color
        self.retro = retro

    def get_attributes(self) -> dict:
        return {
            "name": self.name,
            "rent": self.rent,
            "corporation_2": self.corporation_2,
            "mortgage_value": self.mortgage_value,
            "position": self.position,
            "cost": self.cost,
            "path": self.path,
            "color": self.color,
            "retro": self.retro
        }