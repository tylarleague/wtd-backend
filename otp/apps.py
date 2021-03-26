from django.apps import AppConfig


class OtpConfig(AppConfig):
    name = 'otp'

    def ready(self):
        import otp.tasks
