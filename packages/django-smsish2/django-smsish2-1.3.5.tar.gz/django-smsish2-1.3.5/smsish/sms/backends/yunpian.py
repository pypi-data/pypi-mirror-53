import logging
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient

logger = logging.getLogger(__name__)


class SMSBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.connection = None

    def open(self):
        """
		Ensures we have a connection to the SMS gateway. Returns whether or not a new connection was required (True or False).
		"""
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        self.connection = self._get_connection()
        return True

    def close(self):
        """Closes the connection to the email server."""
        del self.connection

    def send_messages(self, email_messages):
        """
		Sends one or more SMSMessage objects and returns the number of text messages sent.
		"""
        if not email_messages:
            return
        new_conn_created = self.open()
        if not self.connection:
            # We failed silently on open().
            # Trying to send would be pointless.
            return
        num_sent = 0
        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
            if new_conn_created:
                self.close()
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        from_email = email_message.from_email
        recipients = email_message.recipients()
        param = {YC.MOBILE: recipients, YC.TEXT: email_message.body}
        try:
            result = self.connection.sms().single_send(param)
        except Exception:
            if not self.fail_silently:
                raise
            return False
        if not result.is_succ():
            raise Exception(result.msg())

        return True

    def _get_connection(self):
        client = YunpianClient(settings.YUNPIAN_API_KEY)
        return client
