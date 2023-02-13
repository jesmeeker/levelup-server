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
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        try:
            authenticated_player = Gamer.objects.get(user=request.auth.user)

        except Gamer.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            game = Game.objects.get(pk=request.data['game'])
        except Game.DoesNotExist:
            return Response({'message': 'You sent an invalid game ID'}, status=status.HTTP_404_NOT_FOUND)
        
        event = Event.objects.create(
            date_of_event=request.data["date_of_event"],
            start_time=request.data["start_time"],
            location=request.data["location"],
            host=authenticated_player,
            game=game
        )
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        # try:
        #     authenticated_player = Gamer.objects.get(user=request.auth.user)

        # except Gamer.DoesNotExist:
        #     return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            game = Game.objects.get(pk=request.data['game'])
        except Game.DoesNotExist:
            return Response({'message': 'You sent an invalid game ID'}, status=status.HTTP_404_NOT_FOUND)
        
        event_to_update = Event.objects.get(pk=pk)
        event_to_update.date_of_event=request.data["date_of_event"]
        event_to_update.start_time=request.data["start_time"]
        event_to_update.location=request.data["location"]
        event_to_update.game=game
        event_to_update.save()

        serializer = EventSerializer(event_to_update)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

    
class EventGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'name', )

class EventHostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ('full_name',)

class EventAttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ('full_name',)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    game = EventGameSerializer(many=False)
    host = EventHostSerializer(many=False)
    attendees = EventAttendeeSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'date_of_event', 'start_time', 'location', 'game', 'host', 'attendees')