# spotii-notification-client
API for notification things

- API version: 1.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.v3.generators.python.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install spotii-notification-client
```

Then import the package:
```python
import spotii_notification_client 
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import spotii_notification_client
from spotii_notification_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = spotii_notification_client.DefaultApi(spotii_notification_client.ApiClient(configuration))
body = spotii_notification_client.Body() # Body |  (optional)

try:
    api_response = api_instance.create_message(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->create_message: %s\n" % e)

# create an instance of the API class
api_instance = spotii_notification_client.DefaultApi(spotii_notification_client.ApiClient(configuration))
body = spotii_notification_client.Body1() # Body1 |  (optional)

try:
    api_response = api_instance.create_message_0(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->create_message_0: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to */*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DefaultApi* | [**create_message**](docs/DefaultApi.md#create_message) | **POST** /api/v1.0/sms/messages/ | 
*DefaultApi* | [**create_message_0**](docs/DefaultApi.md#create_message_0) | **POST** /api/v1.0/email/messages/ | 

## Documentation For Models

 - [Body](docs/Body.md)
 - [Body1](docs/Body1.md)

## Documentation For Authorization

 All endpoints do not require authorization.


## Author


