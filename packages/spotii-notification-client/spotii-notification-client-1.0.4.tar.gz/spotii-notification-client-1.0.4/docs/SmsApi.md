# spotii_notification_client.SmsApi

All URIs are relative to *http://localhost:8000/api/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sms_messages_create**](SmsApi.md#sms_messages_create) | **POST** /sms/messages/ | 

# **sms_messages_create**
> SMSMessage sms_messages_create(body)



### Example
```python
from __future__ import print_function
import time
import spotii_notification_client
from spotii_notification_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = spotii_notification_client.SmsApi()
body = spotii_notification_client.SMSMessage() # SMSMessage | 

try:
    api_response = api_instance.sms_messages_create(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SmsApi->sms_messages_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SMSMessage**](SMSMessage.md)|  | 

### Return type

[**SMSMessage**](SMSMessage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

