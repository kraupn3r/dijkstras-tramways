
from tramfind.models import TramStop, Line, LineTimetable, AdjacencyMatrixCell
import json
from math import sin, cos, sqrt, atan2, radians
from django.db import connection
from django.db import reset_queries
import time
R = 6373.0
grap = []
reset_queries()
start_queries = len(connection.queries)

tramstops = TramStop.objects.all()

start = time.perf_counter()
for count,row in enumerate(tramstops):
    f = []
    grap.append(f)

    adjmatcells = AdjacencyMatrixCell.objects.filter(row=row)
    for column in tramstops:
        # print(column.id)
        #
        if adjmatcells.get(col=column).first() is not None:
            f.append(adjmatcells.get(col=column).value)
        else:


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

    print(connection.queries[0:10])
    end = time.perf_counter()
    end_queries = len(connection.queries)
    print(f"Number of Queries : {end_queries - start_queries}")
    print(f"Finished in : {(end - start):.2f}s")
    print(count, tramstops.count())



    # grap = [[adjmatcells.filter(col=column).filter(row=row)[0].value if adjmatcells.filter(col=column).filter(row=row).exists() else 0 for column in tramstops] for row in tramstops]
#from django.db import connection

# with open('scripts/data.json', 'w', encoding="utf-8") as data:
#     data.write(json.dumps(grap))


#
# Lrap = []
# for count,row in enumerate(TramStop.objects.all()):
#     d = []
#     Lrap.append(d)
#
#     for column in TramStop.objects.all():
#         # print(column.id)
#         if AdjacencyMatrixCell.objects.all().filter(col=column).filter(row=row).count() > 0:
#             inlist = []
#             for each in AdjacencyMatrixCell.objects.all().filter(col=column).filter(row=row)[0].lines.all():
#                 inlist.append(each.pk)
#             d.append(inlist)
#         else:
#             d.append(0)
#     print(count, TramStop.objects.all().count())
#
# with open('scripts/lines.json', 'w', encoding="utf-8") as data:
#     data.write(json.dumps(Lrap))


# latrap = []
# R = 6373.0
# for count,row in enumerate(TramStop.objects.all()):
#     d = []
#     latrap.append(d)
#     for column in TramStop.objects.all():
#
#
#         lat1 = radians(row.latitude)
#         lon1 = radians(row.longitude)
#         lat2 = radians(column.latitude)
#         lon2 = radians(column.longitude)
#
#         dlon = lon2 - lon1
#         dlat = lat2 - lat1
#
#         a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#         distance = R * c
#         if distance*1000 < 120 and distance != 0 and row.name == column.name:
#
#             d.append(column.pk)
#
#     print(count, TramStop.objects.all().count())
#
# with open('scripts/lats.json', 'w', encoding="utf-8") as data:
#     data.write(json.dumps(latrap))

# for each in TramStop.objects.all():
#     for beach in TramStop.objects.all():
#
#
#
#

#         R = 6373.0
#
#         lat1 = radians(each.latitude)
#         lon1 = radians(each.longitude)
#         lat2 = radians(beach.latitude)
#         lon2 = radians(beach.longitude)
#
#         dlon = lon2 - lon1
#         dlat = lat2 - lat1
#
#         a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#         distance = R * c
#         if distance*1000 < 120 and distance != 0 and each.name == beach.name:
#             line_instance = Line.objects.create(
#                 number = 0,
#                 first_stop = each,
#                 last_stop = beach,
#                 walkline = True
#             )
#             LineTimetable.objects.create(
#                 line = line_instance,
#                 stop = each,
#                 order = 0,
#                 time_since_0 = 0
#             )
#             LineTimetable.objects.create(
#                 line = line_instance,
#                 stop =beach,
#                 order = 1,
#                 time_since_0 = 1
#             )
