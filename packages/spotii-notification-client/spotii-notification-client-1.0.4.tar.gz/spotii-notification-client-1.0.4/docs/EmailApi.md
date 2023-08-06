# spotii_notification_client.EmailApi

All URIs are relative to *http://localhost:8000/api/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**email_messages_create**](EmailApi.md#email_messages_create) | **POST** /email/messages/ | 

# **email_messages_create**
> EmailMessage email_messages_create(body)



### Example
```python
from __future__ import print_function
import time
import spotii_notification_client
from spotii_notification_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = spotii_notification_client.EmailApi()
body = spotii_notification_client.EmailMessage() # EmailMessage | 

try:
    api_response = api_instance.email_messages_create(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailApi->email_messages_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EmailMessage**](EmailMessage.md)|  | 

### Return type

[**EmailMessage**](EmailMessage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

