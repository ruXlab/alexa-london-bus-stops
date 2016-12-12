







London Bus stops database
=======================


* http://naptan.app.dft.gov.uk/datarequest/help (GTFS dataset)
* http://naptan.app.dft.gov.uk/datarequest/GTFS.ashx (direct link)
```
	echo "stop_id\tstop_code\tstop_name\tstop_lat\tstop_lon\tstop_url\tvehicle_type" > LondonStops.tsv
	egrep "^49" Stops.txt  >> LondonStops.tsv
```
* 