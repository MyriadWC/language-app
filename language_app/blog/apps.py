from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        # Automatically registers and connects signal receiver functions to their signals when
        # django starts
        import blog.signals
