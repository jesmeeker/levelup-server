"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer


class GameView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)
    
class GamerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ('id', )

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    gamer = GamerSerializer(many=False)
    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'game_type', 'min_player', 'max_player', 'gamer')