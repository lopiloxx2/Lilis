import logging
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend

logger = logging.getLogger(__name__)


class ConsoleAndSMTPBackend:
    """Email backend that sends via SMTP and also writes a copy to the console.

    Useful for development when you want real delivery and a local copy.
    It reads SMTP configuration from Django settings (EMAIL_HOST, EMAIL_PORT, etc.).
    Exceptions from SMTP are logged and re-raised depending on
    `settings.EMAIL_FAIL_SILENTLY`.
    """

    def __init__(self, *args, **kwargs):
        self.smtp = SMTPBackend(
            host=getattr(settings, 'EMAIL_HOST', None),
            port=getattr(settings, 'EMAIL_PORT', None),
            username=getattr(settings, 'EMAIL_HOST_USER', None),
            password=getattr(settings, 'EMAIL_HOST_PASSWORD', None),
            use_tls=getattr(settings, 'EMAIL_USE_TLS', False),
            use_ssl=getattr(settings, 'EMAIL_USE_SSL', False),
            fail_silently=getattr(settings, 'EMAIL_FAIL_SILENTLY', False),
            timeout=getattr(settings, 'EMAIL_TIMEOUT', None),
        )
        self.console = ConsoleBackend()

    def send_messages(self, email_messages):
        sent_smtp = None
        try:
            sent_smtp = self.smtp.send_messages(email_messages)
        except Exception as exc:
            # Log the exception so the developer can see SMTP errors
            logger.exception('SMTP send_messages failed: %s', exc)
            # If not configured to fail silently, re-raise so the server shows the error
            if not getattr(settings, 'EMAIL_FAIL_SILENTLY', False):
                raise

        # always write to console as well (for local copy)
        sent_console = None
        try:
            sent_console = self.console.send_messages(email_messages)
        except Exception:
            logger.exception('Console backend failed to write email(s)')

        # prefer smtp count if available, otherwise console
        if isinstance(sent_smtp, int):
            return sent_smtp
        return sent_console
