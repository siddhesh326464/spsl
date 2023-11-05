import os
from django.core.management.base import BaseCommand
from apps.job.models import Campaign

class Command(BaseCommand):
    def handle(self, *args, **options):
      try:
        base_path = os.getcwd() 
        path = os.path.join(base_path,'campaign.csv') 
        with open(path,'r') as file:
            data=file.readlines()
            data = [Campaign(name=x.strip()) for x in data[1:]]
            Campaign.objects.all().delete()
            Campaign.objects.bulk_create(data)
        self.stdout.write(
                self.style.SUCCESS('Campaign created successfully')
            )
      except Exception as e:
        self.stdout.write(
                self.style.ERROR(e)
            )