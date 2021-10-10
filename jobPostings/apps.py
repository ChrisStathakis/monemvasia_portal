from django.apps import AppConfig


class JobpostingsConfig(AppConfig):
    name = 'jobPostings'

    def ready(self):
        import jobPostings.signals
