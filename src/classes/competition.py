class Competition:

    def __init__(self):
        self.Name = 'Foo'

    def set__name(self, Name):
        """Set competition name.

        Args:
            Name (string): Competition name.
        """
        self.Name = Name
        self.Filled += 1

    def set_timezone(self, Timezone):
        """Set timezone.

        Args:
            Timezone (int): Competition timezone in UTC.
        """
        self.Timezone = Timezone
        self.Filled += 1

    def set_start_date(self, Date):
        """Set competition start.

        Args:
            Date (DateTime): Competition start.
        """
        self.StartDate = Date
        self.Filled += 1

    def set_end_date(self, Date):
        """Set competition end.

        Args:
            Date (DateTime): Competition end.
        """
        self.EndDate = Date
        self.Filled += 1

    def set_country(self, Country):
        """Set competition country.

        Args:
            Country (string): Competition country.
        """
        self.Country = Country
        self.Filled += 1

    def set_location(self, Location):
        """Set competition location

        Args:
            Location ([type]): [description]
        """
        self.Location = Location
        self.Filled += 1

    def set_url(self, url):
        """Set competition url.

        Args:
            url (string): Competition url.
        """
        self.url = url
        self.Filled += 1
