from django.apps import AppConfig


class NetworkConfig(AppConfig):
    name = 'network'
    
    def ready(self):
        import network.models  # Import your models to ensure signal handlers are connected
