from datetime import date, timedelta

from django.core.management.base import BaseCommand

from core.api.creators.models import Creator


class Command(BaseCommand):
    help = 'Update report state'

    def handle(self, *args, **options):
        creators = Creator.objects.filter(
                channel_report_generated=False,
                channel_registered_date__lte=date.today() - timedelta(days=3)
            )
        for creator in creators:
            creator.channel_report_generated = True
            creator.save()
            print(f"Report state updated for id: {creator.channel_id}, channel_name: {creator.channel_name}")
