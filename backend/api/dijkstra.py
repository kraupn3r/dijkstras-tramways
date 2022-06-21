import sys
import json
from backend.api.models import AdjacencyMatrix,LineMatrix,TramStop,Line,StopTimetable,LineTimetable
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph


class Graph():
    def __init__(self, vertices):

        self.V = vertices
        self.graph = json.loads(AdjacencyMatrix.objects.all().latest().matrix)
        self.Lgraph = json.loads(LineMatrix.objects.all().latest().matrix)
        self.vdict = {}
        for count, each in enumerate(TramStop.objects.all()):
            self.vdict[count] = each
        self.end = 1

# sorts path into dict of Line objects containing stops from path
    def pathfinder(self, node, lines, path):
        sets = {}
        lines = list(lines)
        lineSet = {}

        if lines == []:
            path.append(node)
            lines.append(self.vdict[node].line.all()[0].pk)

        for line in lines:
            linestoplist = []
            for each in LineTimetable.objects.filter(line=line).order_by('order'):
                linestoplist.append(each.stop.pk)

            sets[line] = []
            for v in path:
                if (self.vdict[v].pk in linestoplist) == True:
                    sets[line].append(v)


        for k, p in sets.items():
            lineSet[Line.objects.get(pk=k)] = sets[k]
        return lineSet



# Returns a list of Lines that together cover path
    def routeer(self, path, sets):
        route = []
        current = path[0]
        todel = []

        for k, p in sets.items():
            stops = [self.vdict[x] for x in p]
            timetables = [LineTimetable.objects.filter(line=k).filter(stop=stops[-1])[0],
                          LineTimetable.objects.filter(line=k).filter(stop=stops[0])[0]]
            if timetables[0].order - timetables[1].order != len(p) - 1:
                todel.append(k)
        for k in todel:
            del sets[k]
        while True:
            inn = False
            for k, p in sets.items():
                if current in p and current != p[-1]:
                    inn = True
            if inn == False and current != path[-1]:
                current = path[path.index(current) + 1]
                route.append('walk')
            elif inn == False:
                route.append('walk')
                return route

            if current == path[-1]:
                return route

            for k, p in sets.items():
                if current in p and path[-1] in p:
                    sum = 0
                    sum += len(p)
                    for each in route:
                        if each == 'walk':
                            sum += 1
                        else:
                            sum += len(sets[each])
                    if sum >= len(path):
                        route.append(k)
                        return route


            longest = 0
            for ka, pa in sets.items():
                if ka not in route and current in pa and current != pa[-1]:
                    if len(pa) > longest:
                        long_dir = ka
                        longest = len(sets[ka])

            current = sets[long_dir][-1]
            route.append(long_dir)

    def printSolution(self, dist, pathset, lines):
        node = self.end
        route = self.routeer(pathset[node], self.pathfinder(
            node, lines[node], pathset[node]))
        path = pathset[node]
        pathfind = self.pathfinder(node, lines[node], pathset[node])
        return route, path, pathfind

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree

    def minDistance(self, dist, sptSet):

         # Initialize minimum distance for next node
        min = sys.maxsize

        # Search not nearest vertex not in the
        # shortest path tree
        min_index = 19999
        for v in range(self.V):

            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v



        return min_index

    def linepath(self, currentlines, adjacentlines):
        if adjacentlines == 0:
            adjacentlines = [0]
        intersectedlines = []
        penalty = 0
        walkpenalty = 1
        # //wtf w ogole o co cho że tranferpenalty wpływa na przechodzenie po tych samych przystankach
        transferpenalty = 2
        if len(currentlines) == 0:
            if adjacentlines == [0]:
                penalty = walkpenalty
            else:
                # penalty = transferpenalty
                intersectedlines = adjacentlines.copy()
        elif len(currentlines) > 0 and adjacentlines == [0]:
            pass
        elif len(currentlines) > 0 and len(adjacentlines) > 0:
            for line in currentlines:
                if line in adjacentlines:
                    intersectedlines.append(line)
        if len(intersectedlines) == 0:
            penalty = transferpenalty

            if adjacentlines != [0]:
                intersectedlines = adjacentlines.copy()
        return intersectedlines, penalty

    # Funtion that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation

    def dijkstra(self, src):

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        pathset = [[]] * self.V
        lines = [set()] * self.V
        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:

                    intersectedlines = []
                    intersectedlines, penalty = self.linepath(
                        lines[u], self.Lgraph[u][v])

                    dist[v] = dist[u] + self.graph[u][v]
                    dist[v] = dist[v] + penalty

                    pathset[v] = pathset[u].copy()
                    pathset[v].append(u)

                    lines[v] = lines[u].copy()
                    for each in intersectedlines:
                        lines[v].add(each)
        for count, each in enumerate(pathset):
            each.append(count)
        return self.printSolution(dist, pathset, lines)






