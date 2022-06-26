import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import TramStop
from .serializers import TramStopSerializer
from .dijkstra import Driver



class SearchView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fromlist'] = json.dumps(self.request.session['fromlist'])
        context['tolist'] = json.dumps(self.request.session['tolist'])
        return context

    def get(self, request, *args, **kwargs):
        if 'fromlist' not in request.session:
            request.session['fromlist'] = []
        if 'tolist' not in request.session:
            request.session['tolist'] = []
        context = self.get_context_data()

        return render(request, self.template_name, context)


class TramStopAPIView(generics.ListAPIView):

    serializer_class = TramStopSerializer

    def get_queryset(self):
        queryset = TramStop.objects.all()
        if self.request.GET.get('q') != None and self.request.GET.get('q') != '':
            query = self.request.GET.get('q')
            queryset = queryset.filter(name__icontains=query).order_by(
                'name').distinct('name')

        if self.request.GET.get('qs') != None and self.request.GET.get('qs') != '':
            query = self.request.GET.get('qs')
            qlist = [int(e) for e in query.split(',')]
            queryset = queryset.filter(pk__in=qlist)
        print(queryset)
        return queryset


class ApiView(APIView):

    def get(self, request, *args, **kwargs):

        start_lat = request.GET.get('slat')
        start_long = request.GET.get('slong')
        end_lat = request.GET.get('elat')
        end_long = request.GET.get('elong')
        start_point = request.GET.get('spoint', '')
        end_point = request.GET.get('epoint', '')
        start_time = request.GET.get('stime', '')

        if start_point != '' and int(start_point) not in request.session['fromlist']:
            request.session['fromlist'] += [int(start_point)]

        if end_point != '' and int(end_point) not in request.session['tolist']:
            request.session['tolist'] += [int(end_point)]

        dijsktra_driver = Driver(
            start_point, end_point, start_time, start_lat, start_long, end_lat, end_long)
        response = dijsktra_driver.get_dict_w_times()
        return JsonResponse(json.loads(str(response)), status=status.HTTP_200_OK)
