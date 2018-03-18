London bus stops Amazon Alexa skill
===================================


This skill allows users to get updates about buses coming to saved bus stop in London 

Skill is [available at Amazon Alexa Store](https://www.amazon.co.uk/ruX-lab-London-bus-stops/dp/B01N4DKTNY) for free

Service is Powered by TfL Open Data


### How to use it?

Say
> Alexa ask bus stop for update

To get updates about busses coming to saved bus stop


Say
> Alexa ask bus stop for setup

To configure skill. You'll be required to find 5 digit bus stop number either from plate at bus stop or online [on TfL website](https://tfl.gov.uk/modes/buses/). 
Unfortunatelly I couldn't find simpler way to configure it. If you have suggestions please [open an issue or make PR](https://github.com/ruXlab/alexa-london-bus-stops/issues)



### Where to get dataset?

Please follow these links and use oneliner provided below to filter out London bus stops and generate dataset recognized by application

* [GTFS dataset](http://naptan.app.dft.gov.uk/datarequest/help)
* [Direct link for dataset](http://naptan.app.dft.gov.uk/datarequest/GTFS.ashx)

```
	echo "stop_id\tstop_code\tstop_name\tstop_lat\tstop_lon\tstop_url\tvehicle_type" > LondonStops.tsv
	egrep "^49" Stops.txt  >> LondonStops.tsv
```


### Dependencies
* Python 3.5, ```sudo apt-get install python3.5 python3-setuptools python3.5-dev build-essential ```
*  (inside virtualenv) ```pip install flask flask-ask encodings requests```