class Driver():
    def __init__(self, startstop, endstop, start_time, start_long, start_lat, end_long, end_lat):

        if start_time == '':
            self.start_time = timezone.now().strftime('%H:%M:%S')
        elif len(start_time) == 5:
            self.start_time = start_time + ":00"
        else:
            self.start_time = start_time

        if startstop == '':
            self.first_stop, dist = self.findstop(float(start_long), float(start_lat))
            current_time = datetime.strptime(
                start_time, '%H:%M:%S') + timedelta(minutes=(int(round(dist * 12, 0))))
            self.firstwalk = int(round(dist * 12, 0))
            self.current_time = current_time.strftime('%H:%M:%S')
        else:
            self.first_stop = startstop
            self.firstwalk = 0
            self.current_time = start_time

        if endstop == '':
            self.last_stop, dist = self.findstop(float(end_long), float(end_lat))
            self.lastwalk = int(round(dist * 12, 0))
        else:
            self.last_stop = endstop
            self.lastwalk = 0
        self.current_time = datetime.strptime(self.current_time, '%H:%M:%S')
        self.route, self.path, self.pathfind, self.g = self.get_routes(self.first_stop, self.last_stop)
    # find closest stop to coords
    def findstop(self, latitude, longitude):

        R = 6373.0
        min_distance = 100000.0
        min_distance_index = 0
        for stop in TramStop.objects.all():

            lat1 = radians(latitude)
            lon1 = radians(longitude)
            lat2 = radians(stop.latitude)
            lon2 = radians(stop.longitude)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            xxx = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * xxx
            if distance < min_distance:

                min_distance = distance
                min_distance_index = stop.pk

        return (min_distance_index, min_distance)

    # find stop index in the dictionary
    def transstop(self, target):
        for count, each in enumerate(TramStop.objects.all()):
            if each.pk == int(target):
                return count


    def get_routes(self, first_stop, last_stop):
        graph = Graph(TramStop.objects.count())

        graph.end = self.transstop(last_stop)

        route, path, pathfind = graph.dijkstra(self.transstop(first_stop))
        if route[-1] == 'walk':
            del route[-1]
        if route[0] == 'walk':
            del route[0]
            del path[0]
        return (route, path, pathfind, graph)

    def get_routedict(self):
        current_stop_index = 0
        routedict = {}
        for count, each in enumerate(self.route):
            if each != 'walk':
                for stime in json.loads(StopTimetable.objects.filter(stop=self.g.vdict[self.path[current_stop_index]]).filter(line=each)[0].timearray):
                    if self.current_time < datetime.strptime(stime, '%H:%M:%S'):
                        self.current_time = datetime.strptime(stime, '%H:%M:%S')
                        break
                delta = LineTimetable.objects.filter(line=each).filter(stop=self.g.vdict[self.pathfind[each][-1]])[
                    0].time_since_0 - LineTimetable.objects.filter(line=each).filter(stop=self.g.vdict[self.path[current_stop_index]])[0].time_since_0
                end_time = self.current_time + timedelta(minutes=delta)
                routedict[count] = {
                    'start': str(self.g.vdict[self.path[current_stop_index]]),
                    'line': str(each),
                    'line_direction': str(each.last_stop),
                    'line_number': each.number,
                    'start_time': self.current_time.strftime('%H:%M'),
                    'end': str(self.g.vdict[self.pathfind[each][-1]]),
                    'stopslist': [[(float(self.g.vdict[x].latitude), float(self.g.vdict[x].longitude)), str(self.g.vdict[x]),
                                (self.current_time + timedelta(minutes=(LineTimetable.objects.filter(line=each).filter(stop=self.g.vdict[x])[0].time_since_0
                                 - LineTimetable.objects.filter(line=each).filter(stop=self.g.vdict[self.path[current_stop_index]])[0].time_since_0))).strftime('%H:%M')]
                                 for x in self.path[current_stop_index:self.path.index(self.pathfind[each][-1]) + 1]],
                    'end_time': end_time.strftime('%H:%M'),
                    'triptime': (end_time - self.current_time).seconds / 60
                }
                self.current_time = end_time
                current_stop_index = self.path.index(self.pathfind[each][-1])

            else:
                delta = 1
                end_time = self.current_time + timedelta(minutes=delta)
                routedict[count] = {
                    'start': str(self.g.vdict[self.path[current_stop_index]]),
                    'line': 'walk',
                    'line_direction': str(self.g.vdict[self.path[current_stop_index + 1]]),
                    'start_time': self.current_time.strftime('%H:%M'),
                    'end': str(self.g.vdict[self.path[current_stop_index + 1]]),
                    'end_time': end_time.strftime('%H:%M'),
                    'stopslist': [[(float(self.g.vdict[x].latitude),
                                 float(self.g.vdict[x].longitude)),
                                 str(self.g.vdict[x]),
                                 'timetime'] for x in self.path[current_stop_index:self.path.index(self.path[current_stop_index + 1]) + 1]],
                    'triptime': (end_time - self.current_time).seconds / 60
                }
                self.current_time = end_time
                current_stop_index += 1
        return routedict

    def get_dict_w_times(self):
        routedict = self.get_routedict()
        stime =  (datetime.strptime(routedict[0]['start_time'], '%H:%M') - timedelta(minutes=self.firstwalk)).strftime(
            '%H:%M')
        etime = (datetime.strptime(routedict[len(routedict) - 1]['end_time'], '%H:%M') + timedelta(minutes=self.lastwalk)).strftime('%H:%M')
        ttime = datetime.strptime(etime, '%H:%M') - datetime.strptime(stime, '%H:%M')
        tts = datetime.strptime(stime, '%H:%M') - datetime.strptime(self.start_time, '%H:%M:%S')
        tfn = datetime.strptime(stime, '%H:%M') - datetime.strptime(timezone.localtime().strftime('%H:%M'), '%H:%M')
        routedict[100] = [self.firstwalk, self.lastwalk, stime, etime,int(ttime.seconds/60),int(tts.seconds/60),int(tfn.seconds/60)]
        return json.dumps(routedict)

# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph


class Graph():
#
    def __init__(self, vertices):
#
        self.V = vertices
        self.graph = json.loads(AdjacencyMatrix.objects.all().latest().matrix)
        self.Lgraph = json.loads(LineMatrix.objects.all().latest().matrix)
        self.vdict = {}
        for count, each in enumerate(TramStop.objects.all()):
            self.vdict[count] = each
        self.end = 1

# sorts path into dict of Line objects containing stops from path
    def pathfinder(self, node, lines, path):
        sets = {}
        lines = list(lines)
        lineSet = {}

        if lines == []:
            path.append(node)
            lines.append(self.vdict[node].line.all()[0].pk)

        for line in lines:
            linestoplist = []
            for each in LineTimetable.objects.filter(line=line).order_by('order'):
                linestoplist.append(each.stop.pk)

            sets[line] = []
            for v in path:
                if (self.vdict[v].pk in linestoplist) == True:
                    sets[line].append(v)


        for k, p in sets.items():
            lineSet[Line.objects.get(pk=k)] = sets[k]
        return lineSet



# Returns a list of Lines that together cover path
    def routeer(self, path, sets):
        route = []
        current = path[0]
        todel = []

        for k, p in sets.items():
            stops = [self.vdict[x] for x in p]
            timetables = [LineTimetable.objects.filter(line=k).filter(stop=stops[-1])[0],
                          LineTimetable.objects.filter(line=k).filter(stop=stops[0])[0]]
            if timetables[0].order - timetables[1].order != len(p) - 1:
                todel.append(k)
        for k in todel:
            del sets[k]
        while True:
            inn = False
            for k, p in sets.items():
                if current in p and current != p[-1]:
                    inn = True
            if inn == False and current != path[-1]:
                current = path[path.index(current) + 1]
                route.append('walk')
            elif inn == False:
                route.append('walk')
                return route

            if current == path[-1]:
                return route

            for k, p in sets.items():
                if current in p and path[-1] in p:
                    sum = 0
                    sum += len(p)
                    for each in route:
                        if each == 'walk':
                            sum += 1
                        else:
                            sum += len(sets[each])
                    if sum >= len(path):
                        route.append(k)
                        return route


            longest = 0
            for ka, pa in sets.items():
                if ka not in route and current in pa and current != pa[-1]:
                    if len(pa) > longest:
                        long_dir = ka
                        longest = len(sets[ka])

            current = sets[long_dir][-1]
            route.append(long_dir)

    def printSolution(self, dist, pathset, lines):
        node = self.end
        route = self.routeer(pathset[node], self.pathfinder(
            node, lines[node], pathset[node]))
        path = pathset[node]
        pathfind = self.pathfinder(node, lines[node], pathset[node])
        return route, path, pathfind

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree

    def minDistance(self, dist, sptSet):

         # Initialize minimum distance for next node
        min = sys.maxsize

        # Search not nearest vertex not in the
        # shortest path tree
        min_index = 19999
        for v in range(self.V):

            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v



        return min_index

    def linepath(self, currentlines, adjacentlines):
        if adjacentlines == 0:
            adjacentlines = [0]
        intersectedlines = []
        penalty = 0
        walkpenalty = 1
        # //wtf w ogole o co cho że tranferpenalty wpływa na przechodzenie po tych samych przystankach
        transferpenalty = 2
        if len(currentlines) == 0:
            if adjacentlines == [0]:
                penalty = walkpenalty
            else:
                # penalty = transferpenalty
                intersectedlines = adjacentlines.copy()
        elif len(currentlines) > 0 and adjacentlines == [0]:
            pass
        elif len(currentlines) > 0 and len(adjacentlines) > 0:
            for line in currentlines:
                if line in adjacentlines:
                    intersectedlines.append(line)
        if len(intersectedlines) == 0:
            penalty = transferpenalty

            if adjacentlines != [0]:
                intersectedlines = adjacentlines.copy()
        return intersectedlines, penalty

    # Funtion that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation

    def dijkstra(self, src):

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        pathset = [[]] * self.V
        lines = [set()] * self.V
        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:

                    intersectedlines = []
                    intersectedlines, penalty = self.linepath(
                        lines[u], self.Lgraph[u][v])

                    dist[v] = dist[u] + self.graph[u][v]
                    dist[v] = dist[v] + penalty

                    pathset[v] = pathset[u].copy()
                    pathset[v].append(u)

                    lines[v] = lines[u].copy()
                    for each in intersectedlines:
                        lines[v].add(each)
        for count, each in enumerate(pathset):
            each.append(count)
        return self.printSolution(dist, pathset, lines)






