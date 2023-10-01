from Airport import *


class Flight:
    # Constructor for the flight class
    def __init__(self, flightNo, origAirport, destAirport):
        # Checks if both origAirport and destAirport are Airport objects, and that the flight code is valid
        if not isinstance(origAirport, Airport) and not isinstance(destAirport, Airport):
            raise TypeError("The origin and destination must be Airport objects")
        if not(len(flightNo) == 6 and flightNo[:3].isupper() and flightNo[:3].isalpha() and flightNo[3:].isdigit()):
             raise TypeError("The flight number format is incorrect")

        else:
            self._origAirport = origAirport
            self._flightNo = flightNo
            self._destAirport = destAirport

    # Repr for the flight class, printing "Flight(######) originCity -> destinationCity [international/national]"
    def __repr__(self):
        if self.isDomesticFlight():
            self.region = "[domestic]"
        else:
            self.region = "[international]"
        return f"Flight({self._flightNo}): {self._origAirport.getCity()} -> {self._destAirport.getCity()} {self.region}"

    # Checks if two flights have identical origin cities, and destination cities
    def __eq__(self, other):
        try:
            if self.getOrigin().getCity() == other.getOrigin().getCity() and self.getDestination().getCity() == self.getDestination().getCity():
                return True
            return False
        except:
            return False

    # Gets the flight number string
    def getFlightNumber(self):
        return self._flightNo

    # Gets the origin airport object
    def getOrigin(self):
        return self._origAirport

    # Gets the destination airport object
    def getDestination(self):
        return self._destAirport

    # Checks if the flight is domestic (origin + destination in same country) or international (across countries)
    def isDomesticFlight(self):
        if self._origAirport.getCountry() == self._destAirport.getCountry():
            return True
        else:
            return False

    # Sets the origin airport object
    def setOrigin(self, origin):
        self._origin = origin

    # Sets the destination airport object
    def setDestination(self, destination):
        self._destAirport = destination