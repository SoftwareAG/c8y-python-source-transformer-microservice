# cumulocity-source-transformer-microservice


This project is an microservice that allows sending measurements, events and alarms to the Cumulocity API´s while not knowing the internalID. Therefore an own service endpoint is opened that requires the externalId and the externalId type in the POST request. The Event/Alarm/Measurement is thus transformed with the microservice and handed over to the real Cumulocity API.

# Content
- [cumulocity-source-transformer-microservice](#cumulocity-source-transformer-microservice)
- [Content](#content)
- [Quick Start](#quick-start)
- [How to use](#how-to-use)
- [Solution components](#solution-components)
- [Installation from scratch](#installation-from-scratch)

# Quick Start
Use the provided zip here in the release and upload it as microservice.

![Upload](/pics/upload.png)

# How to use

Measurements, Alarms or Events can be send while adding "type" and "externalId as parameter to the POST request.
The API endpoint is opened on /service/{service-name}/(event/events,alarm/alarms,measurement/measurements) and adds the interalId to the payload before handing the payload to the Cumulocity API.
Please be aware that due to that intermediate service no further inventory role filtering takes place anymore. A device that can reach that service endpoint can write to any device.

```bash
curl --location 
--request POST '{C8Y_URL}/service/source-transformer/measurement/measurements?type=c8y_Serial&externalId=mbay-test' \
--data-raw '{
  "time": "2022-10-12T12:03:27.845Z",
  "type": "c8y_TemperatureMeasurement",
  "c8y_Steam": {
    "Temperature": {
      "unit": "C",
      "value": 100
    }
  }
}'
```

# Solution components

The microservice consists of 4 modules and a main runtime:
* `main.py`: Main runtime that opens an health endpoint at /health and also creates the rest endpoints
* `API/authentication.py`: Contains the Authentication class that requests the service user via the bootstrap user from within the microservice environment. See [documentation](https://cumulocity.com/guides/microservice-sdk/concept/#microservice-bootstrap) for more details.
* `API/inventory.py`: Consists of the logic to deliver the internalId of the device from the externalId and the externalId type.
* `API/measurments.py`: Creates the measurement from the payload and sends it to Cumulocity.
* `API/events.py`: Creates the events from the payload and sends it to Cumulocity.
* `API/alarms.py`: Creates the alarm from the payload and sends it to Cumulocity.

* `resources/base.py`: Is the base class of the request within the service microservice. It contains the main logic on extracting the externalId and the externalId type from the POST request. It also queries the internalId while calling `API/inventory.py` and replaces the {"source": {"id": "internalID"} } within the json body of the POST request. The base class is used from the specialized classes that handles logic of the endpoints etc.
* `resources/alarms.py`: Is called when the alarms endpoint is calles on the service microservices and hand the payload over to 'API/alarms.py'.
* `resources/events.py`: Is called when the events endpoint is calles on the service microservices and hand the payload over to 'API/events.py'.
* `resources/measurements.py`: Is called when the measurements endpoint is calles on the service microservices and hand the payload over to 'API/measurements.py'.

Currently the sheduled request for statistics is set to be 900s which equals 15 minutes. Debug Level is set to be INFO. Feel free to adjust the resolution but keep in mind that a device is created for every subtenant as well as a certain device class is associated with that.

# Installation from scratch

To build the microservice run:
```
docker buildx build --platform linux/amd64 -t {NAMEOFSERVICE} .
docker save {NAMEOFSERVICE} > image.tar
zip {NAMEOFSERVICE} cumulocity.json image.tar
```

You can upload the microservice via the UI or via [go-c8y-cli](https://github.com/reubenmiller/go-c8y-cli)


------------------------------

These tools are provided as-is and without warranty or support. They do not constitute part of the Software AG product suite. Users are free to use, fork and modify them, subject to the license agreement. While Software AG welcomes contributions, we cannot guarantee to include every contribution in the master project.
_____________________
For more information you can Ask a Question in the [TECHcommunity Forums](http://tech.forums.softwareag.com/techjforum/forums/list.page?product=cumulocity).

You can find additional information in the [Software AG TECHcommunity](http://techcommunity.softwareag.com/home/-/product/name/cumulocity).