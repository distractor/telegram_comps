"""
Master file reads all urls and saves competitions to a JSON file
"""
import json
import pandas as pd

from readAirtribune import *
from readLivetrack24 import *
from readSlocomps import *
from readPWCA import *
from readPGCP import *

comps = readSlocomps()
N = len(comps)
print('Imported %d competitions from Slocomps.' % N)

# comps += readAirtribune()
# print('Imported %d competitions from Airtribune.' % (len(comps) - N))
# N = len(comps)

# comps += readLivetrack24()
# print('Imported %d competitions from Livetrack24.' % (len(comps) - N))
# N = len(comps)

# comps += readPWCA()
# print('Imported %d competitions from PWCA.' % (len(comps) - N))
# N = len(comps)

# comps += readPGCP()
# print('Imported %d competitions from PGCP.' % (len(comps) - N))
# N = len(comps)

cols = ['Name', 'Timezone', 'StartDate', 'EndDate', 'Country',
        'Location', 'Lat', 'Lon', 'url', 'Sport', 'Filled']
Names = [comp.Name for comp in comps]
Timezones = [comp.Timezone for comp in comps]
StartDates = [comp.StartDate for comp in comps]
EndDates = [comp.EndDate for comp in comps]
Countries = [comp.Country for comp in comps]
Locations = [comp.Location for comp in comps]
Lats = [comp.Lat for comp in comps]
Lons = [comp.Lon for comp in comps]
Urls = [comp.url for comp in comps]
Sports = [comp.Sport for comp in comps]
Fill = [comp.Filled for comp in comps]

data = pd.DataFrame(list(zip(Names, Timezones, StartDates, EndDates,
                             Countries, Locations, Lats, Lons, Urls, Sports, Fill)), columns=cols)

# remove all that are not Paragliding competitions
data = data.loc[data['Sport'] == 0]

# Find duplicates by name
#duplicates = data[data.duplicated(['Name'], keep = False)]
# drop duplicates from original dataframe
#data.drop_duplicates(['Name'], keep = False, inplace = True)
# sort duplicates by filled factor
#duplicates.sort_values(by = ['Filled'], ascending = False)
# from duplicates by name only keep the first with the same start date
#temp = duplicates
#temp.drop_duplicates(['StartDate'], keep = 'first')
# merge with original
#data = pd.concat([data, temp])

# sort by date
data.sort_values(by=['StartDate'])

# Save to JSON
data.to_json('../data/out.json')
print('Total competitions saved: %d' % data.shape[0])
print('Saved to file ../json/out.json.')
