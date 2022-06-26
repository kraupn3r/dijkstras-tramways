from rest_framework import serializers
from .models import TramStop

class TramStopSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super(TramStopSerializer, self).to_representation(instance)
        rep['nameno'] = str(instance)
        rep['longitude'] = float(instance.longitude)
        rep['latitude'] = float(instance.latitude)
        return rep
    nameno = serializers.CharField(source='tramstop.name', read_only=True)

    class Meta:
        model = TramStop
        fields = [
            'id',
            'name',
            'nameno',
            'longitude',
            'latitude',
              ]
