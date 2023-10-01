from Flight import *
from Airport import *


class Aviation:
    # constructor for the Aviation class
    def __init__(self):
        self._allAirports = []
        self._allFlights = {}
        self._allCountries = {}

    # Sets the allAirports list
    def setAllAirports(self, airports):
        self._allAirports = airports

    # Sets the allFlights dictionary
    def setAllFlights(self,flights):
        self._allFlights = flights

    # Sets the allCountries dictionary
    def setAllCountries(self, countries):
        self._allCountries = countries

    # Gets the allAirports list
    def getAllAirports(self):
        return self._allAirports

    # Gets the allFlights dictionary
    def getAllFlights(self):
        return self._allFlights

    # Gets the allCountries dictionary
    def getAllCountries(self):
        return self._allCountries


    # Loads in the data from the airport, flight, and country files into their respective lists and dictionaries
    def loadData(self, airportFile, flightFile, countriesFile):
        try:
            # Read the countries file and adds each line as its own dictionary entry
            f = open(countriesFile, "r", encoding='utf8')
            self._allCountries = {}
            for line in f:
                parts = line.split(',')
                country = parts[0].strip()
                continent = parts[1].strip()
                self._allCountries[country] = continent
            f.close()

            # Read the airport file and adds each line as its own airport object to a list
            f = open(airportFile, "r", encoding='utf8')
            self._allAirports= []
            for line in f:
                parts = line.split(',')
                code = parts[0].strip()
                country = parts[1].strip()
                city = parts[2].strip()
                continent = self._allCountries[country]
                self._allAirports.append(Airport(code, city, country, continent))
            f.close()

            # Read the flight file and adds each line as its own airport object to a dictionary, sorted by origin
            f = open(flightFile, "r", encoding='utf8')
            self._allFlights = {}
            for line in f:
                parts = line.split(',')
                flightNo = parts[0].strip()
                origCode = parts[1].strip()
                destCode = parts[2].strip()

                # finds corresponding airport objects (origin + destination of flight)
                for airport in self._allAirports:
                    if airport.getCode() == origCode:
                        origAirport = airport
                    if airport.getCode() == destCode:
                        destAirport = airport
    
                newFlight = Flight(flightNo, origAirport, destAirport)
                # adds to dictionary, sorted by origin airport
                if origAirport in self._allFlights.keys(): 
                    self._allFlights[origAirport].append(newFlight)
                else:
                    self._allFlights[origAirport] = [newFlight]
            f.close()

        except: # error handling if a filename is incorrect
            return False
        return True

    # Returns the airport object with the input code
    def getAirportByCode(self, code):
        for airport in self._allAirports:
            if code == airport.getCode():
                return airport
        return -1

    # Returns a list all flights in or out of a city
    def findAllCityFlights(self, city):
        allCityFlights = []
        for flight in self._allFlights.values():
            for value in flight:
                if city in value.getOrigin().getCity():
                    allCityFlights.append(value)
                elif city in value.getDestination().getCity():
                    allCityFlights.append(value)
                    
        return allCityFlights

    # Returns a flight belonging to the input number
    def findFlightByNo(self, flightNo):
        for flights in self._allFlights.values():
            for flight in flights:
                if flight.getFlightNumber() == flightNo:
                    return flight
        return -1

    # # Returns a list all flights in or out of a country
    def findAllCountryFlights(self, country):
        allCountryFlights = []
        for flight in self._allFlights.values():
            for value in flight:
                if country in value.getOrigin().getCountry():
                    allCountryFlights.append(value)
                if country in value.getDestination().getCountry():
                    allCountryFlights.append(value)
        return allCountryFlights

    # Returns a flight, or connection flights, between two destinations
    def findFlightBetween(self, origAirport, destAirport):
        # Returns a direct flight statement, if a direct flight is available between the origin and destination
        for flight in self._allFlights.values():
            for value in flight:
                if origAirport.getCode() in value.getOrigin().getCode() and destAirport.getCode() in value.getDestination().getCode():
                    return (f"Direct Flight({value.getFlightNumber()}): {origAirport.getCode()} to {destAirport.getCode()}")  # .format(origAirport.getCode(), destAirport.getCode())

        #If no direct flight is available, made two lists of airports leaving from origin, and arriving to destination
        originAirports = []
        destinationAirports = []
        linkAirports = set()
        for flight in self._allFlights.values():
            for value in flight:
                if origAirport.getCode() in value.getOrigin().getCode():
                    originAirports.append(value)
                if destAirport.getCode() in value.getDestination().getCode():
                    destinationAirports.append(value)

        # Check if any of those airports have a matching midpoint, add them to the list
        for i in originAirports:
            for j in destinationAirports:
                if i.getDestination().getCode() in j.getOrigin().getCode():
                    linkAirports.add(i.getDestination().getCode())

        if len(linkAirports) != 0:
            return linkAirports

        # Returns -1 if no connecting or direct flight exists
        return -1

    # Returns a flight that has the opposite origin and destination as the input (origin of returned flight was the destination of input flight)
    def findReturnFlight(self, firstFlight):
        for flight in self._allFlights.values():
            for value in flight:
                if firstFlight.getOrigin().getCode() in value.getDestination().getCode() and firstFlight.getDestination().getCode() in value.getOrigin().getCode():
                    return value
        # Returns -1 if no return flight exists
        return -1

    # Returns a set of all flights that cross across the Pacific or Atlantic ocean, depending on input
    def findFlightsAcross(self, ocean):
        greenZone = {"United States", "Canada", "Mexico", "Brazil", "Argentina", "Colombia"}
        redZone = {"China", "Japan", "Australia", "India", "South Korea", "Philippines", "Palestine", "United Arab Emirates"}
        blueZone = {"United Kingdom", "France", "Spain", "Germany", "Italy", "South Africa", "Kenya", "Libya", "England", "Portugal"}
        flights_across = set()

        # Checks if a flight has its origin and destination in the green and red zones, or the green and blue zones, depending on input ocean
        if ocean == "Pacific":
            for flights in self._allFlights.values():
                for flight in flights:
                    if flight.getOrigin().getCountry() in greenZone and flight.getDestination().getCountry() in redZone:
                        flights_across.add(flight.getFlightNumber())
                    elif flight.getOrigin().getCountry() in redZone and flight.getDestination().getCountry() in greenZone:
                        flights_across.add(flight.getFlightNumber())
        elif ocean == "Atlantic":
            for flights in self._allFlights.values():
                for flight in flights:
                    if flight.getOrigin().getCountry() in greenZone and flight.getDestination().getCountry() in blueZone:
                        flights_across.add(flight.getFlightNumber())
                    elif flight.getOrigin().getCountry() in blueZone and flight.getDestination().getCountry() in greenZone:
                        flights_across.add(flight.getFlightNumber())

        # Returns -1 if no flights exist for that ocean
        if len(flights_across) > 0:
            return flights_across
        return -1