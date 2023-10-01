class Airport:
    # Constructor for the airport object class
    def __init__(self, code, city, country,continent):
        self._code = code
        self._city = city
        self._country = country
        self._continent = continent

    # Repr for the airport object, printing "### (cityName, countryName)"
    def __repr__(self):
        return (f"{self._code} ({self._city}, {self._country})")

    # Gets the airport's code
    def getCode(self):
        return self._code

    # Gets the airport's city
    def getCity(self):
        return self._city

    # Gets the airport's country
    def getCountry(self):
        return self._country

    # Gets the airport's continent
    def getContinent(self):
        return self._continent

    # Sets the airport's city
    def setCity(self, city):
        self._city = city

    # Sets the airport's country
    def setCountry(self, country):
        self._country = country

    # Sets the airport's continent
    def setContinent(self, continent):
        self._continent = continent