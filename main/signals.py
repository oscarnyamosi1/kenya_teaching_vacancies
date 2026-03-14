# main/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from myutils import createThemes  # your utility function

themeList = ["macglass", "charcoal", "green"]

@receiver(post_migrate)
def initialize_default_themes(sender, **kwargs):
    # Only run for your 'main' app
    if sender.name == 'main':
        createThemes(themeList)