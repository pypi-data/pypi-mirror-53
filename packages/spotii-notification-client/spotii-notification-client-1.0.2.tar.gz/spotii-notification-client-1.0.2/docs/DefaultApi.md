# spotii_notification_client.DefaultApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_message**](DefaultApi.md#create_message) | **POST** /api/v1.0/sms/messages/ | 
[**create_message_0**](DefaultApi.md#create_message_0) | **POST** /api/v1.0/email/messages/ | 

# **create_message**
> Object create_message(body=body)



### Example
```python
from __future__ import print_function
import time
import spotii_notification_client
from spotii_notification_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = spotii_notification_client.DefaultApi()
body = spotii_notification_client.Body() # Body |  (optional)

try:
    api_response = api_instance.create_message(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->create_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body**](Body.md)|  | [optional] 

### Return type

[**Object**](Object.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_message_0**
> Object create_message_0(body=body)



### Example
```python
from __future__ import print_function
import time
import spotii_notification_client
from spotii_notification_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = spotii_notification_client.DefaultApi()
body = spotii_notification_client.Body1() # Body1 |  (optional)

try:
    api_response = api_instance.create_message_0(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->create_message_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body1**](Body1.md)|  | [optional] 

### Return type

[**Object**](Object.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

