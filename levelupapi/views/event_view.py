"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = []

        if "game" in request.query_params:
            query = request.GET.get('game')
            query_int = int(query)
            events = Event.objects.all()
            events = events.filter(game_id=query_int)
        else:
            events = Event.objects.all()

        serialized = EventSerializer(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
class EventGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', )

class EventHostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ('id', )

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    game = EventGameSerializer(many=False)
    host = EventHostSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'date_of_event', 'location', 'game', 'host')