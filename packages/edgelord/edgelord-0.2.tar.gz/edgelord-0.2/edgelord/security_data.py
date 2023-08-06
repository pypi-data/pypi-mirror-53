from datetime import datetime
import pandas
from pandas.tseries.offsets import BDay
from tiingo import TiingoClient
import time
import os

def last_business_day(days = 1):
    """Return the date for the last business day"""

    today = pandas.datetime.today()
    today = str(today - BDay(days)).split(" ")[0].split("-")
    today = datetime(int(today[0]), int(today[1]), int(today[2]))

    return today

class security_data:
    """Time series data"""
    cache_directory = None
    columns_allowed = None
    data = None
    parent = None

    # Magic subroutines
    #
    def __init__(self, parent, caching = False):
        self.caching = caching
        self.columns_allowed = ['close', 'high', 'low', 'open', 'volume']
        self.parent = parent

        # Check caching
        if 'EDGELORD_CACHE_DIR' in os.environ:
            self.cache_directory = str(os.environ['EDGELORD_CACHE_DIR']).replace("~", os.environ['HOME'])
            if os.path.exists(self.cache_directory):
                days_before_renew = 2
                if 'EDGELORD_CACHE_DAYS' in os.environ:
                    day_before_renew = int(os.environ['EDGELORD_CACHE_DAYS'])

                seconds = time.time() - os.stat(self.cache_directory).st_mtime
                minutes = (seconds / 60)
                hours = (minutes / 60)
                days = (hours / 24)

                if days > 1 and days_before_renew < days:
                    os.rmdir(self.cache_directory)
            else:
                os.mkdir(self.cache_directory)

#    def __del__(self):
#        if self.caching and self.cache_directory is not None:
#            self.frame().to_json("%s/%s.json" % (self.cache_directory, self.parent.ticker))

    def __str__(self):
        return str(self.frame())

    # Operation subroutines
    #
    def build(self, data):
        """Restructure data to be usable"""

        self.data = []
        
        for row in data.values.tolist():
            self.data.append(row)

        self.columns = data.columns
        return self


    def frame(self):
        """Return data as dataframe"""

        return pandas.DataFrame(self.data, columns = self.columns).sort_values(by=['date'])

    def from_cache(self):
        print("...")
        return 1

    def from_csv(self, file):
        """Build a security_data object from the given CSV file"""
        
        data = pandas.read_csv(file)
        return self.build(data)


    def from_json(self, file):
        """Build a security_data object from the given JSON file"""

        with open(file, 'r') as f:
            data = f.read()
            f.close()
        
        data = pandas.read_json(data)
        data = data.sort_values(by=['date'])
        return self.build(data)

    def from_rest(self, ticker = None, days = 260):
        """Download data from Tiingo"""


        self.cache_filename = "%s/%s.json" % (self.cache_directory, ticker)
        if os.path.exists(self.cache_filename):
            buffer = self.from_json(self.cache_filename)
            print("Loading from cache")
        else:
            client = TiingoClient()
            data = client.get_ticker_price(ticker, startDate=last_business_day(days), endDate=last_business_day())

            result = []

            column_list = None
            set_columns = False
            for row in data:
                buffer = {}
                
                if column_list is None and not set_columns:
                    column_list = []

                for column in row:
                    # Loop through each rows column list
                    if ("adj" in column) or (column == 'date'):
                        # Only grab adjusted data (to account for any splits)

                        column_name = column.replace("adj", "").lower()

                        if not set_columns:
                            column_list.append(column.replace("adj", "").lower())

                        if column == 'date':
                            buffer[column_name] = row[column].split("T")[0]
                        else:
                            buffer[column_name] = row[column]

                if not set_columns and column_list is not None:
                    # Only set the column list once
                    set_columns = True

                result.append(buffer)

            data = pandas.DataFrame(result, columns=column_list)
            data = data.sort_values(by=['date'])

            data.to_json("%s/%s.json" % (self.cache_directory, ticker))
            buffer = self.build(data)

        return buffer
        