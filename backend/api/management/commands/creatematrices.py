from django.core.management.base import BaseCommand, CommandError
from backend.api.models import TramStop, Line, LineTimetable, AdjacencyMatrixCell, AdjacencyMatrix, LineMatrix
import json
from math import sin, cos, sqrt, atan2, radians
class Command(BaseCommand):
    help = 'Create base plans and thumbnail resolutions'


    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('creating matrices'))


        R = 6373.0
        grap = []
        Lrap = []
        tramstops = TramStop.objects.all()
        for count,row in enumerate(tramstops):
            f = []
            grap.append(f)

            adjmatcells = AdjacencyMatrixCell.objects.filter(row=row)
            d = []
            Lrap.append(d)



            for column in tramstops:
                que = adjmatcells.filter(col=column)
                if que.count() > 0:
                    inlist = []
                    for each in que[0].lines.all():
                        inlist.append(each.pk)
                    d.append(inlist)
                else:
                    d.append(0)

                try:
                    f.append(que[0].value)
                except:


                    lat1 = radians(row.latitude)
                    lon1 = radians(row.longitude)
                    lat2 = radians(column.latitude)
                    lon2 = radians(column.longitude)

                    dlon = lon2 - lon1
                    dlat = lat2 - lat1

                    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    distance = R * c
                    if distance*1000 < 300 and distance != 0 and row.name == column.name:
                        if distance*10 < 0.5:
                            f.append(1)
                        else:
                            f.append(int(round(distance*12, 0)))
                        # pass
                    else:
                        f.append(0)
        AdjacencyMatrix.objects.create(
        matrix = json.dumps(grap)
        )

        LineMatrix.objects.create(
        matrix = json.dumps(Lrap)
        )

        self.stdout.write(self.style.SUCCESS('Successfully created'))
