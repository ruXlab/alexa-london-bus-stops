import requests
import logging
import csv

logger = logging.getLogger("tfl").setLevel(logging.DEBUG)

stops = dict()
with open("data/LondonStops.csv") as tsv:
	reader = csv.reader(tsv, dialect="excel-tab")
	#tsv.next(reader)
	for line in reader:
		stops[line[0]] = (line[1], line[2])
	logging.info("Loaded {} bus stops".format(len(stops)))


class TFL:
	def arrivals(bus_stop):
		'''
		Returns list of [bus_number, arrival_in_seconds]
		'''
		url = "https://api.tfl.gov.uk/StopPoint/{}/arrivals".format(bus_stop)
		json = requests.get(url=url).json()
		m = dict()

		for i in json:
			m[i['lineId']] = m.get(i['lineId'], i['timeToStation'])
			if m[i['lineId']] > i['timeToStation']:
				m[i['lineId']] = i['timeToStation']

		return [ [k,v] for k, v in m.items() ]
		
	def lookup_bus_stop(short_number):
		return stops.get(short_number, None)
