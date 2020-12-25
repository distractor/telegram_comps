class Competition:

    def __init__(self):
        self.Name = ''
        self.Timezone = ''
        self.StartDate = ''
        self.EndDate = ''
        self.Country = ''
        self.Location = ''
        self.Lat = ''
        self.Lon = ''
        self.url = ''
        self.Sport = ''

        self.Filled = 0

    def SetName(self, Name):
        """Set competition name.

        Args:
            Name (string): Competition name.
        """
        self.Name = Name
        self.Filled += 1

    def SetTimezone(self, Timezone):
        """Set timezone.

        Args:
            Timezone (int): Competition timezone in UTC.
        """
        self.Timezone = Timezone
        self.Filled += 1

    def SetStartDate(self, Date):
        """Set competition start.

        Args:
            Date (DateTime): Competition start.
        """ 
        self.StartDate = Date
        self.Filled += 1

    def SetEndDate(self, Date):
        """Set competition end.

        Args:
            Date (DateTime): Competition end.
        """
        self.EndDate = Date
        self.Filled += 1

    def SetCountry(self, Country):
        """Set competition country.

        Args:
            Country (string): Competition country.
        """
        self.Country = Country
        self.Filled += 1

    def SetLocation(self, Location):
        """Set competition location

        Args:
            Location ([type]): [description]
        """
        self.Location = Location
        self.Filled += 1

    def SetLatitude(self, Latitude):
        self.Lat = Latitude
        self.Filled += 1

    def SetLongitute(self, Longitude):
        self.Lon = Longitude
        self.Filled += 1

    def SetUrl(self, url):
        self.url = url
        self.Filled += 1

    def SetSport(self, ID):
        self.Sport = ID  # 0 for XC paragliding
        self.Filled += 1

    def GetFullness(self):
        return self.Filled
