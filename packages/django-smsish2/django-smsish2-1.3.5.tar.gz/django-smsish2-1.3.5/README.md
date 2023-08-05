# django-smsish
Forked from [RyanBalfanz](https://github.com/RyanBalfanz/django-smsish)

Installation
------------

Add `smsish` to your `INSTALLED_APPS` and set `SMS_BACKEND`.
```
	INSTALLED_APPS += (
		'smsish',
	)

	SMS_BACKEND_CONSOLE = 'smsish.sms.backends.console.SMSBackend'
	SMS_BACKEND_DUMMY = 'smsish.sms.backends.dummy.SMSBackend'
	SMS_BACKEND_TWILIO = 'smsish.sms.backends.twilio.SMSBackend'
	SMS_BACKEND_YUNPIAN = 'smsish.sms.backends.yunpian.SMSBackend'
	SMS_BACKEND = SMS_BACKEND_DUMMY
```
## Twillio
To use the Twilio backend set some additional settings as well.
```
	TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", None)
	TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", None)
	TWILIO_MAGIC_FROM_NUMBER = "+15005550006"  # This number passes all validation.
	TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", TWILIO_MAGIC_FROM_NUMBER)
```

Example:
```
from smsish.sms import send_sms
send_msg(message, '', (phone,))
```
Note: You must also `pip install twilio` to use the Twilio backend.

## Yunpian

settings.py:
```
YUNPIAN_API_KEY = getenv("YUNPIAN_API_KEY")
```
Note: You must also `pip install yunpian-python-sdk` to use the YunPian backend.

Example:
```
from smsish.sms import send_sms
send_msg(message, '', (phone,))
```

# Test

```
tox
# tox in docker

docker run --rm -it -v ${PWD}:/src themattrix/tox
```
