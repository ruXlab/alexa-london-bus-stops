import pandas as pd
from urllib.request import urlopen # Python 3
import os.path
import urllib.request
url = "http://naptan.app.dft.gov.uk/datarequest/GTFS.ashx"
zipfile = "GTFS.zip"


if not os.path.exists(zipfile):
	print("Downloading {}".format(zipfile))
	with urllib.request.urlopen(url) as response, open(zipfile, 'wb') as out_file:
	    data = response.read() # a `bytes` object
	    out_file.write(data)

t = pd.read_table(zipfile)
t.dropna(subset=['stop_code'], inplace=True)
t.set_index(['stop_code'], inplace=True)
t = t[t.stop_id.str.match('^49')]
t.drop('stop_url', axis=1, inplace=True)
t.drop(['vehicle_type', 'stop_lat', 'stop_lon'], axis=1, inplace=True)


t.to_csv("LondonStops.csv", sep="\t")

print(t)

print(t.columns)