class Driver():
    def __init__(self, startstop = '', endstop = '', start_time = '', start_long, start_lat, end_long, end_lat):

        if start_time == '':
            self.start_time = timezone.now().strftime('%H:%M:%S')
        elif len(start_time) == 5:
            self.start_time = start_time + ":00"
        else:
            self.start_time = start_time

        if startstop == '':
            self.first_stop, dist = self.findstop(float(start_long), float(start_lat))
            current_time = datetime.strptime(
                start_time, '%H:%M:%S') + timedelta(minutes=(int(round(dist * 12, 0))))
            self.firstwalk = int(round(dist * 12, 0))
            self.current_time = current_time.strftime('%H:%M:%S')
        else:
            self.first_stop = startstop
            self.firstwalk = 0
            self.current_time = start_time

        if endstop == '':
            self.last_stop, dist = self.findstop(float(end_long), float(end_lat))
            self.lastwalk = int(round(dist * 12, 0))
        else:
            self.last_stop = endstop
            self.lastwalk = 0
        self.current_time = datetime.strptime(self.current_time, '%H:%M:%S')
        self.route, self.path, self.pathfind = elf.get_routes(self.first_stop, sef.last_stop)
    # find closest stop to coords
    def findstop(self, latitude, longitude):

        R = 6373.0
        min_distance = 100000.0
        min_distance_index = 0
        for stop in TramStop.objects.all():

            lat1 = radians(latitude)
            lon1 = radians(longitude)
            lat2 = radians(stop.latitude)
            lon2 = radians(stop.longitude)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            xxx = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * xxx
            if distance < min_distance:

                min_distance = distance
                min_distance_index = stop.pk

        return (min_distance_index, min_distance)

    # find stop index in the dictionary
    def transstop(self, target):
        for count, each in enumerate(TramStop.objects.all()):
            if each.pk == int(target):
                return count


    def get_routes(self, first_stop, last_stop):
        g = Graph(TramStop.objects.count())

        g.end = transstop(last_stop)

        route, path, pathfind = g.dijkstra(transstop(first_stop))
        if route[-1] == 'walk':
            del route[-1]
        if route[0] == 'walk':
            del route[0]
            del path[0]
        return (route, path, pathfind)

    def get_routedict(self, route, path, pathfind, current_time):
        current_stop_index = 0
        routedict = {}
        for count, each in enumerate(route):
            if each != 'walk':
                for stime in json.loads(StopTimetable.objects.filter(stop=g.vdict[path[current_stop_index]]).filter(line=each)[0].timearray):
                    if current_time < datetime.strptime(stime, '%H:%M:%S'):
                        current_time = datetime.strptime(stime, '%H:%M:%S')
                        break
                delta = LineTimetable.objects.filter(line=each).filter(stop=g.vdict[pathfind[each][-1]])[
                    0].time_since_0 - LineTimetable.objects.filter(line=each).filter(stop=g.vdict[path[current_stop_index]])[0].time_since_0
                end_time = current_time + timedelta(minutes=delta)
                routedict[count] = {
                    'start': str(g.vdict[path[current_stop_index]]),
                    'line': str(each),
                    'line_direction': str(each.last_stop),
                    'line_number': each.number,
                    'start_time': current_time.strftime('%H:%M'),
                    'end': str(g.vdict[pathfind[each][-1]]),
                    'stopslist': [[(float(g.vdict[x].latitude), float(g.vdict[x].longitude)), str(g.vdict[x]),
                                (current_time + timedelta(minutes=(LineTimetable.objects.filter(line=each).filter(stop=g.vdict[x])[0].time_since_0
                                 - LineTimetable.objects.filter(line=each).filter(stop=g.vdict[path[current_stop_index]])[0].time_since_0))).strftime('%H:%M')]
                                 for x in path[current_stop_index:path.index(pathfind[each][-1]) + 1]],
                    'end_time': end_time.strftime('%H:%M'),
                    'triptime': (end_time - current_time).seconds / 60
                }
                self.current_time = end_time
                current_stop_index = path.index(pathfind[each][-1])

            else:
                delta = 1
                end_time = self.current_time + timedelta(minutes=delta)
                routedict[count] = {
                    'start': str(g.vdict[path[current_stop_index]]),
                    'line': 'walk',
                    'line_direction': str(g.vdict[path[current_stop_index + 1]]),
                    'start_time': self.current_time.strftime('%H:%M'),
                    'end': str(g.vdict[path[current_stop_index + 1]]),
                    'end_time': end_time.strftime('%H:%M'),
                    'stopslist': [[(float(g.vdict[x].latitude),
                                 float(g.vdict[x].longitude)),
                                 str(g.vdict[x]),
                                 'timetime'] for x in path[current_stop_index:path.index(path[current_stop_index + 1]) + 1]],
                    'triptime': (end_time - self.current_time).seconds / 60
                }
                self.current_time = end_time
                current_stop_index += 1
        return routedict

    def get_dict_w_times(self,routedict):
        stime =  (datetime.strptime(routedict[0]['start_time'], '%H:%M') - timedelta(minutes=self.firstwalk)).strftime(
            '%H:%M')
        etime = (datetime.strptime(routedict[len(routedict) - 1]['end_time'], '%H:%M') + timedelta(minutes=self.lastwalk)).strftime('%H:%M')
        ttime = datetime.strptime(etime, '%H:%M') - datetime.strptime(stime, '%H:%M')
        tts = datetime.strptime(stime, '%H:%M') - datetime.strptime(self.start_time, '%H:%M:%S')
        tfn = datetime.strptime(stime, '%H:%M') - datetime.strptime(timezone.localtime().strftime('%H:%M'), '%H:%M')
        routedict[100] = [self.firstwalk, self.lastwalk, stime, etime,int(ttime.seconds/60),int(tts.seconds/60),int(tfn.seconds/60)]
        return json.dumps(routedict)
