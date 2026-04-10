# main/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from myutils import createThemes  # your utility function

themeList = ["macglass", "charcoal", "green"]

@receiver(post_migrate)
def initialize_default_themes(sender, **kwargs):
    # Only run for your 'main' app
    if sender.name == 'main':
        from django.db import connection
        table_names = connection.introspection.table_names()
        if 'main_theme' in table_names:
            createThemes(themeList)
