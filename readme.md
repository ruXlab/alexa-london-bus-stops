London bus stops Amazon Alexa skill
===================================

This skill allows users to get updates about buses coming to saved bus stop in London 


Service is Powered by TfL Open Data







### Where to get dataset?



* http://naptan.app.dft.gov.uk/datarequest/help (GTFS dataset)
* http://naptan.app.dft.gov.uk/datarequest/GTFS.ashx (direct link)
```
	echo "stop_id\tstop_code\tstop_name\tstop_lat\tstop_lon\tstop_url\tvehicle_type" > LondonStops.tsv
	egrep "^49" Stops.txt  >> LondonStops.tsv
```


### Dependencies
* Python 3.5, ```sudo apt-get install python3.5 python3-setuptools python3.5-dev build-essential ```
*  (inside virtualenv) ```pip install flask flask-ask encodings requests```
