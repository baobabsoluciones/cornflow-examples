from django.core.management.base import BaseCommand

from interface.const import stations, no_position_station, tasks, tasks_duration, precedences, station_order
from interface.models import Stations, Tasks, Precedences

class Command(BaseCommand):
    help='Loads the database'

    def handle(self, *args, **kwargs):
        Stations.objects.all().delete()
        for station in stations:
            Stations(name=station, no_position=no_position_station[station], order=station_order[station]).save()

        Tasks.objects.all().delete()
        for task in tasks:
            Tasks(name= task, duration = tasks_duration[task]).save()

        Precedences.objects.all().delete()
        for precedence in precedences:
            Precedences(before=Tasks.objects.get(name=precedence[0]),
                        after=Tasks.objects.get(name=precedence[1])).save()

        self.stdout.write(self.style.SUCCESS('DATA LOADED!'))
